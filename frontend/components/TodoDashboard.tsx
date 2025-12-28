'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, CheckCircle2, Circle, Clock, Trash2, TrendingUp, Zap, BarChart3, PieChart } from 'lucide-react';
import { Task, Stats } from '../types';
import TaskItem from './TaskItem';
import GlassTile from './GlassTile';
import EditTaskModal from './EditTaskModal';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../lib/api';

interface Props {
  initialTasks: Task[];
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const TodoDashboard: React.FC<Props> = ({ initialTasks }) => {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState<'all' | 'pending' | 'in_progress' | 'completed'>('all');
  const [sortBy, setSortBy] = useState<'date' | 'priority' | 'status'>('date');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const { token, user } = useAuth();

  useEffect(() => {
    if (token) {
      let statusFilter = undefined;
      if (filter !== 'all') {
        statusFilter = filter;
      }
      fetchTasks(statusFilter);
    }
  }, [token, filter]);

  // Filter and sort tasks
  const filteredAndSortedTasks = React.useMemo(() => {
    let result = [...tasks];

    // Apply filter
    if (filter !== 'all') {
      result = result.filter(task => task.status === filter);
    }

    // Apply sorting
    switch (sortBy) {
      case 'priority':
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        result.sort((a, b) => priorityOrder[b.priority as keyof typeof priorityOrder] - priorityOrder[a.priority as keyof typeof priorityOrder]);
        break;
      case 'status':
        const statusOrder = { completed: 3, in_progress: 2, pending: 1 };
        result.sort((a, b) => statusOrder[b.status as keyof typeof statusOrder] - statusOrder[a.status as keyof typeof statusOrder]);
        break;
      case 'date':
      default:
        result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        break;
    }

    return result;
  }, [tasks, filter, sortBy]);

  const fetchTasks = async (statusFilter?: string) => {
    if (!token) return;

    try {
      setLoading(true);
      const response = await api.getTasks(token, statusFilter);
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (id: string) => {
    if (!token) return;

    try {
      const task = tasks.find(t => t.id === id);
      if (!task) return;

      // Optimistically update the UI
      const updatedStatus = task.status === 'completed' ? 'pending' : 'completed';
      setTasks(prev => prev.map(t =>
        t.id === id ? { ...t, status: updatedStatus as 'pending' | 'completed' } : t
      ));

      // Update on the server using the toggle method
      await api.toggleTaskCompletion(token, id);
      await fetchTasks(); // Refresh tasks to ensure consistency
    } catch (error) {
      console.error('Failed to update task:', error);
      // Revert optimistic update on error
      fetchTasks();
    }
  };

  const handleDelete = async (id: string) => {
    if (!token) return;

    try {
      // Optimistically update the UI
      setTasks(prev => prev.filter(t => t.id !== id));

      // Delete on the server
      await api.deleteTask(token, id);
    } catch (error) {
      console.error('Failed to delete task:', error);
      // Revert optimistic update on error
      fetchTasks();
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(prev => prev.map(t => t.id === updatedTask.id ? updatedTask : t));
    setEditingTask(null);
  };

  const completedCount = tasks.filter(t => t.status === 'completed').length;
  const progress = tasks.length > 0 ? (completedCount / tasks.length) * 100 : 0;

  if (loading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className={`animate-pulse bg-white/5 rounded-3xl h-48 border border-white/5 ${i === 1 ? 'lg:col-span-2 lg:row-span-2' : ''}`}
          />
        ))}
      </div>
    );
  }

  return (
    <>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 grid-rows-auto gap-6"
      >
      {/* Header Stat Tile */}
      <GlassTile className="p-6 flex flex-col justify-between">
        <div className="flex items-center justify-between mb-4">
          <div className="p-2 bg-indigo-500/10 rounded-xl">
            <Zap className="w-5 h-5 text-indigo-400" />
          </div>
          <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">Productivity</span>
        </div>
        <div>
          <h3 className="text-3xl font-bold text-white mb-1">{Math.round(progress)}%</h3>
          <p className="text-sm text-white/50">Completion rate today</p>
        </div>
        <div className="w-full bg-white/5 h-1.5 rounded-full mt-4 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            className="h-full bg-gradient-to-r from-indigo-500 to-pink-500"
          />
        </div>
      </GlassTile>

      {/* Main Task List Tile */}
      <GlassTile className="lg:col-span-2 lg:row-span-3 overflow-hidden flex flex-col min-h-[600px]">
        <div className="p-6 border-b border-white/5 flex items-center justify-between sticky top-0 bg-white/5 backdrop-blur-md z-10">
          <div>
            <h2 className="text-xl font-bold text-white">Current Tasks</h2>
            <p className="text-sm text-white/40">{tasks.filter(t => t.status !== 'completed').length} pending actions</p>
          </div>
          <div className="flex space-x-2">
            <button
              className={`px-3 py-1 text-xs rounded-full font-medium transition-colors ${
                filter === 'all'
                  ? 'bg-indigo-500/20 text-indigo-300'
                  : 'hover:bg-white/5 text-white/50'
              }`}
              onClick={() => setFilter('all')}
            >
              All
            </button>
            <button
              className={`px-3 py-1 text-xs rounded-full font-medium transition-colors ${
                filter === 'pending'
                  ? 'bg-amber-500/20 text-amber-300'
                  : 'hover:bg-white/5 text-white/50'
              }`}
              onClick={() => setFilter('pending')}
            >
              Pending
            </button>
            <button
              className={`px-3 py-1 text-xs rounded-full font-medium transition-colors ${
                filter === 'in_progress'
                  ? 'bg-blue-500/20 text-blue-300'
                  : 'hover:bg-white/5 text-white/50'
              }`}
              onClick={() => setFilter('in_progress')}
            >
              In Progress
            </button>
            <button
              className={`px-3 py-1 text-xs rounded-full font-medium transition-colors ${
                filter === 'completed'
                  ? 'bg-emerald-500/20 text-emerald-300'
                  : 'hover:bg-white/5 text-white/50'
              }`}
              onClick={() => setFilter('completed')}
            >
              Completed
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
          {filteredAndSortedTasks.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-white/30 py-20">
              <Calendar className="w-12 h-12 mb-4 opacity-20" />
              <p>No tasks found. Create one to get started!</p>
            </div>
          ) : (
            filteredAndSortedTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onToggle={handleToggle}
                onDelete={handleDelete}
                onEdit={handleEdit}
              />
            ))
          )}
        </div>
      </GlassTile>

      {/* Side Tile - Next 7 Days Activity */}
      <GlassTile className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="p-2 bg-pink-500/10 rounded-xl">
            <BarChart3 className="w-5 h-5 text-pink-400" />
          </div>
          <span className="text-xs font-semibold text-pink-400 uppercase tracking-wider">Next 7 Days</span>
        </div>
        <div className="h-40 flex items-center justify-center">
          <p className="text-white/50 text-center">Activity chart placeholder</p>
        </div>
      </GlassTile>

      {/* Side Tile - Priority Distribution */}
      <GlassTile className="p-6 lg:row-span-2 flex flex-col">
        <div className="flex items-center justify-between mb-6">
          <div className="p-2 bg-emerald-500/10 rounded-xl">
            <PieChart className="w-5 h-5 text-emerald-400" />
          </div>
          <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Segments</span>
        </div>
        <div className="flex-1 flex flex-col justify-center">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-white/50">Low Priority</span>
              <span className="text-sm font-bold text-emerald-400">
                {tasks.filter(t => t.priority === 'low').length}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-white/50">Medium Priority</span>
              <span className="text-sm font-bold text-amber-400">
                {tasks.filter(t => t.priority === 'medium').length}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-white/50">High Priority</span>
              <span className="text-sm font-bold text-red-400">
                {tasks.filter(t => t.priority === 'high').length}
              </span>
            </div>
          </div>
        </div>
      </GlassTile>

      {/* Summary Tile */}
      <GlassTile className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="p-2 bg-blue-500/10 rounded-xl">
            <TrendingUp className="w-5 h-5 text-blue-400" />
          </div>
          <span className="text-xs font-semibold text-blue-400 uppercase tracking-wider">Summary</span>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-white/50">Total Tasks</span>
            <span className="text-sm font-bold text-white">{tasks.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-white/50">Completed</span>
            <span className="text-sm font-bold text-emerald-400">{completedCount}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-white/50">Pending</span>
            <span className="text-sm font-bold text-amber-400">{tasks.filter(t => t.status !== 'completed').length}</span>
          </div>
        </div>
      </GlassTile>
    </motion.div>

    {editingTask && (
      <EditTaskModal
        isOpen={!!editingTask}
        onClose={() => setEditingTask(null)}
        task={editingTask}
        onTaskUpdated={handleTaskUpdated}
      />
    )}
    </>
  );
};

export default TodoDashboard;
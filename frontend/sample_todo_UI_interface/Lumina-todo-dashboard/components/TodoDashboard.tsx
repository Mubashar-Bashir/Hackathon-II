
import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, CheckCircle2, Circle, Clock, Trash2, TrendingUp, Zap, BarChart3, PieChart } from 'lucide-react';
import { Task } from '../types';
import PriorityDistribution from './PriorityDistribution';
import ActivityChart from './ActivityChart';
import GlassTile from './GlassTile';

interface Props {
  tasks: Task[];
  isLoading: boolean;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
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

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1 }
};

const TodoDashboard: React.FC<Props> = ({ tasks, isLoading, onToggle, onDelete }) => {
  const completedCount = tasks.filter(t => t.completed).length;
  const progress = tasks.length > 0 ? (completedCount / tasks.length) * 100 : 0;

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className={`animate-pulse bg-white/5 rounded-3xl h-48 border border-white/5 ${i === 1 ? 'lg:col-span-2 lg:row-span-2' : ''}`} />
        ))}
      </div>
    );
  }

  return (
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
            <p className="text-sm text-white/40">{tasks.filter(t => !t.completed).length} pending actions</p>
          </div>
          <div className="flex space-x-2">
            <button className="px-3 py-1 text-xs rounded-full bg-indigo-500/20 text-indigo-300 font-medium">All</button>
            <button className="px-3 py-1 text-xs rounded-full hover:bg-white/5 text-white/50 transition-colors">Priority</button>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
          {tasks.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-white/30 py-20">
              <Calendar className="w-12 h-12 mb-4 opacity-20" />
              <p>No tasks yet. Create one to get started!</p>
            </div>
          ) : (
            tasks.map(task => (
              <motion.div
                layout
                key={task.id}
                variants={itemVariants}
                className={`group p-4 rounded-2xl border transition-all duration-300 flex items-start space-x-4
                  ${task.completed ? 'bg-emerald-500/5 border-emerald-500/10 opacity-60' : 'bg-white/5 border-white/10 hover:border-indigo-500/50 hover:shadow-[0_0_20px_rgba(99,102,241,0.15)] hover:bg-white/[0.08]'}
                `}
              >
                <button 
                  onClick={() => onToggle(task.id)}
                  className={`mt-1 flex-shrink-0 transition-transform active:scale-90 ${task.completed ? 'text-emerald-400' : 'text-white/30 hover:text-indigo-400'}`}
                >
                  {task.completed ? <CheckCircle2 className="w-6 h-6" /> : <Circle className="w-6 h-6" />}
                </button>
                
                <div className={`flex-1 ${task.isUrdu ? 'text-right' : ''}`}>
                  <h4 className={`text-base font-semibold transition-all ${task.completed ? 'line-through text-white/30' : 'text-white/90'} ${task.isUrdu ? 'urdu-text text-xl' : ''}`}>
                    {task.title}
                  </h4>
                  <p className={`text-sm mt-1 leading-relaxed ${task.completed ? 'text-white/20' : 'text-white/50'} ${task.isUrdu ? 'urdu-text text-lg leading-loose' : ''}`}>
                    {task.description}
                  </p>
                  
                  <div className={`mt-3 flex items-center gap-3 ${task.isUrdu ? 'flex-row-reverse' : 'flex-row'}`}>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider
                      ${task.priority === 'high' ? 'bg-red-500/10 text-red-400' : task.priority === 'medium' ? 'bg-amber-500/10 text-amber-400' : 'bg-emerald-500/10 text-emerald-400'}
                    `}>
                      {task.priority}
                    </span>
                    <span className="flex items-center text-[10px] text-white/30 font-medium">
                      <Clock className="w-3 h-3 mr-1" />
                      {task.dueDate}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] bg-white/5 text-white/40 uppercase tracking-tighter">
                      {task.category}
                    </span>
                  </div>
                </div>

                <button 
                  onClick={() => onDelete(task.id)}
                  className="opacity-0 group-hover:opacity-100 p-2 hover:bg-red-500/10 rounded-lg text-white/20 hover:text-red-400 transition-all"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </motion.div>
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
        <div className="h-40">
          <ActivityChart tasks={tasks} />
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
          <PriorityDistribution tasks={tasks} />
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
            <span className="text-sm text-white/50">Total Projects</span>
            <span className="text-sm font-bold text-white">{tasks.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-white/50">Urdu Tasks</span>
            <span className="text-sm font-bold text-white">{tasks.filter(t => t.isUrdu).length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-white/50">High Priority</span>
            <span className="text-sm font-bold text-red-400">{tasks.filter(t => t.priority === 'high').length}</span>
          </div>
        </div>
      </GlassTile>

    </motion.div>
  );
};

export default TodoDashboard;


import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, LayoutDashboard, Settings, User, Bell, Search } from 'lucide-react';
import confetti from 'canvas-confetti';
import { Task, Priority } from './types';
import { INITIAL_TASKS, COLORS } from './constants';
import TodoDashboard from './components/TodoDashboard';
import AddTaskModal from './components/AddTaskModal';

const App: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>(() => {
    const saved = localStorage.getItem('lumina_tasks');
    return saved ? JSON.parse(saved) : INITIAL_TASKS;
  });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate initial fetching delay
    const timer = setTimeout(() => setIsLoading(false), 1500);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    localStorage.setItem('lumina_tasks', JSON.stringify(tasks));
  }, [tasks]);

  const toggleTask = (id: string) => {
    setTasks(prev => prev.map(task => {
      if (task.id === id) {
        if (!task.completed) {
          confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
            colors: [COLORS.primary, COLORS.secondary, COLORS.success]
          });
        }
        return { ...task, completed: !task.completed };
      }
      return task;
    }));
  };

  const addTask = (task: Omit<Task, 'id' | 'completed'>) => {
    const newTask: Task = {
      ...task,
      id: Math.random().toString(36).substr(2, 9),
      completed: false
    };
    setTasks(prev => [newTask, ...prev]);
    setIsModalOpen(false);
  };

  const deleteTask = (id: string) => {
    setTasks(prev => prev.filter(t => t.id !== id));
  };

  return (
    <div className="min-h-screen text-slate-200 bg-[#0f172a] selection:bg-indigo-500/30">
      {/* Mesh Gradients */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-600/20 blur-[120px] animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-pink-600/20 blur-[120px] animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-[20%] right-[10%] w-[30%] h-[30%] rounded-full bg-blue-600/10 blur-[100px]" />
      </div>

      {/* Navigation Bar */}
      <nav className="sticky top-0 z-40 backdrop-blur-xl border-b border-white/5 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <LayoutDashboard className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Lumina</span>
          </div>
          <div className="hidden md:flex items-center space-x-6">
            <a href="#" className="text-sm font-medium text-white/90 hover:text-white transition-colors">Dashboard</a>
            <a href="#" className="text-sm font-medium text-white/50 hover:text-white transition-colors">Calendar</a>
            <a href="#" className="text-sm font-medium text-white/50 hover:text-white transition-colors">Analytics</a>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <button className="p-2 hover:bg-white/5 rounded-full transition-colors">
            <Search className="w-5 h-5 text-white/60" />
          </button>
          <button className="p-2 hover:bg-white/5 rounded-full transition-colors relative">
            <Bell className="w-5 h-5 text-white/60" />
            <span className="absolute top-2 right-2 w-2 h-2 bg-pink-500 rounded-full border-2 border-[#0f172a]"></span>
          </button>
          <div className="h-8 w-[1px] bg-white/10 mx-2"></div>
          <button className="flex items-center space-x-2 p-1.5 hover:bg-white/5 rounded-lg transition-colors">
            <img src="https://picsum.photos/id/64/32/32" className="w-8 h-8 rounded-lg object-cover border border-white/10" alt="User" />
            <span className="text-sm font-medium hidden sm:inline">Alex Rivera</span>
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8 pb-32">
        <TodoDashboard 
          tasks={tasks} 
          isLoading={isLoading} 
          onToggle={toggleTask} 
          onDelete={deleteTask}
        />
      </main>

      {/* Floating Action Button */}
      <motion.button
        whileHover={{ scale: 1.1, rotate: 90 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsModalOpen(true)}
        className="fixed bottom-8 right-8 w-14 h-14 bg-gradient-to-br from-indigo-500 via-indigo-600 to-pink-500 rounded-2xl flex items-center justify-center text-white shadow-2xl shadow-indigo-500/40 z-50 group overflow-hidden"
      >
        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
        <Plus className="w-8 h-8 relative z-10" />
      </motion.button>

      {/* Modals */}
      <AnimatePresence>
        {isModalOpen && (
          <AddTaskModal 
            isOpen={isModalOpen} 
            onClose={() => setIsModalOpen(false)} 
            onAdd={addTask} 
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default App;

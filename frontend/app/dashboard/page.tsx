'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, LayoutDashboard, Settings, User, Search } from 'lucide-react';
import { useRouter } from 'next/navigation';
import confetti from 'canvas-confetti';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification, NotificationProvider } from '../../contexts/NotificationContext';
import TodoDashboard from '../../components/TodoDashboard';
import AddTaskModal from '../../components/AddTaskModal';
import ProtectedRoute from '../../components/ProtectedRoute';
import UserProfileDropdown from '../../components/UserProfileDropdown';
import NotificationDropdown from '../../components/NotificationDropdown';
import { Task } from '../../types';
import { api } from '../../lib/api';

const DashboardPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const { user, token, logout: contextLogout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    contextLogout(); // Perform the logout logic from context
    router.push('/login'); // Redirect to login page
  };

  useEffect(() => {
    if (token) {
      fetchTasks();
    }
  }, [token]);

  const fetchTasks = async () => {
    if (!token) return;

    try {
      setIsLoading(true);
      const response = await api.getTasks(token);
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddTask = () => {
    fetchTasks(); // Refresh tasks after adding
  };

  // Check for due and upcoming tasks periodically
  useEffect(() => {
    if (token) {
      // Check for due tasks immediately when the page loads
      const checkDueTasks = async () => {
        try {
          await api.checkDueTaskNotifications(token);
        } catch (error) {
          console.error('Failed to check due task notifications:', error);
        }
      };

      // Check for upcoming tasks (due tomorrow)
      const checkUpcomingTasks = async () => {
        try {
          await api.checkUpcomingTaskNotifications(token, 1);
        } catch (error) {
          console.error('Failed to check upcoming task notifications:', error);
        }
      };

      checkDueTasks();
      checkUpcomingTasks();

      // Set up periodic checks (every 5 minutes)
      const interval = setInterval(async () => {
        await checkDueTasks();
        await checkUpcomingTasks();
      }, 5 * 60 * 1000); // 5 minutes

      return () => clearInterval(interval);
    }
  }, [token]);

  // Colors for confetti
  const COLORS = {
    primary: '#6366f1',
    secondary: '#f472b6',
    success: '#10b981'
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
            <a href="/dashboard" className="text-sm font-medium text-white/90 hover:text-white transition-colors">Dashboard</a>
            <a href="#" className="text-sm font-medium text-white/50 hover:text-white transition-colors">Calendar</a>
            <a href="#" className="text-sm font-medium text-white/50 hover:text-white transition-colors">Analytics</a>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <button className="p-2 hover:bg-white/5 rounded-full transition-colors">
            <Search className="w-5 h-5 text-white/60" />
          </button>
          <NotificationDropdown />
          <div className="h-8 w-[1px] bg-white/10 mx-2"></div>
          <UserProfileDropdown
            user={user}
            onLogout={handleLogout}
          />
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8 pb-32">
        <TodoDashboard initialTasks={tasks} />
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
            onAdd={handleAddTask}
          />
        )}
      </AnimatePresence>
    </div>
  );
};


const DashboardPageWithProtection = () => {
  return (
    <NotificationProvider>
      <ProtectedRoute>
        <DashboardPage />
      </ProtectedRoute>
    </NotificationProvider>
  );
};

export default DashboardPageWithProtection;


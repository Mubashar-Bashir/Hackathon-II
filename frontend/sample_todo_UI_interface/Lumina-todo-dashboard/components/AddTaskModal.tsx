
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { X, Check } from 'lucide-react';
import { Priority, Task } from '../types';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onAdd: (task: Omit<Task, 'id' | 'completed'>) => void;
}

const AddTaskModal: React.FC<Props> = ({ onClose, onAdd }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<Priority>('medium');
  const [category, setCategory] = useState('General');
  const [isUrdu, setIsUrdu] = useState(false);
  const [dueDate, setDueDate] = useState(new Date().toISOString().split('T')[0]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onAdd({ title, description, priority, category, isUrdu, dueDate });
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-6">
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm"
      />
      
      <motion.div
        initial={{ scale: 0.9, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.9, opacity: 0, y: 20 }}
        className="relative bg-[#1e293b] border border-white/10 rounded-[2.5rem] w-full max-w-lg p-8 shadow-2xl overflow-hidden"
      >
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-pink-500 to-indigo-500"></div>
        
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-2xl font-bold text-white">New Task</h2>
          <button onClick={onClose} className="p-2 hover:bg-white/5 rounded-full transition-colors">
            <X className="w-6 h-6 text-white/50" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Task Title</label>
            <input 
              autoFocus
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              className={`w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-white focus:outline-none focus:border-indigo-500/50 transition-all ${isUrdu ? 'text-right urdu-text text-xl' : ''}`}
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Description</label>
            <textarea 
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add some details..."
              rows={3}
              className={`w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-white focus:outline-none focus:border-indigo-500/50 transition-all resize-none ${isUrdu ? 'text-right urdu-text text-lg' : ''}`}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Priority</label>
              <select 
                value={priority}
                onChange={(e) => setPriority(e.target.value as Priority)}
                className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-white focus:outline-none appearance-none"
              >
                <option value="low" className="bg-[#1e293b]">Low</option>
                <option value="medium" className="bg-[#1e293b]">Medium</option>
                <option value="high" className="bg-[#1e293b]">High</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-xs font-bold text-white/40 uppercase tracking-widest ml-1">Due Date</label>
              <input 
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 text-white focus:outline-none"
              />
            </div>
          </div>

          <div className="flex items-center space-x-4 pt-2">
            <button
              type="button"
              onClick={() => setIsUrdu(!isUrdu)}
              className={`flex-1 flex items-center justify-center space-x-2 p-4 rounded-2xl border transition-all ${isUrdu ? 'bg-indigo-500/20 border-indigo-500/50 text-indigo-300' : 'bg-white/5 border-white/10 text-white/40'}`}
            >
              <span className="urdu-text text-lg">اردو متن</span>
              {isUrdu && <Check className="w-4 h-4" />}
            </button>
            <button
              type="submit"
              disabled={!title.trim()}
              className="flex-[2] bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-400 hover:to-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold p-4 rounded-2xl shadow-xl shadow-indigo-500/20 transition-all active:scale-95"
            >
              Create Task
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
};

export default AddTaskModal;

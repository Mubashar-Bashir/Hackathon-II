'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, Circle, Clock, Trash2, Pencil } from 'lucide-react';
import { Task } from '../types';

interface TaskItemProps {
  task: Task;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit: (task: Task) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete, onEdit }) => {
  const priorityColors = {
    low: 'bg-emerald-500/10 text-emerald-400',
    medium: 'bg-amber-500/10 text-amber-400',
    high: 'bg-red-500/10 text-red-400',
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={`group p-4 rounded-2xl border transition-all duration-300 flex items-start space-x-4
        ${task.status === 'completed' ? 'bg-emerald-500/5 border-emerald-500/10 opacity-60' : 'bg-white/5 border-white/10 hover:border-indigo-500/50 hover:shadow-[0_0_20px_rgba(99,102,241,0.15)] hover:bg-white/[0.08]'}
      `}
    >
      <button
        onClick={() => onToggle(task.id)}
        className={`mt-1 flex-shrink-0 transition-transform active:scale-90 ${task.status === 'completed' ? 'text-emerald-400' : 'text-white/30 hover:text-indigo-400'}`}
      >
        {task.status === 'completed' ? <CheckCircle2 className="w-6 h-6" /> : <Circle className="w-6 h-6" />}
      </button>

      <div className="flex-1">
        <h4 className={`text-base font-semibold transition-all ${task.status === 'completed' ? 'line-through text-white/30' : 'text-white/90'}`}>
          {task.title}
        </h4>
        <p className="text-sm mt-1 leading-relaxed text-white/50">
          {task.description}
        </p>

        <div className="mt-3 flex items-center gap-3">
          <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider
            ${priorityColors[task.priority]}
          `}>
            {task.priority}
          </span>
          <span className="flex items-center text-[10px] text-white/30 font-medium">
            <Clock className="w-3 h-3 mr-1" />
            {task.due_date || 'No due date'}
          </span>
        </div>
      </div>

      <div className="flex space-x-1 opacity-0 group-hover:opacity-100">
        <button
          onClick={() => onEdit(task)}
          className="p-2 hover:bg-indigo-500/10 rounded-lg text-white/20 hover:text-indigo-400 transition-all"
        >
          <Pencil className="w-4 h-4" />
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="p-2 hover:bg-red-500/10 rounded-lg text-white/20 hover:text-red-400 transition-all"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </motion.div>
  );
};

export default TaskItem;
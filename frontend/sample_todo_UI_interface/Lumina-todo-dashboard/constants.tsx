
import { Task } from './types';

export const COLORS = {
  primary: '#6366f1', // Electric Indigo
  secondary: '#f472b6', // Cyber Pink
  success: '#10b981', // Emerald Aurora
  bg: '#0f172a', // Deep Slate
  priority: {
    low: '#34d399',
    medium: '#fbbf24',
    high: '#f87171',
  }
};

export const INITIAL_TASKS: Task[] = [
  {
    id: '1',
    title: 'Design System Update',
    description: 'Update the glassmorphism components for Phase II.',
    completed: false,
    priority: 'high',
    dueDate: '2024-05-20',
    category: 'Design'
  },
  {
    id: '2',
    title: 'نیا پروجیکٹ شروع کریں',
    description: 'اردو زبان میں ٹاسک لسٹ کی جانچ پڑتال کریں۔',
    completed: false,
    priority: 'medium',
    dueDate: '2024-05-22',
    category: 'Urdu',
    isUrdu: true
  },
  {
    id: '3',
    title: 'Fix Navigation Bug',
    description: 'The mobile menu is overlapping the FAB on small screens.',
    completed: true,
    priority: 'low',
    dueDate: '2024-05-18',
    category: 'Dev'
  },
  {
    id: '4',
    title: 'Client Presentation',
    description: 'Present the new bento grid layout to stakeholders.',
    completed: false,
    priority: 'high',
    dueDate: '2024-05-25',
    category: 'Meetings'
  }
];

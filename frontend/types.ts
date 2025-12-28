// Application types based on the backend API

export type Priority = 'low' | 'medium' | 'high';
export type Status = 'pending' | 'in_progress' | 'completed';

export interface Task {
  id: string;
  title: string;
  description: string;
  status: Status;
  priority: Priority;
  due_date?: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskFormData {
  title: string;
  description: string;
  priority: Priority;
  status: Status;
  due_date?: string;
}

export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  name?: string;
  password: string;
}

export interface Stats {
  total: number;
  completed: number;
  pending: number;
  priorityDistribution: {
    low: number;
    medium: number;
    high: number;
  };
  dailyActivity: { date: string; count: number }[];
}
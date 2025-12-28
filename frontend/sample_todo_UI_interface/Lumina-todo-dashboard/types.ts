
export type Priority = 'low' | 'medium' | 'high';

export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: Priority;
  dueDate: string;
  category: string;
  isUrdu?: boolean;
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

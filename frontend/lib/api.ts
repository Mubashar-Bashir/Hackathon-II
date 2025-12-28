// API client for connecting to the FastAPI backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Task {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed';
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface User {
  id: string;
  email: string;
  name?: string;
  phone?: string;
  avatar?: string;
  created_at: string;
  updated_at: string;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  name?: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Authentication methods
  async register(userData: RegisterData): Promise<User> {
    const response = await fetch(`${this.baseUrl}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }

    return response.json();
  }

  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    return response.json();
  }

  async getMe(token: string): Promise<User> {
    const response = await fetch(`${this.baseUrl}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get user info');
    }

    return response.json();
  }

  async logout(): Promise<{ message: string }> {
    // In a real implementation, you might want to invalidate the token on the server
    return { message: 'Logged out successfully' };
  }

  // Task methods
  async getTasks(token: string, status?: string, limit: number = 20, offset: number = 0): Promise<{ tasks: Task[]; total: number; offset: number; limit: number }> {
    // Use the authenticated endpoint which extracts user ID from the JWT token
    let url = `${this.baseUrl}/tasks?limit=${limit}&offset=${offset}`;
    if (status) {
      url += `&status_filter=${status}`;
    }

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get tasks');
    }

    return response.json();
  }

  async createTask(token: string, taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<Task> {
    const response = await fetch(`${this.baseUrl}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create task');
    }

    return response.json();
  }

  async getTaskById(token: string, taskId: string): Promise<Task> {
    const response = await fetch(`${this.baseUrl}/tasks/${taskId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get task');
    }

    return response.json();
  }

  async updateTask(token: string, taskId: string, taskData: Partial<Task>): Promise<Task> {
    const response = await fetch(`${this.baseUrl}/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update task');
    }

    return response.json();
  }

  async deleteTask(token: string, taskId: string): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/tasks/${taskId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to delete task');
    }

    return response.json();
  }

  async toggleTaskCompletion(token: string, taskId: string): Promise<Task> {
    const response = await fetch(`${this.baseUrl}/tasks/${taskId}`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to toggle task completion');
    }

    return response.json();
  }
}

export const api = new ApiClient();
export type { Task, User, LoginCredentials, RegisterData, LoginResponse };
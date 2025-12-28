'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { User, LoginCredentials, RegisterData, LoginResponse } from '../lib/api';
import { api } from '../lib/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  updateUserProfile: (userData: Partial<User>) => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check for existing token in localStorage on initial load
    const storedToken = localStorage.getItem('auth_token');
    const storedUser = localStorage.getItem('user');
    const storedAvatar = localStorage.getItem('user_avatar');

    if (storedToken && storedUser) {
      let user = JSON.parse(storedUser);

      // Add avatar if it exists in storage
      if (storedAvatar) {
        user = { ...user, avatar: storedAvatar };
      }

      setToken(storedToken);
      setUser(user);
    }
    setLoading(false);
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      setLoading(true);
      const response: LoginResponse = await api.login(credentials);

      setToken(response.access_token);
      localStorage.setItem('auth_token', response.access_token);

      // Get user info after login
      const userData = await api.getMe(response.access_token);
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      setLoading(true);
      await api.register(userData);
      // After registration, user needs to login
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    localStorage.removeItem('user_avatar');
  };

  const updateUserProfile = (userData: Partial<User>) => {
    if (user) {
      // Don't store avatar in localStorage to avoid quota issues
      const { avatar, ...userDataWithoutAvatar } = userData;
      const updatedUser = {
        ...user,
        ...userDataWithoutAvatar
      };

      // Add avatar to the user object if provided
      if (avatar) {
        (updatedUser as any).avatar = avatar;
      }

      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));

      // Store avatar separately if it exists
      if (avatar) {
        // Check if the avatar data is too large for localStorage
        // If it's too large, we'll skip storing it to avoid quota errors
        try {
          // Use a more conservative limit (e.g., 100KB) for safety
          if (avatar.length < 100000) { // Less than 100KB
            localStorage.setItem('user_avatar', avatar);
          } else {
            console.warn('Avatar image is too large to store in localStorage');
          }
        } catch (e) {
          // If we still hit quota errors, just skip storing the avatar
          console.warn('Failed to store avatar in localStorage due to quota limits');
        }
      }
    }
  };

  const isAuthenticated = !!token;

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    updateUserProfile,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
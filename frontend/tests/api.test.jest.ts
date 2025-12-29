// Simple test to verify API client functionality
import { api } from '../lib/api';

// Mock fetch to test API calls
global.fetch = jest.fn();

describe('API Client', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  test('should make login request correctly', async () => {
    const mockResponse = {
      access_token: 'mock-token',
      token_type: 'bearer',
      expires_in: 3600
    };

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => mockResponse,
    });

    const credentials = { email: 'test@example.com', password: 'password123' };
    const result = await api.login(credentials);

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/auth/login'),
      expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: expect.any(URLSearchParams)
      })
    );

    expect(result).toEqual(mockResponse);
  });

  test('should make register request correctly', async () => {
    const mockUser = {
      id: '123',
      email: 'test@example.com',
      name: 'Test User'
    };

    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => mockUser,
    });

    const userData = { email: 'test@example.com', name: 'Test User', password: 'password123' };
    const result = await api.register(userData);

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/auth/register'),
      expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      })
    );

    expect(result).toEqual(mockUser);
  });
});
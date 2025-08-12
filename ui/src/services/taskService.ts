import { Task } from '../types';
import * as authService from './authService';

const API_URL = 'http://localhost:8000/tasks/';

const getAuthHeaders = () => {
  const token = authService.getToken();
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const getTasks = async (): Promise<Task[]> => {
  const response = await fetch(API_URL, { headers: getAuthHeaders() });
  if (response.status === 401) {
    authService.logout();
    window.location.href = '/login';
    return [];
  }
  return response.json();
};

export const createTask = async (title: string, description: string): Promise<Task> => {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ title, description }),
  });
  return response.json();
};

export const updateTask = async (id: number, is_completed: boolean): Promise<Task> => {
  const response = await fetch(`${API_URL}${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify({ is_completed }),
  });
  return response.json();
};

export const deleteTask = async (id: number): Promise<void> => {
  await fetch(`${API_URL}${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
};
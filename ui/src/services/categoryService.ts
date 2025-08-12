import { Category } from '../types';
import * as authService from './authService';

const API_URL = 'http://localhost:8000/categories/';

const getAuthHeaders = () => {
  const token = authService.getToken();
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const getCategories = async (): Promise<Category[]> => {
  const response = await fetch(API_URL, { headers: getAuthHeaders() });
  return response.json();
};

export const createCategory = async (name: string): Promise<Category> => {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ name }),
  });
  return response.json();
};

export const deleteCategory = async (id: number): Promise<void> => {
  await fetch(`${API_URL}${id}/`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });
};
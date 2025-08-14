import { getToken } from "./authService";

const api_url = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const getCategories = async () => {
        const token = getToken();
        const response = await fetch(`${api_url}/categories`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Failed to fetch categories');
        return response.json();
    }

export const createCategory = async (name: string) => {
        const token = getToken();
        const response = await fetch(`${api_url}/categories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name })
        });
        if (!response.ok) throw new Error('Failed to create category');
        return response.json();
    }

export const updateCategory = async (id: number, name: string) => {
        const token = getToken();
        const response = await fetch(`${api_url}/categories/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name })
        });
        if (!response.ok) throw new Error('Failed to update category');
        return response.json();
    }

export const deleteCategory = async (id: number) => {
        const token = getToken();
        const response = await fetch(`${api_url}/categories/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Failed to delete category');
        return response.json();
    }
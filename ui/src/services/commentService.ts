import { getToken } from "./authService";

const api_url = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const commentService = {
    async getComments(taskId: string) {
        const token = getToken();
        const response = await fetch(`${api_url}/tasks/${taskId}/comments`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) {
            throw new Error('Failed to fetch comments');
        }
        return response.json();
    },

    async addComment(taskId: string, content: string) {
        const token = getToken();
        const response = await fetch(`${api_url}/tasks/${taskId}/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ content })
        });
        if (!response.ok) {
            throw new Error('Failed to add comment');
        }
        return response.json();
    }
};
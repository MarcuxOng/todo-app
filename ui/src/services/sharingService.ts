import { getToken } from "./authService";

const api_url = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const sharingService = {
    async shareTask(taskId: string, userId: string) {
        const token = getToken();
        const response = await fetch(`${api_url}/tasks/${taskId}/share`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ user_id: userId })
        });
        if (!response.ok) {
            throw new Error('Failed to share task');
        }
        return response.json();
    }
};
import { getToken } from "./authService";

const api_url = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const workspaceService = {
    async getWorkspaces() {
        const token = getToken();
        const response = await fetch(`${api_url}/workspaces`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) {
            throw new Error('Failed to fetch workspaces');
        }
        return response.json();
    },

    async createWorkspace(name: string) {
        const token = getToken();
        const response = await fetch(`${api_url}/workspaces`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name })
        });
        if (!response.ok) {
            throw new Error('Failed to create workspace');
        }
        return response.json();
    }
};
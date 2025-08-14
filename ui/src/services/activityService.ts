import { getToken } from "./authService";

const api_url = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const activityService = {
    async getActivities() {
        const token = getToken();
        const response = await fetch(`${api_url}/activities`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) {
            throw new Error('Failed to fetch activities');
        }
        return response.json();
    }
};
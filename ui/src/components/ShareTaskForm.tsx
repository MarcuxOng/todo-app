import React, { useState } from 'react';
import { sharingService } from '../services/sharingService';

interface ShareTaskFormProps {
    taskId: string;
    onTaskShared: () => void;
}

const ShareTaskForm: React.FC<ShareTaskFormProps> = ({ taskId, onTaskShared }) => {
    const [userId, setUserId] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!userId.trim()) return;
        try {
            await sharingService.shareTask(taskId, userId);
            setUserId('');
            onTaskShared();
        } catch (error) {
            console.error('Failed to share task:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter user ID to share with"
            />
            <button type="submit">Share Task</button>
        </form>
    );
};

export default ShareTaskForm;
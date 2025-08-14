import React, { useState, useEffect } from 'react';
import { activityService } from '../services/activityService';
import { IActivity } from '../types';

const ActivityPage: React.FC = () => {
    const [activities, setActivities] = useState<IActivity[]>([]);

    useEffect(() => {
        fetchActivities();
    }, []);

    const fetchActivities = async () => {
        try {
            const fetchedActivities = await activityService.getActivities();
            setActivities(fetchedActivities);
        } catch (error) {
            console.error('Failed to fetch activities:', error);
        }
    };

    return (
        <div>
            <h2>Activity Log</h2>
            <ul>
                {activities.map(activity => (
                    <li key={activity.id}>
                        {activity.description} - {new Date(activity.created_at).toLocaleString()}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ActivityPage;
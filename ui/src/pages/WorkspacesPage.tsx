import React, { useState, useEffect } from 'react';
import { workspaceService } from '../services/workspaceService';
import { IWorkspace } from '../types';

const WorkspacesPage: React.FC = () => {
    const [workspaces, setWorkspaces] = useState<IWorkspace[]>([]);
    const [newWorkspaceName, setNewWorkspaceName] = useState('');

    useEffect(() => {
        fetchWorkspaces();
    }, []);

    const fetchWorkspaces = async () => {
        try {
            const fetchedWorkspaces = await workspaceService.getWorkspaces();
            setWorkspaces(fetchedWorkspaces);
        } catch (error) {
            console.error('Failed to fetch workspaces:', error);
        }
    };

    const handleCreateWorkspace = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newWorkspaceName.trim()) return;
        try {
            await workspaceService.createWorkspace(newWorkspaceName);
            setNewWorkspaceName('');
            fetchWorkspaces();
        } catch (error) {
            console.error('Failed to create workspace:', error);
        }
    };

    return (
        <div>
            <h2>Workspaces</h2>
            <ul>
                {workspaces.map(workspace => (
                    <li key={workspace.id}>{workspace.name}</li>
                ))}
            </ul>
            <form onSubmit={handleCreateWorkspace}>
                <input
                    type="text"
                    value={newWorkspaceName}
                    onChange={(e) => setNewWorkspaceName(e.target.value)}
                    placeholder="New workspace name"
                />
                <button type="submit">Create Workspace</button>
            </form>
        </div>
    );
};

export default WorkspacesPage;
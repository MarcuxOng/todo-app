import React, { useState } from 'react';
import { commentService } from '../services/commentService';

interface AddCommentFormProps {
    taskId: string;
    onCommentAdded: () => void;
}

const AddCommentForm: React.FC<AddCommentFormProps> = ({ taskId, onCommentAdded }) => {
    const [content, setContent] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!content.trim()) return;
        try {
            await commentService.addComment(taskId, content);
            setContent('');
            onCommentAdded();
        } catch (error) {
            console.error('Failed to add comment:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Add a comment"
            />
            <button type="submit">Add Comment</button>
        </form>
    );
};

export default AddCommentForm;
import React from 'react';
import { IComment } from '../types';

interface CommentListProps {
    comments: IComment[];
}

const CommentList: React.FC<CommentListProps> = ({ comments }) => {
    return (
        <div>
            {comments.map(comment => (
                <div key={comment.id}>
                    <p>{comment.content}</p>
                    <span>By: {comment.owner.username}</span>
                </div>
            ))}
        </div>
    );
};

export default CommentList;
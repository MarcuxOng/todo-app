import React, { useState, useEffect } from 'react';
import './TodoList.css';
import { Task, IComment } from '../types';
import { commentService } from '../services/commentService';
import CommentList from './CommentList';
import AddCommentForm from './AddCommentForm';
import ShareTaskForm from './ShareTaskForm';

interface TodoItemProps {
  task: Task;
  onUpdateTask: (id: number, is_completed: boolean) => void;
  onDeleteTask: (id: number) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ task, onUpdateTask, onDeleteTask }) => {
  const [comments, setComments] = useState<IComment[]>([]);
  const [showComments, setShowComments] = useState(false);

  const fetchComments = async () => {
    if (showComments) {
        try {
            const fetchedComments = await commentService.getComments(task.id.toString());
            setComments(fetchedComments);
        } catch (error) {
            console.error('Failed to fetch comments:', error);
        }
    }
  };

  useEffect(() => {
    fetchComments();
  }, [showComments]);

  const handleToggleComments = () => {
    setShowComments(!showComments);
  };

  const handleCommentAdded = () => {
    fetchComments();
  };

  return (
    <div className={`todo-item ${task.is_completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        checked={task.is_completed}
        onChange={(e) => onUpdateTask(task.id, e.target.checked)}
      />
      <span>{task.title}</span>
      <button onClick={() => onDeleteTask(task.id)}>Delete</button>
      <button onClick={handleToggleComments}>
        {showComments ? 'Hide' : 'Show'} Comments
      </button>
      {showComments && (
        <div>
          <CommentList comments={comments} />
          <AddCommentForm taskId={task.id.toString()} onCommentAdded={handleCommentAdded} />
          <ShareTaskForm taskId={task.id.toString()} onTaskShared={() => {
            console.log('Task shared successfully');
          }} />
        </div>
      )}
    </div>
  );
};

export default TodoItem;
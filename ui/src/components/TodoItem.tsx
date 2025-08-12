import React from 'react';
import './TodoList.css';
import { Task } from '../types';

interface TodoItemProps {
  task: Task;
  onUpdateTask: (id: number, is_completed: boolean) => void;
  onDeleteTask: (id: number) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ task, onUpdateTask, onDeleteTask }) => {
  return (
    <div className={`todo-item ${task.is_completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        checked={task.is_completed}
        onChange={(e) => onUpdateTask(task.id, e.target.checked)}
      />
      <span>{task.title}</span>
      <button onClick={() => onDeleteTask(task.id)}>Delete</button>
    </div>
  );
};

export default TodoItem;
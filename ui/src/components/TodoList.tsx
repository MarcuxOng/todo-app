import React from 'react';
import { Task } from '../types';
import TodoItem from './TodoItem';

interface TodoListProps {
  tasks: Task[] | undefined | null; // make prop more flexible
  onUpdateTask: (id: number, is_completed: boolean) => void;
  onDeleteTask: (id: number) => void;
}

const TodoList: React.FC<TodoListProps> = ({ tasks, onUpdateTask, onDeleteTask }) => {
  if (!Array.isArray(tasks)) {
    return <p>No tasks to display.</p>; // fallback rendering
  }

  return (
    <div>
      {tasks.map((task) => (
        <TodoItem
          key={task.id}
          task={task}
          onUpdateTask={onUpdateTask}
          onDeleteTask={onDeleteTask}
        />
      ))}
    </div>
  );
};

export default TodoList;

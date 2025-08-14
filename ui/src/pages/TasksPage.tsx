import { useState, useEffect } from 'react';
import TodoList from '../components/TodoList';
import AddTodoForm from '../components/AddTodoForm';
import { Task } from '../types';
import * as taskService from '../services/taskService';
import { websocketService } from '../services/websocketService';

const TasksPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);

  const fetchTasks = async () => {
    const fetchedTasks = await taskService.getTasks();
    setTasks(fetchedTasks);
  };

  useEffect(() => {
    fetchTasks();

    websocketService.onMessage((data) => {
      if (data.type === 'task_update') {
        fetchTasks();
      }
    });
  }, []);

  const handleAddTask = async (title: string, description: string) => {
    const newTask = await taskService.createTask(title, description);
    setTasks([...tasks, newTask]);
  };

  const handleUpdateTask = async (id: number, is_completed: boolean) => {
    const updatedTask = await taskService.updateTask(id, is_completed);
    setTasks(tasks.map(task => task.id === id ? updatedTask : task));
  };

  const handleDeleteTask = async (id: number) => {
    await taskService.deleteTask(id);
    setTasks(tasks.filter(task => task.id !== id));
  };

  return (
    <div className="tasks-page">
      <AddTodoForm onAddTask={handleAddTask} />
      <TodoList 
        tasks={tasks}
        onUpdateTask={handleUpdateTask}
        onDeleteTask={handleDeleteTask}
      />
    </div>
  );
};

export default TasksPage;
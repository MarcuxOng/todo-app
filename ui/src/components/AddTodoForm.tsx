import React, { useState } from 'react';
import './AddTodoForm.css';

interface AddTodoFormProps {
  onAddTask: (title: string, description: string) => void;
}

const AddTodoForm: React.FC<AddTodoFormProps> = ({ onAddTask }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onAddTask(title, description);
    setTitle('');
    setDescription('');
  };

  return (
    <div className="add-todo-form">
      <form onSubmit={handleSubmit} className="form-container">
        <div className="input-group">
          <div className="input-field">
            <input
              type="text"
              placeholder="Enter task title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="title-input"
            />
          </div>
          
          <div className="input-field">
            <textarea
              placeholder="Task Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="description-textarea"
              rows={4}
            />
          </div>
        </div>
        
        <div className="button-container">
          <button type="submit" className="add-button">
            Add Task
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddTodoForm;
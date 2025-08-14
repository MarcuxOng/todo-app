import React, { useState } from 'react';
import { Category } from '../types';
import {
  updateCategory,
  deleteCategory
} from '../services/categoryService';

interface CategoryItemProps {
  category: Category;
  onSelectCategory: (id: number) => void;
  onDelete: (id: number) => void;
  onUpdate: (updatedCategory: Category) => void;
}

const CategoryItem: React.FC<CategoryItemProps> = ({ category, onSelectCategory, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(category.name);

  const handleUpdate = async () => {
    try {
      const updatedCategory = await updateCategory(category.id, name);
      onSelectCategory(updatedCategory.id); // Refresh category selection
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update category:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this category?')) {
      try {
        await deleteCategory(category.id);
        onDelete(category.id);
      } catch (error) {
        console.error('Failed to delete category:', error);
      }
    }
  };

  return (
    <div className="category-item">
      {isEditing ? (
        <>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <button onClick={handleUpdate}>Save</button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
        </>
      ) : (
        <>
          <span onClick={() => onSelectCategory(category.id)}>
            {category.name}
          </span>
          <button onClick={() => setIsEditing(true)}>Edit</button>
          <button onClick={handleDelete}>Delete</button>
        </>
      )}
    </div>
  );
};

export default CategoryItem;
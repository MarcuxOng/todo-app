import React, { useState, useEffect } from 'react';
import { Category } from '../types';
import CategoryItem from './CategoryItem';
import {
  getCategories,
  deleteCategory
} from '../services/categoryService';

interface CategoryListProps {
  categories: Category[];
  onSelectCategory: (id: number) => void;
  onDelete: (id: number) => void;
}

const CategoryList: React.FC<CategoryListProps> = ({ onSelectCategory }) => {
  const [categories, setCategories] = useState<Category[]>([]);

  const fetchCategories = async () => {
    try {
      const fetchedCategories = await getCategories();
      setCategories(fetchedCategories);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await deleteCategory(id);
      setCategories(categories.filter(cat => cat.id !== id));
    } catch (error) {
      console.error('Failed to delete category:', error);
    }
  };

  const handleUpdate = (updatedCategory: Category) => {
    setCategories(categories.map(cat =>
      cat.id === updatedCategory.id ? updatedCategory : cat
    ));
  };

  return (
    <div>
      <h3>Categories</h3>
      {categories.map(category => (
        <CategoryItem
          key={category.id}
          category={category}
          onSelectCategory={onSelectCategory}
          onDelete={handleDelete}
          onUpdate={handleUpdate}
        />
      ))}
    </div>
  );
};

export default CategoryList;
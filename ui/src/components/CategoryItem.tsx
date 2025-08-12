import React from 'react';
import { Category } from '../types';

interface CategoryItemProps {
  category: Category;
  onSelectCategory: (id: number) => void;
  onDeleteCategory: (id: number) => void;
}

const CategoryItem: React.FC<CategoryItemProps> = ({ category, onSelectCategory, onDeleteCategory }) => {
  return (
    <div>
      <span onClick={() => onSelectCategory(category.id)}>
        {category.name}
      </span>
      <button onClick={() => onDeleteCategory(category.id)}>Delete</button>
    </div>
  );
};

export default CategoryItem;
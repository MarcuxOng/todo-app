import React from 'react';
import { Category } from '../types';
import CategoryItem from './CategoryItem';

interface CategoryListProps {
  categories: Category[];
  onSelectCategory: (id: number) => void;
  onDeleteCategory: (id: number) => void;
}

const CategoryList: React.FC<CategoryListProps> = ({ categories, onSelectCategory, onDeleteCategory }) => {
  return (
    <div>
      <h3>Categories</h3>
      {categories.map((category) => (
        <CategoryItem
          key={category.id}
          category={category}
          onSelectCategory={onSelectCategory}
          onDeleteCategory={onDeleteCategory}
        />
      ))}
    </div>
  );
};

export default CategoryList;
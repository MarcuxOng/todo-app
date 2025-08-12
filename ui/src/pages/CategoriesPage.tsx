import { useState, useEffect } from 'react';
import CategoryList from '../components/CategoryList';
import AddCategoryForm from '../components/AddCategoryForm';
import { Category } from '../types';
import * as categoryService from '../services/categoryService';

const CategoriesPage = () => {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    const fetchCategories = async () => {
      const fetchedCategories = await categoryService.getCategories();
      setCategories(fetchedCategories);
    };
    fetchCategories();
  }, []);

  const handleAddCategory = async (name: string) => {
    const newCategory = await categoryService.createCategory(name);
    setCategories([...categories, newCategory]);
  };

  const handleDeleteCategory = async (id: number) => {
    await categoryService.deleteCategory(id);
    setCategories(categories.filter(category => category.id !== id));
  };

  const handleSelectCategory = (id: number) => {
    // TODO: Implement category selection logic
    console.log('Selected category:', id);
  };

  return (
    <div className="categories-page">
      <AddCategoryForm onAddCategory={handleAddCategory} />
      <CategoryList
        categories={categories}
        onDeleteCategory={handleDeleteCategory}
        onSelectCategory={handleSelectCategory}
      />
    </div>
  );
};

export default CategoriesPage;
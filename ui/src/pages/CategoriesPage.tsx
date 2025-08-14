import { useState, useEffect } from 'react';
import CategoryList from '../components/CategoryList';
import AddCategoryForm from '../components/AddCategoryForm';
import { Category } from '../types';
import {
  getCategories,
  createCategory,
  deleteCategory
} from '../services/categoryService';

const CategoriesPage = () => {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    const fetchCategories = async () => {
      const fetchedCategories = await getCategories();
      setCategories(fetchedCategories);
    };
    fetchCategories();
  }, []);

  const handleAddCategory = async (name: string) => {
    const newCategory = await createCategory(name);
    setCategories([...categories, newCategory]);
  };

  const handleDeleteCategory = async (id: number) => {
    await deleteCategory(id);
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
        onDelete={handleDeleteCategory}
        onSelectCategory={handleSelectCategory}
      />
    </div>
  );
};

export default CategoriesPage;
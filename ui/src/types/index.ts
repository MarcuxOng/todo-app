export interface Category {
  id: number;
  name: string;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  due_date: string | null;
  categories: Category[];
}
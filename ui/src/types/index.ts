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

export interface IUser {
    id: number;
    username: string;
}

export interface IComment {
    id: number;
    content: string;
    owner: IUser;
}

export interface IWorkspace {
    id: number;
    name: string;
}

export interface IActivity {
    id: number;
    description: string;
    created_at: string;
}
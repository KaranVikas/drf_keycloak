export interface Todo {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTodoRequest {
  title: string;
  description?: string;
}

export interface UpdateTodoRequest {
  title?:  string;
  description?: string;
  completed?: boolean;
}

export interface TodosResponse {
  count: number;
  results: Todo[];
}

export interface ApiRequestOptions {
  method?: string;
  headers?: Record<string,string>;
  body?: any;
}

export interface RegisterUserData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  name?: string;
}

export interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  name: string;
}

export interface RegisterFormProps {
  onSuccess?: () => void;
  onCancel?: () =>  void;
}

export interface User {
  id: number;
  username: string;
  email: string;
  name?: string;
  url?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}
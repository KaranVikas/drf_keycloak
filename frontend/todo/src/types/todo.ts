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
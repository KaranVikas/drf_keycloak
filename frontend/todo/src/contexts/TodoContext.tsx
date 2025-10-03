import React, {createContext, useContext, useState, useEffect } from 'react'
import type {CreateTodoRequest, Todo, UpdateTodoRequest} from "../types/todo";
import {apiService} from '../services/apiService';
import { useAuth } from './AuthContext';


interface TodoContextType {
  todos: Todo[];
  loading: boolean;
  error: string | null
  createTodo : (todoData: CreateTodoRequest) => Promise<void>;
  updateTodo: (id: number, todoData: UpdateTodoRequest) => Promise<void>;
  deleteTodo: (id: number ) => Promise<void>;
  toggleComplete: (id: number) => Promise<void>;
  refreshTodos: () => Promise<void>;
}

const TodoContext = createContext<TodoContextType | undefined>(undefined);

export const TodoProvider: React.FC<{children: React.ReactNode}> = ({
  children
}) => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const {authenticated} = useAuth();


  const refreshTodos = async (): Promise<void> => {
    if (!authenticated) {
      setTodos([])
      return;
    }


    setLoading(true);
    setError(null);

    try {
      const response = await apiService.getTodos();
      setTodos(response.results);
    } catch (err: any) {
      setError( err.response?.data?.detail || 'Failed to fetch todos');
      console.error('Error fetching todos: ', err);
    }
    finally{
      setLoading(false);
    }
  };

  const createTodo = async(todoData: CreateTodoRequest): Promise<void> => {
    setError(null);

    try{
      const newTodo = await apiService.createTodo(todoData);
      setTodos(prev => [newTodo, ...prev]);
    } catch(err: any){
      setError(err.response?.data?.detail || 'Failed to create todo');
      throw err;
    }
  };

  const updateTodo = async(id: number, todoData: UpdateTodoRequest): Promise<void> => {
    setError(null);

    try {
      const updatedTodo = await apiService.updateTodo(id, todoData);
      setTodos(prev => prev.map(todo => todo.id === id ? updatedTodo : todo));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update data');
      throw err;
    }
  }
  const deleteTodo = async(id: number): Promise<void> => {
    setError(null)
    try{
      await apiService.deleteTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
    } catch (err: any){
      setError(err.response?.data?.detail || 'Failed to delete todo');
      throw err;
    }
  }

  const toggleComplete = async(id: number): Promise<void> => {
    const todo = todos.find(t => t.id === id);
    if(!todo) return;

    await updateTodo(id, {completed: !todo.completed});
  }

  useEffect(()=> {
    if(authenticated) {
      refreshTodos();
    }else {
        setTodos([]);
      }

  },[authenticated]);

  return (
      <TodoContext.Provider value={{todos, loading, error, createTodo, updateTodo, deleteTodo, toggleComplete, refreshTodos}}>
        {children}
      </TodoContext.Provider>
  )
}

export const useTodos = (): TodoContextType => {
  const context = useContext(TodoContext);
  if (context === undefined) {
    throw new Error('useTodos must be used within a TodoProvider')
  }
  return context;
}
import React, {useState, useEffect} from 'react';
import {apiService} from '../services/apiService';
import {useAuth} from '../contexts/AuthContext';

interface Todo {
  id: string;
  title: string;
  completed: boolean;
  created_at: string;
}

const TodoApp: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const {user} = useAuth();

  useEffect(() => {
    fetchTodos();
  }, []);


  const fetchTodos = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getTodos();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos: ', error);
      setError('Failed to fetch todos');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;

    try {
      const newTodo = await apiService.createTodo({
        title: newTodoTitle,
        completed: false,
      })
      setTodos([...todos, newTodo]);
      setNewTodoTitle('');
    } catch (error) {
      console.error(`Error creating todo: `, error);
      setError('Failed to create todo ');
    }
  };

  const handleToggleTodo = async (todo: Todo) => {
    try {
      const updatedTodo = await apiService.updateTodo.id, {
        ...todo,
        completed:
      !todo.completed,
    }
      setTodos(todos.map(t => t.id === toid.id ? updatedTodo : t));
    } catch (error) {
      console.error('Error updating todo:', error);
      setError('Failed to update todo');
    }
  };

  const handleDeleteTodo = async (todoId: string) => {
    try {
      await apiService.deleteTodo(todoId);
      setTodos(todos.filter(t => t.id !== todoId));
    } catch (error) {
      console.error('Error deleting todo', error);
      setError('Failed to delete todo');
    }
  };

  if (loading) {
    return <div className={"text-center"}>Loading todos..</div>
  }
  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">
          Hello, {user?.preferred_username || 'User'}!
        </h2>

        {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
        )}

        {/* Add new todo */}
        <form onSubmit={handleCreateTodo} className="mb-6">
          <div className="flex gap-2">
            <input
                type="text"
                value={newTodoTitle}
                onChange={(e) => setNewTodoTitle(e.target.value)}
                placeholder="Enter a new todo..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
                type="submit"
                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Add Todo
            </button>
          </div>
        </form>

        {/* Todo list */}
        <div className="space-y-2">
          {todos.length === 0 ? (
              <p className="text-gray-500 text-center py-4">
                No todos yet. Add one above!
              </p>
          ) : (
              todos.map((todo) => (
                <div
                    key={todo.id}
                    className="flex items-center justify-between p-3 border border-gray-200 rounded-md"
                >
                  <div className="flex items-center gap-3">
                    <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => handleToggleTodo(todo)}
                        className="h-4 w-4 text-blue-600"
                    />
                    <span
                        className={`${
                            todo.completed
                                ? 'line-through text-gray-500'
                                : 'text-gray-900'
                        }`}
                    >
                                    {todo.title}
                                </span>
                  </div>
                  <button
                      onClick={() => handleDeleteTodo(todo.id)}
                      className="text-red-500 hover:text-red-700"
                  >
                    Delete
                  </button>
                </div>
              ))
          )}
        </div>
      </div>
    </div>
  );

}
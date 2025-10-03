import React from 'react';
import { useTodos } from '../contexts/TodoContext';
import TodoItem from './TodoItem';
import CreateTodoForm from './CreateTodoForm';

const TodoList: React.FC = () => {
  const { todos, loading, error, refreshTodos } = useTodos();

  if (loading && todos.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading todos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">My Todos</h1>
        <p className="text-gray-600">
          {todos.length === 0
            ? 'No todos yet. Create your first one below!'
            : `${todos.filter(t => !t.completed).length} pending, ${todos.filter(t => t.completed).length} completed`
          }
        </p>
      </div>

      <CreateTodoForm />

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-center justify-between">
            <p className="text-red-800">{error}</p>
            <button
              onClick={refreshTodos}
              className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600 transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {todos.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4"></div>
            <p className="text-gray-500 text-lg">No todos yet</p>
            <p className="text-gray-400">Create your first todo above to get started!</p>
          </div>
        ) : (
          todos.map((todo) => (
            <TodoItem key={todo.id} todo={todo} />
          ))
        )}
      </div>

      {todos.length > 0 && (
        <div className="mt-8 text-center">
          <button
            onClick={refreshTodos}
            disabled={loading}
            className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 disabled:bg-gray-300 transition-colors"
          >
            {loading ? 'Refreshing...' : 'Refresh Todos'}
          </button>
        </div>
      )}
    </div>
  );
};

export default TodoList;
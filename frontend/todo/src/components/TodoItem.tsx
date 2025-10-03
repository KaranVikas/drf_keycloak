import React, { useState } from 'react';
import type { Todo, UpdateTodoRequest} from '../types/todo';
import { useTodos } from '../contexts/TodoContext';

interface TodoItemProps {
  todo: Todo
}

const TodoItem: React.FC<TodoItemProps> = ({todo}) => {
  const { updateTodo, deleteTodo, toggleComplete } = useTodos();
  const [ isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description);
  const [isLoading, setIsLoading] = useState(false);

  const handleToggleComplete = async (): Promise<void> => {
    setIsLoading(true);
    try{
    await toggleComplete(todo.id);
  } catch(error) {
    console.log('Failed to toggle complete:',error);
  }  finally {
    setIsLoading(false);
  }
  }


  const handleSaveEdit = async (): Promise<void> => {
    if(!editTitle.trim()) return;

    setIsLoading(true);
    try{
      const updateData: UpdateTodoRequest = {
        title: editTitle.trim(),
        description: editDescription.trim(),
      };
      await updateTodo(todo.id, updateData);
      setIsEditing(false);
    } catch(error){
      console.log('Failed to update todo: ',error);
    } finally {
      setIsLoading(false)
    }
  };

  const handleDelete = async ():Promise<void> => {
    if(!window.confirm('Are you sure you want to delete this  todo?')) return;

    setIsLoading(true);
    try{
      await deleteTodo(todo.id);
    } catch (error) {
      console.error('Failed to delete todo', error);
      setIsLoading(false)
    }
  }

  const handleCancelEdit = (): void => {
    setEditTitle(todo.title);
    setEditDescription(todo.description);
    setIsEditing(false);
  }

  if(isEditing){
    return(
        <div className="">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className=""
            placeholder="Todo title..."
            disabled={isLoading}
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className=""
            placeholder="Description (optional)... "
            rows={2}
            disabled={isLoading}
          />
          <div className="flex space-x-2">
            <button
              onClick={handleSaveEdit}
              disabled={isLoading || !editTitle.trim() }
              className="px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600 disabled:bg-gray-300 transition-colors"
            >
              {isLoading ? '...' : 'Save'}
            </button>
             <button
              onClick={handleCancelEdit}
              disabled={isLoading}
              className="px-3 py-1 bg-gray-500 text-white rounded text-sm hover:bg-gray-600 disabled:bg-gray-300 transition-colors"
            >
            Cancel
             </button>
          </div>
        </div>
    )
  }
  return(
      <div className={""}>
        <div className={""}>
          <button
            onClick={handleToggleComplete}
            disabled={isLoading}
            className={`mt-1 w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors ${
            todo.completed 
              ? 'bg-green-500 border-green-500 text-white' 
              : 'border-gray-300 hover:border-green-400'
          }`}

          >
            {todo.completed && '✓'}
          </button>

          <div className="flex=1">
            <h3 className={`font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
            {todo.title}
            </h3>
          {todo.description && (
            <p className={`text-sm mt-1 ${todo.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
              {todo.description}
            </p>
          )}
          <p className="text-xs text-gray-400 mt-2">
            Created: {new Date(todo.created_at).toLocaleDateString()}
          </p>

          </div>

          <div className="flex space-x-2">
          <button
            onClick={() => setIsEditing(true)}
            disabled={isLoading}
            className="px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300 transition-colors"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            disabled={isLoading}
            className="px-2 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600 disabled:bg-gray-300 transition-colors"
          >
            Delete
          </button>
        </div>

        </div>
      </div>
  )
};

export default TodoItem;
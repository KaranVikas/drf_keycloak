import React from 'react';
import { useAuth } from '../contexts/AuthContext.tsx';

const AuthButton: React.FC = () => {
  const { authenticated, user, login, logout } = useAuth();

  if (authenticated){
    return (
      <div className="flex items-center space-x-4">
        <span className="text-sm text-gray-600">
          Welcome, {user?.preferred_username || user?.name || 'User'}
        </span>
        <button
          onClick={logout}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
          >
          Logout
        </button>
      </div>
    );
  }
  return(
      <button
        onClick={login}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      >
        Login
      </button>
  )
};

export default AuthButton;

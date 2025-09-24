import React, {ReactNode} from 'react'
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
  roles?: string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, roles }) => {
  const { authenticated, loading, login, hasRole } = useAuth();

  if (loading){
    return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-lg">Loading...</div>
        </div>
    );
  }

  if(!authenticated){
    return(
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <h2 className="text-xl mb-4">Authentication Required</h2>
            <button onClick={login} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
              Login
            </button>
          </div>
        </div>
    )
  }

//   Check if user has requried roles
  if(roles && roles.length > 0){
    const hasRequiredRole = roles.some(role => hasRole(role));
    if(!hasRequiredRole){
      return(
          <div className="flex items-center justify-center min-h-screen">
            <div className="text-center text-red-500">
              <h2 className="text-xl mb-4">Access Denied</h2>
              <p>You don;t have permissions to access this page.</p>
            </div>
          </div>
      )
    }
  }
}
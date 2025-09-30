import React, {ReactNode} from 'react'
import { useAuth } from '../contexts/AuthContext.tsx';

interface ProtectedRouteProps {
  children: ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { authenticated, loading, login } = useAuth();

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

  return <>{children}</>
}

export default ProtectedRoute;
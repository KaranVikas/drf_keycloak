import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { userService } from '../services/userService';
import TodoList from './TodoList';
import keycloak from '../keycloak';

const TodoApp: React.FC = () => {
  const { authenticated, loading, login, logout, user } = useAuth();
  const [userData, setUserData] = useState(null);
  const [apiLoading, setApiLoading] = useState(false);


  useEffect(() => {
    if (authenticated && !userData) {
      fetchUserData();
    }
  }, [authenticated]);

  const fetchUserData = async () => {
    setApiLoading(true);
    try {
      const data = await userService.getMe();
      setUserData(data);
      console.log('API Response:', data);
    } catch (error) {
      console.error('API Error:', error);
    } finally {
      setApiLoading(false);
    }
  };

  // useEffect(() => {
  // let cancelled = false;

  // const fetchData = async () => {
  //   if (authenticated && !userData && !apiLoading) {
  //     setApiLoading(true);
  //     try {
  //       const data = await userService.getMe();
  //       if (!cancelled) { // Prevent state update if component unmounted
  //         setUserData(data);
  //       }
  //     } catch (error) {
  //       if (!cancelled) {
  //         console.error('API Error:', error);
  //       }
  //     } finally {
  //       if (!cancelled) {
  //         setApiLoading(false);
  //       }
  //     }
  //   }
  // };
  //
  // fetchData();
  //
  //   return () => {
  //     cancelled = true; // Cleanup function
  //   };
  // }, [authenticated]);


  const handleRegister = () => {
    keycloak.register();

  };

  if (loading) {
    return <div>Loading authentication...</div>;
  }

  if (!authenticated) {
    return (
      <div>
        <h1>Todo App</h1>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '200px' }}>
          <button onClick={login}>Login with Keycloak</button>
          <button onClick={handleRegister}>Register with Keycloak</button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h1>Welcome to Todo App</h1>
          <p>User: {user?.preferred_username}</p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          {/*/*/}
          {/*<button*/}
          {/*  onClick={logout}*/}
          {/*  style={{*/}
          {/*    padding: '8px 16px',*/}
          {/*    backgroundColor: '#dc3545',*/}
          {/*    color: 'white',*/}
          {/*    border: 'none',*/}
          {/*    borderRadius: '4px'*/}
          {/*  }}*/}
          {/*>*/}
          {/*  Logout*/}
          {/*</button>*/}
        </div>
      </div>

      {apiLoading ? (
        <p>Loading user data...</p>
      ) : (
        <>
          <div>
            <h2>API Test</h2>
            <button onClick={fetchUserData}>Refresh User Data</button>
            {userData && (
              <pre className="text-xs overflow-auto">
                {JSON.stringify(userData, null, 2)}
              </pre>
            )}
          </div>
          <TodoList />
        </>
      )}
    </div>
  );
};

export default TodoApp;
import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { userService } from '../services/userService';
import TodoList from './TodoList';
import RegisterForm from './RegisterForm';

const TodoApp: React.FC = () => {
  const { authenticated, loading, login, logout, user } = useAuth();
  const [userData, setUserData] = useState(null);
  const [apiLoading, setApiLoading] = useState(false);
  const [showRegistration, setShowRegistration] = useState(false);

  useEffect(() => {
    if (authenticated) {
      fetchUserData();
    }
  }, [authenticated]);

  const fetchUserData = async () => {
    setApiLoading(true);
    console.log("inside authButton ")
    try {
      const data = await userService.getMe();
      console.log("getme user")
      setUserData(data);
      console.log('API Response:', data);
    } catch (error) {
      console.error('API Error:', error);
    } finally {
      setApiLoading(false);
    }
  };

  if(loading) {
    return <div>Loading authentication...</div>;
  }

  if (!authenticated) {
    return (
      <>
      <div>
        <h1>Todo App</h1>
        <button onClick={login}>Login with Keycloak</button>
        <span>or</span>
        <button onClick={() => setShowRegistration(true)}>Register</button>



      </div>
        {
        showRegistration && (
          <RegisterForm
              onSuccess={() => {
                setShowRegistration(false);
              }}
              onCancel={() => setShowRegistration(false)}
          ></RegisterForm>
        )
      }
      </>
    );
  }

  return (
    <div>
      <h1>Welcome to Todo App</h1>
      <p>User: {user?.preferred_username}</p>
      <button onClick={logout}>Logout</button>

      {apiLoading ? (
        <p>Loading user data...</p>
      ) : (
          <>
            <div>
              <h2>API Test</h2>
              {/*<pre>{JSON.stringify(userData, null, 2)}</pre>*/}
              <button onClick={fetchUserData}>Refresh User Data</button>
              {userData && (
                  <pre className="text-xs overflow-auto">
                              {JSON.stringify(userData, null, 2)}
                          </pre>
              )}
            </div>
            <TodoList/></>
      )}
    </div>
  );
};

export default TodoApp;
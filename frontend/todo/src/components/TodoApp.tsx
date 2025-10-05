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
    if (authenticated) {
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

  const handleSyncUser = async () => {
    if (!authenticated) return;

    setApiLoading(true);
    try {
      const data = await userService.syncKeycloakUser();
      setUserData(data);
      console.log('User synced:', data);
    } catch (error) {
      console.error('Sync error:', error);
    } finally {
      setApiLoading(false);
    }
  };

  const handleRegister = () => {
    keycloak.register();

    // Redirect to Keycloak registration page
  //   console.log('Keycloak Config:', {
  //     authServerUrl: keycloak.authServerUrl,
  //     realm: keycloak.realm,
  //     clientId: keycloak.clientId,
  //     // configured: keycloak.configured
  // });
  //
  //   if (!keycloak.authServerUrl || !keycloak.realm || !keycloak.clientId) {
  //   console.error('Keycloak not properly configured');
  //   alert('Registration not available - Keycloak configuration missing');
  //   return;
  // }
  //
  //   const registrationKeycloakUrl = `${keycloak.authServerUrl}/realms/${keycloak.realm}/protocol/openid-connect/registrations?client_id=${keycloak.clientId}&response_type=code&redirect_uri=${encodeURIComponent(window.location.origin)}`;
  //   console.log("registration Keycloak Url")
  //   window.location.href = registrationKeycloakUrl;
  //   // Test if registration is enabled by making a simple request first
  // fetch(registrationKeycloakUrl)
  //   .then(response => {
  //     if (response.ok || response.status === 302) {
  //       // Registration page exists, redirect
  //       window.location.href = registrationKeycloakUrl;
  //     } else {
  //       console.error('Registration not available, status:', response.status);
  //       alert('User registration is not enabled in Keycloak. Please contact your administrator.');
  //     }
  //   })
  //   .catch(error => {
  //     console.error('Registration check failed:', error);
  //     // Try anyway
  //     window.location.href = registrationKeycloakUrl;
  //   });

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
          <button
            onClick={handleSyncUser}
            disabled={apiLoading}
            style={{
              padding: '8px 16px',
              backgroundColor: apiLoading ? '#ccc' : '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: apiLoading ? 'not-allowed' : 'pointer'
            }}
          >
            {apiLoading ? 'Syncing...' : 'Sync User'}
          </button>
          <button
            onClick={logout}
            style={{
              padding: '8px 16px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px'
            }}
          >
            Logout
          </button>
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
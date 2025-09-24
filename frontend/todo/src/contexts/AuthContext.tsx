import React , {createContext, useContext, useEffect, useState, ReactNode }
import keycloak from '../keycloak.ts';

interface AuthContextType {
  authenticated: boolean;
  loading: boolean;
  token: string | null;
  user: any | null;
  login: () => void;
  logout: () => void;
  hasRole: (role: string) => boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const initKeycloak = async () => {
      try {
        const authenticated = await keycloak.init({
          onLoad: 'check-sso',
          checkLoginIframe: false,
          pkceMethod: 'S256'
        });

        setAuthenticated(authenticated);

        if (authenticated) {
          setToken(keycloak.token || null);
          setUser(keycloak.tokenParsed);

          //   Setup refresh token
          keycloak.onTokenExpired = () => {
            keycloak.updateToken(30)
                .then((refreshed) => {
                  if (refreshed) {
                    setToken(keycloak.token || null);
                    console.log('Token refreshed');
                  } else {
                    console.log('Token not refreshed');
                  }
                })
                .catch(() => {
                  console.error('Failed to refresh tokens');
                  logout();
                })
          }
        }
      } catch (error) {
        console.error('Failed to initialize keycloak: ', error);
      } finally {
        setLoading(false);
      }
    };
    initKeycloak();
  }, []);

  const login = () => {
    keycloak.login({
      redirectUri: window.location.origin
    });
  };

  const logout = () => {
    keycloak.logout({
      redirectUri: window.location.origin
    });
  };

  const hasRole = (role: string): boolean => {
    return keycloak.hasResourceRole(role) || keycloak.hasRealmRole(role);
  };

  const contextValue: AuthContextType = {
    authenticated,
    loading,
    token,
    user,
    login,
    logout,
    hasRole
  };

  return (
      <AuthContext.Provider value={contextValue}>
        {children}
      </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if(!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
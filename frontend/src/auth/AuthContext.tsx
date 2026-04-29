import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { User } from '../api/types';
import { login as apiLogin, register as apiRegister, logout as apiLogout, getCurrentUser, getToken } from '../api/auth';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAdmin: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const token = getToken();
    if (token) {
      getCurrentUser()
        .then(setUser)
        .catch(() => {
          // Token invalid, clear it
          localStorage.removeItem('token');
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (username: string, password: string) => {
    await apiLogin({ username, password });
    const user = await getCurrentUser();
    setUser(user);
  };

  const register = async (email: string, password: string) => {
    await apiRegister(email, password);
    const user = await getCurrentUser();
    setUser(user);
  };

  const logout = async () => {
    await apiLogout();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login,
        register,
        logout,
        isAdmin: user?.role === 'admin',
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

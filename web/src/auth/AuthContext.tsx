import { createContext, useContext, useMemo, useState } from 'react'
import { api } from '../api/client'

type AuthState = { token: string | null; login: (email: string, password: string) => Promise<void>; logout: () => void }
const AuthContext = createContext<AuthState>({ token: null, login: async () => {}, logout: () => {} })

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))

  const value = useMemo(() => ({
    token,
    async login(email: string, password: string) {
      const result = await api('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password, default_currency: 'USD' }) })
      localStorage.setItem('token', result.access_token)
      setToken(result.access_token)
    },
    logout() { localStorage.removeItem('token'); setToken(null) }
  }), [token])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)

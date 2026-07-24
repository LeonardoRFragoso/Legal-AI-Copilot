import api from './api'

export interface AuthUser {
  id: string
  name: string
  email: string
  role: string
  is_active: boolean
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  expires_in: number
}

function storeSession(tokens: LoginResponse, user: AuthUser) {
  localStorage.setItem('access_token', tokens.access_token)
  localStorage.setItem('refresh_token', tokens.refresh_token)
  localStorage.setItem('user', JSON.stringify(user))
}

function clearSession() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
}

export const authService = {
  async login(email: string, password: string): Promise<AuthUser> {
    const resp = await api.post<LoginResponse>('/auth/login', { email, password })
    // Fetch user info
    const userResp = await api.get<AuthUser>('/auth/me', {
      headers: { Authorization: `Bearer ${resp.data.access_token}` },
    })
    storeSession(resp.data, userResp.data)
    return userResp.data
  },

  async getCurrentUser(): Promise<AuthUser | null> {
    const token = localStorage.getItem('access_token')
    const userJson = localStorage.getItem('user')
    if (!token || !userJson) return null
    try {
      return JSON.parse(userJson) as AuthUser
    } catch {
      return null
    }
  },

  async refreshCurrentUser(): Promise<AuthUser | null> {
    const token = localStorage.getItem('access_token')
    if (!token) return null
    try {
      const resp = await api.get<AuthUser>('/auth/me')
      localStorage.setItem('user', JSON.stringify(resp.data))
      return resp.data
    } catch {
      clearSession()
      return null
    }
  },

  logout() {
    clearSession()
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token')
  },
}

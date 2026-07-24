import { create } from 'zustand'
import { authService, type AuthUser } from '../services/authService'

interface AuthState {
  user: AuthUser | null
  loading: boolean
  initialized: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  initAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: false,
  initialized: false,

  login: async (email: string, password: string) => {
    set({ loading: true })
    try {
      const user = await authService.login(email, password)
      set({ user, loading: false })
    } catch (error) {
      set({ loading: false })
      throw error
    }
  },

  logout: () => {
    authService.logout()
    set({ user: null })
  },

  initAuth: async () => {
    const user = await authService.getCurrentUser()
    if (user) {
      // Verify token is still valid
      const freshUser = await authService.refreshCurrentUser()
      set({ user: freshUser, initialized: true })
    } else {
      set({ user: null, initialized: true })
    }
  },
}))

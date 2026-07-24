import { create } from 'zustand'
import type { Document, Conversation } from '../types'

interface StoreState {
  documents: Document[]
  conversations: Conversation[]
  selectedDocument: Document | null
  selectedConversation: Conversation | null
  setDocuments: (documents: Document[]) => void
  setConversations: (conversations: Conversation[]) => void
  setSelectedDocument: (document: Document | null) => void
  setSelectedConversation: (conversation: Conversation | null) => void
}

export const useStore = create<StoreState>((set) => ({
  documents: [],
  conversations: [],
  selectedDocument: null,
  selectedConversation: null,
  setDocuments: (documents) => set({ documents }),
  setConversations: (conversations) => set({ conversations }),
  setSelectedDocument: (document) => set({ selectedDocument: document }),
  setSelectedConversation: (conversation) => set({ selectedConversation: conversation }),
}))

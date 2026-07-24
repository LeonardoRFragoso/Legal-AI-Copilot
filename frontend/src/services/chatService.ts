import api from './api'
import type { Conversation, Message } from '../types'

export const chatService = {
  async createConversation(documentId?: string, title?: string): Promise<Conversation> {
    const response = await api.post('/conversations', {
      document_id: documentId,
      title,
    })
    return response.data
  },

  async listConversations(): Promise<Conversation[]> {
    const response = await api.get('/conversations')
    return response.data
  },

  async sendMessage(conversationId: string, content: string): Promise<Message> {
    const response = await api.post(`/conversations/${conversationId}/messages`, {
      content,
    })
    return response.data
  },

  async getMessages(conversationId: string): Promise<Message[]> {
    const response = await api.get(`/conversations/${conversationId}/messages`)
    return response.data
  },
}

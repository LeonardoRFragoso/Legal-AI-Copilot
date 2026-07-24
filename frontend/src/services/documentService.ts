import api from './api'
import type { Document } from '../types'

export const documentService = {
  async upload(title: string, file: File): Promise<Document> {
    const formData = new FormData()
    formData.append('title', title)
    formData.append('file', file)
    
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async list(): Promise<Document[]> {
    const response = await api.get('/documents')
    return response.data
  },

  async get(id: string): Promise<Document> {
    const response = await api.get(`/documents/${id}`)
    return response.data
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/documents/${id}`)
  },
}

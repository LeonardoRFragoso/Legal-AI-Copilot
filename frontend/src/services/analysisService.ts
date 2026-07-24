import api from './api'
import type { ExtractionData } from '../types'

export const analysisService = {
  async generateSummary(documentId: string) {
    const response = await api.post('/analysis/summary', { document_id: documentId })
    return response.data
  },

  async extractInformation(documentId: string): Promise<ExtractionData> {
    const response = await api.post('/analysis/extract', { document_id: documentId })
    return response.data
  },

  async compareDocuments(documentAId: string, documentBId: string) {
    const response = await api.post('/analysis/compare', {
      document_a_id: documentAId,
      document_b_id: documentBId,
    })
    return response.data
  },
}

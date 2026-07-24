import api from './api'
import type { ExtractionData } from '../types'

export interface CitationSource {
  document_id: string
  document_title: string
  chunk_id: string
  page_number: number | null
  excerpt: string
  similarity_score: number | null
}

export interface RiskItem {
  title: string
  description: string
  severity: string
  category: string
  recommendation: string
  citations: CitationSource[]
  confidence_score: number
}

export interface RiskAnalysisResponse {
  overall_risk: string
  confidence_score: number
  confidence_level: string
  summary: string
  risks: RiskItem[]
  citations: CitationSource[]
  disclaimer: string
}

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

  async analyzeRisks(documentId: string): Promise<RiskAnalysisResponse> {
    const response = await api.post('/analysis/risks', { document_id: documentId })
    return response.data
  },
}

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

  // Analysis Records & Reviews
  async listAnalyses(params?: {
    document_id?: string
    analysis_type?: string
    status?: string
    confidence_level?: string
    overall_risk?: string
    skip?: number
    limit?: number
  }): Promise<AnalysisRecordList[]> {
    const response = await api.get('/analyses', { params })
    return response.data
  },

  async getAnalysis(id: string): Promise<AnalysisRecordDetail> {
    const response = await api.get(`/analyses/${id}`)
    return response.data
  },

  async createReview(id: string, decision: string, comment?: string): Promise<AnalysisReview> {
    const response = await api.post(`/analyses/${id}/reviews`, { decision, comment })
    return response.data
  },

  async listReviews(id: string): Promise<AnalysisReview[]> {
    const response = await api.get(`/analyses/${id}/reviews`)
    return response.data
  },

  async getImpactMetrics(): Promise<ImpactMetrics> {
    const response = await api.get('/metrics/impact')
    return response.data
  },
}

export interface AnalysisRecordList {
  id: string
  document_id: string
  analysis_type: string
  status: string
  confidence_score: number | null
  confidence_level: string | null
  overall_risk: string | null
  blocked: boolean
  version: number
  created_at: string
}

export interface AnalysisReview {
  id: string
  analysis_record_id: string
  reviewer_user_id: string
  reviewer_name: string
  previous_status: string
  new_status: string
  decision: string
  comment: string | null
  created_at: string
}

export interface AnalysisRecordDetail {
  id: string
  document_id: string
  user_id: string
  automation_run_id: string | null
  conversation_id: string | null
  message_id: string | null
  analysis_type: string
  status: string
  content_summary: string | null
  structured_result: any
  confidence_score: number | null
  confidence_level: string | null
  overall_risk: string | null
  citations: any
  disclaimer: string | null
  model_name: string | null
  prompt_version: string | null
  blocked: boolean
  processing_duration_ms: number | null
  estimated_manual_minutes: number | null
  estimated_time_saved_minutes: number | null
  version: number
  parent_analysis_id: string | null
  created_at: string
  updated_at: string
  reviews: AnalysisReview[]
}

export interface ImpactMetrics {
  documents_total: number
  analyses_total: number
  analyses_by_type: Record<string, number>
  reviews_by_status: Record<string, number>
  approval_rate: number
  average_confidence_score: number
  risks_by_severity: Record<string, number>
  automations_by_status: Record<string, number>
  failed_webhooks: number
  average_processing_duration_ms: number
  estimated_manual_minutes: number
  estimated_time_saved_minutes: number
  estimated_time_saved_hours: number
  estimation_notice: string
}

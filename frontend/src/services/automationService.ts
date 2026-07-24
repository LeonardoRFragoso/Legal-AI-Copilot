import api from './api'

export interface AutomationRun {
  id: string
  document_id: string
  user_id: string
  automation_type: string
  status: string
  current_step: string
  progress_percent: number
  started_at: string | null
  completed_at: string | null
  error_message: string | null
  summary_result: any
  risk_result: any
  webhook_status: string
  webhook_error: string | null
  created_at: string
  updated_at: string
}

export interface SystemStatus {
  timestamp: string
  automation_runs_by_status: Record<string, number>
  total_documents: number
  total_risk_analyses: number
  recent_failures: number
  avg_automation_duration_seconds: number | null
  failed_webhooks: number
}

export const automationService = {
  async listRuns(params?: {
    document_id?: string
    status?: string
    skip?: number
    limit?: number
  }): Promise<AutomationRun[]> {
    const response = await api.get('/automations/runs', { params })
    return response.data
  },

  async getRun(runId: string): Promise<AutomationRun> {
    const response = await api.get(`/automations/runs/${runId}`)
    return response.data
  },

  async retryRun(runId: string): Promise<{ message: string; run_id: string }> {
    const response = await api.post(`/automations/runs/${runId}/retry`)
    return response.data
  },

  async getSystemStatus(): Promise<SystemStatus> {
    const response = await api.get('/admin/system-status')
    return response.data
  },
}

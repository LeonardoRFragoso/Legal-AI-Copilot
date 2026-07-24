import { useEffect, useState } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Textarea from '../components/ui/Textarea'
import { analysisService, type AnalysisRecordList, type AnalysisRecordDetail } from '../services/analysisService'
import { useAuthStore } from '../store/authStore'
import {
  CheckCircle, XCircle, AlertCircle, Clock, FileSearch,
  Shield, ChevronRight, X, RefreshCw, Lock
} from 'lucide-react'

const statusConfig: Record<string, { color: string; icon: typeof CheckCircle; label: string }> = {
  GENERATED: { color: 'bg-gray-100 text-gray-700', icon: Clock, label: 'Gerada' },
  PENDING_REVIEW: { color: 'bg-blue-100 text-blue-700', icon: AlertCircle, label: 'Pendente' },
  APPROVED: { color: 'bg-green-100 text-green-700', icon: CheckCircle, label: 'Aprovada' },
  REJECTED: { color: 'bg-red-100 text-red-700', icon: XCircle, label: 'Rejeitada' },
  NEEDS_CHANGES: { color: 'bg-yellow-100 text-yellow-700', icon: AlertCircle, label: 'Correções' },
}

const typeLabels: Record<string, string> = {
  SUMMARY: 'Resumo',
  EXTRACTION: 'Extração',
  COMPARISON: 'Comparação',
  QUESTION_ANSWERING: 'Q&A',
  RISK_ANALYSIS: 'Análise de Riscos',
}

const riskColors: Record<string, string> = {
  low: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  high: 'bg-orange-100 text-orange-800',
  critical: 'bg-red-100 text-red-800',
}

export default function Reviews() {
  const { user } = useAuthStore()
  const [records, setRecords] = useState<AnalysisRecordList[]>([])
  const [loading, setLoading] = useState(true)
  const [filterStatus, setFilterStatus] = useState('')
  const [filterType, setFilterType] = useState('')
  const [selected, setSelected] = useState<AnalysisRecordDetail | null>(null)
  const [reviewComment, setReviewComment] = useState('')
  const [reviewDecision, setReviewDecision] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [reviewError, setReviewError] = useState('')

  const canReview = user?.role === 'ADMIN' || user?.role === 'LAWYER'

  const loadRecords = async () => {
    setLoading(true)
    try {
      const data = await analysisService.listAnalyses(
        filterStatus || filterType
          ? { status: filterStatus || undefined, analysis_type: filterType || undefined, limit: 50 }
          : { limit: 50 }
      )
      setRecords(data)
    } catch (error) {
      console.error('Error loading analyses:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadRecords()
  }, [filterStatus, filterType])

  const openDetail = async (id: string) => {
    try {
      const detail = await analysisService.getAnalysis(id)
      setSelected(detail)
      setReviewComment('')
      setReviewDecision('')
      setReviewError('')
    } catch (error) {
      console.error('Error loading analysis detail:', error)
    }
  }

  const handleSubmitReview = async () => {
    if (!selected || !reviewDecision) return
    if ((reviewDecision === 'REJECT' || reviewDecision === 'REQUEST_CHANGES') && !reviewComment) {
      setReviewError('Comentário é obrigatório para rejeitar ou solicitar correções')
      return
    }
    setSubmitting(true)
    setReviewError('')
    try {
      await analysisService.createReview(selected.id, reviewDecision, reviewComment || undefined)
      // Reload detail
      const detail = await analysisService.getAnalysis(selected.id)
      setSelected(detail)
      setReviewComment('')
      setReviewDecision('')
      loadRecords()
    } catch (err: any) {
      setReviewError(err.response?.data?.detail || 'Erro ao enviar revisão')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Revisão de Análises</h2>
          <p className="text-sm text-gray-500 mt-1">
            Revise e aprove análises geradas pelo AI
          </p>
        </div>
        <div className="flex gap-2">
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm"
          >
            <option value="">Todos os Tipos</option>
            <option value="SUMMARY">Resumo</option>
            <option value="EXTRACTION">Extração</option>
            <option value="COMPARISON">Comparação</option>
            <option value="QUESTION_ANSWERING">Q&A</option>
            <option value="RISK_ANALYSIS">Análise de Riscos</option>
          </select>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm"
          >
            <option value="">Todos os Status</option>
            <option value="GENERATED">Gerada</option>
            <option value="PENDING_REVIEW">Pendente</option>
            <option value="APPROVED">Aprovada</option>
            <option value="REJECTED">Rejeitada</option>
            <option value="NEEDS_CHANGES">Correções</option>
          </select>
          <Button onClick={loadRecords} disabled={loading}>
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Atualizar
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* List */}
        <div className="lg:col-span-1 space-y-3">
          {records.length === 0 ? (
            <Card className="p-12 text-center">
              <FileSearch className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500">Nenhuma análise encontrada</p>
            </Card>
          ) : (
            records.map((record) => {
              const config = statusConfig[record.status] || statusConfig.GENERATED
              const StatusIcon = config.icon
              return (
                <Card
                  key={record.id}
                  className="p-4 cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => openDetail(record.id)}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <StatusIcon className="w-4 h-4 text-gray-600" />
                      <span className={`px-2 py-0.5 text-xs rounded font-bold ${config.color}`}>
                        {config.label}
                      </span>
                      {record.blocked && (
                        <Lock className="w-3 h-3 text-red-500" />
                      )}
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-400" />
                  </div>
                  <p className="text-sm font-medium text-gray-900">
                    {typeLabels[record.analysis_type] || record.analysis_type}
                  </p>
                  <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
                    {record.confidence_level && (
                      <span>Confiança: {record.confidence_level}</span>
                    )}
                    {record.overall_risk && (
                      <span className={`px-1.5 py-0.5 rounded ${riskColors[record.overall_risk] || ''}`}>
                        Risco: {record.overall_risk}
                      </span>
                    )}
                    <span>v{record.version}</span>
                    <span>{new Date(record.created_at).toLocaleDateString('pt-BR')}</span>
                  </div>
                </Card>
              )
            })
          )}
        </div>

        {/* Detail */}
        <div className="lg:col-span-2">
          {!selected ? (
            <Card className="p-12 text-center">
              <FileSearch className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500">Selecione uma análise para ver os detalhes</p>
            </Card>
          ) : (
            <Card className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">
                    {typeLabels[selected.analysis_type] || selected.analysis_type}
                  </h3>
                  <div className="flex items-center gap-2 mt-1">
                    <span className={`px-2 py-0.5 text-xs rounded font-bold ${statusConfig[selected.status]?.color || ''}`}>
                      {statusConfig[selected.status]?.label || selected.status}
                    </span>
                    {selected.blocked && (
                      <span className="px-2 py-0.5 text-xs rounded font-bold bg-red-100 text-red-700">
                        Bloqueada
                      </span>
                    )}
                    <span className="text-xs text-gray-500">v{selected.version}</span>
                  </div>
                </div>
                <button onClick={() => setSelected(null)} className="text-gray-400 hover:text-gray-600">
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Metadata grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4 text-sm">
                {selected.confidence_score !== null && (
                  <div>
                    <span className="text-gray-500">Confiança:</span>
                    <span className="ml-1 font-medium">{selected.confidence_score}/100</span>
                  </div>
                )}
                {selected.confidence_level && (
                  <div>
                    <span className="text-gray-500">Nível:</span>
                    <span className="ml-1 font-medium">{selected.confidence_level}</span>
                  </div>
                )}
                {selected.overall_risk && (
                  <div>
                    <span className="text-gray-500">Risco:</span>
                    <span className={`ml-1 px-1.5 py-0.5 rounded text-xs font-bold ${riskColors[selected.overall_risk] || ''}`}>
                      {selected.overall_risk}
                    </span>
                  </div>
                )}
                {selected.model_name && (
                  <div>
                    <span className="text-gray-500">Modelo:</span>
                    <span className="ml-1 font-medium">{selected.model_name}</span>
                  </div>
                )}
                {selected.estimated_time_saved_minutes !== null && (
                  <div>
                    <span className="text-gray-500">Tempo poupado:</span>
                    <span className="ml-1 font-medium">~{selected.estimated_time_saved_minutes}min</span>
                  </div>
                )}
                <div>
                  <span className="text-gray-500">Criada:</span>
                  <span className="ml-1">{new Date(selected.created_at).toLocaleString('pt-BR')}</span>
                </div>
              </div>

              {/* Content summary */}
              {selected.content_summary && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Resumo do Conteúdo</h4>
                  <div className="bg-gray-50 rounded-lg p-3 text-sm text-gray-800 whitespace-pre-wrap max-h-48 overflow-y-auto">
                    {selected.content_summary}
                  </div>
                </div>
              )}

              {/* Structured result — risks */}
              {selected.structured_result?.risks && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-1">
                    <Shield className="w-4 h-4 text-orange-500" />
                    Riscos Identificados
                  </h4>
                  <div className="space-y-2">
                    {selected.structured_result.risks.map((risk: any, i: number) => (
                      <div key={i} className="border-l-4 border-orange-400 pl-3 py-1">
                        <div className="flex items-center gap-2">
                          <span className={`px-1.5 py-0.5 text-xs rounded font-bold ${riskColors[risk.severity] || ''}`}>
                            {risk.severity?.toUpperCase()}
                          </span>
                          <span className="font-medium text-sm">{risk.title}</span>
                        </div>
                        <p className="text-xs text-gray-600 mt-1">{risk.description}</p>
                        {risk.recommendation && (
                          <p className="text-xs text-blue-600 mt-1">→ {risk.recommendation}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Disclaimer */}
              {selected.disclaimer && (
                <div className="mb-4">
                  <p className="text-xs text-gray-400 italic">{selected.disclaimer}</p>
                </div>
              )}

              {/* Review history */}
              {selected.reviews.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Histórico de Revisões</h4>
                  <div className="space-y-2">
                    {selected.reviews.map((review) => (
                      <div key={review.id} className="bg-gray-50 rounded-lg p-3">
                        <div className="flex items-center gap-2 mb-1">
                          <span className={`px-1.5 py-0.5 text-xs rounded font-bold ${
                            review.decision === 'APPROVE' ? 'bg-green-100 text-green-700' :
                            review.decision === 'REJECT' ? 'bg-red-100 text-red-700' :
                            'bg-yellow-100 text-yellow-700'
                          }`}>
                            {review.decision}
                          </span>
                          <span className="text-xs text-gray-500">{review.reviewer_name}</span>
                          <span className="text-xs text-gray-400">
                            {new Date(review.created_at).toLocaleString('pt-BR')}
                          </span>
                        </div>
                        {review.comment && (
                          <p className="text-sm text-gray-700">{review.comment}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Review form */}
              {canReview && selected.status !== 'APPROVED' && (
                <div className="border-t pt-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Enviar Revisão</h4>
                  {reviewError && (
                    <div className="bg-red-50 border border-red-200 rounded p-2 mb-2">
                      <p className="text-sm text-red-700">{reviewError}</p>
                    </div>
                  )}
                  <div className="flex gap-2 mb-2">
                    <Button
                      variant={reviewDecision === 'APPROVE' ? 'primary' : 'outline'}
                      onClick={() => setReviewDecision('APPROVE')}
                      className="text-sm"
                      disabled={selected.blocked}
                    >
                      <CheckCircle className="w-4 h-4 mr-1" />
                      Aprovar
                    </Button>
                    <Button
                      variant={reviewDecision === 'REJECT' ? 'primary' : 'outline'}
                      onClick={() => setReviewDecision('REJECT')}
                      className="text-sm"
                    >
                      <XCircle className="w-4 h-4 mr-1" />
                      Rejeitar
                    </Button>
                    <Button
                      variant={reviewDecision === 'REQUEST_CHANGES' ? 'primary' : 'outline'}
                      onClick={() => setReviewDecision('REQUEST_CHANGES')}
                      className="text-sm"
                    >
                      <AlertCircle className="w-4 h-4 mr-1" />
                      Correções
                    </Button>
                  </div>
                  {reviewDecision && (
                    <>
                      <Textarea
                        value={reviewComment}
                        onChange={(e) => setReviewComment(e.target.value)}
                        placeholder={
                          reviewDecision === 'APPROVE'
                            ? 'Comentário (opcional para aprovação)...'
                            : 'Comentário (obrigatório)...'
                        }
                        rows={3}
                        className="mb-2"
                      />
                      <Button onClick={handleSubmitReview} disabled={submitting || !reviewDecision}>
                        {submitting ? 'Enviando...' : 'Confirmar Revisão'}
                      </Button>
                    </>
                  )}
                </div>
              )}

              {!canReview && (
                <div className="border-t pt-4">
                  <p className="text-sm text-gray-500">
                    Seu perfil não permite revisar análises.
                  </p>
                </div>
              )}

              {selected.status === 'APPROVED' && (
                <div className="border-t pt-4">
                  <div className="bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <p className="text-sm text-green-700">Esta análise foi aprovada.</p>
                  </div>
                </div>
              )}
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { analysisService, type ImpactMetrics } from '../services/analysisService'
import {
  FileText, BarChart3, Clock, TrendingUp, Shield,
  CheckCircle, RefreshCw, Zap
} from 'lucide-react'

const riskColors: Record<string, string> = {
  low: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  high: 'bg-orange-100 text-orange-800',
  critical: 'bg-red-100 text-red-800',
}

const typeLabels: Record<string, string> = {
  SUMMARY: 'Resumo',
  EXTRACTION: 'Extração',
  COMPARISON: 'Comparação',
  QUESTION_ANSWERING: 'Q&A',
  RISK_ANALYSIS: 'Análise de Riscos',
}

const statusLabels: Record<string, string> = {
  GENERATED: 'Gerada',
  PENDING_REVIEW: 'Pendente',
  APPROVED: 'Aprovada',
  REJECTED: 'Rejeitada',
  NEEDS_CHANGES: 'Correções',
}

export default function Insights() {
  const [metrics, setMetrics] = useState<ImpactMetrics | null>(null)
  const [loading, setLoading] = useState(true)

  const loadMetrics = async () => {
    setLoading(true)
    try {
      const data = await analysisService.getImpactMetrics()
      setMetrics(data)
    } catch (error) {
      console.error('Error loading metrics:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadMetrics()
  }, [])

  if (loading) {
    return <div className="text-center py-12">Carregando métricas...</div>
  }

  if (!metrics) {
    return <div className="text-center py-12 text-gray-500">Erro ao carregar métricas</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Métricas de Impacto</h2>
          <p className="text-sm text-gray-500 mt-1">
            Dashboard de produtividade e revisão
          </p>
        </div>
        <Button onClick={loadMetrics} disabled={loading}>
          <RefreshCw className="w-4 h-4 mr-2" />
          Atualizar
        </Button>
      </div>

      {/* Top metrics cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-5">
          <div className="flex items-center justify-between mb-2">
            <FileText className="w-8 h-8 text-blue-600" />
            <span className="text-2xl font-bold text-gray-900">{metrics.documents_total}</span>
          </div>
          <p className="text-sm text-gray-500">Documentos</p>
        </Card>

        <Card className="p-5">
          <div className="flex items-center justify-between mb-2">
            <BarChart3 className="w-8 h-8 text-purple-600" />
            <span className="text-2xl font-bold text-gray-900">{metrics.analyses_total}</span>
          </div>
          <p className="text-sm text-gray-500">Análises Geradas</p>
        </Card>

        <Card className="p-5">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="w-8 h-8 text-green-600" />
            <span className="text-2xl font-bold text-gray-900">
              {metrics.estimated_time_saved_hours}h
            </span>
          </div>
          <p className="text-sm text-gray-500">Tempo Poupado (est.)</p>
        </Card>

        <Card className="p-5">
          <div className="flex items-center justify-between mb-2">
            <CheckCircle className="w-8 h-8 text-green-600" />
            <span className="text-2xl font-bold text-gray-900">
              {metrics.approval_rate}%
            </span>
          </div>
          <p className="text-sm text-gray-500">Taxa de Aprovação</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Analyses by type */}
        <Card className="p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Análises por Tipo</h3>
          {Object.keys(metrics.analyses_by_type).length === 0 ? (
            <p className="text-sm text-gray-500">Nenhuma análise registrada</p>
          ) : (
            <div className="space-y-3">
              {Object.entries(metrics.analyses_by_type).map(([type, count]) => {
                const max = Math.max(...Object.values(metrics.analyses_by_type))
                const pct = (count / max) * 100
                return (
                  <div key={type}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-700">{typeLabels[type] || type}</span>
                      <span className="font-medium">{count}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </Card>

        {/* Reviews by status */}
        <Card className="p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Status das Revisões</h3>
          {Object.keys(metrics.reviews_by_status).length === 0 ? (
            <p className="text-sm text-gray-500">Nenhuma revisão registrada</p>
          ) : (
            <div className="space-y-2">
              {Object.entries(metrics.reviews_by_status).map(([status, count]) => (
                <div key={status} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                  <span className="text-sm text-gray-700">{statusLabels[status] || status}</span>
                  <span className="font-bold text-gray-900">{count}</span>
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* Risks by severity */}
        <Card className="p-5">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-orange-500" />
            Riscos por Severidade
          </h3>
          {Object.keys(metrics.risks_by_severity).length === 0 ? (
            <p className="text-sm text-gray-500">Nenhum risco identificado</p>
          ) : (
            <div className="space-y-2">
              {Object.entries(metrics.risks_by_severity).map(([severity, count]) => (
                <div key={severity} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                  <span className={`px-2 py-0.5 text-xs rounded font-bold ${riskColors[severity] || ''}`}>
                    {severity.toUpperCase()}
                  </span>
                  <span className="font-bold text-gray-900">{count}</span>
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* Automations by status */}
        <Card className="p-5">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-blue-500" />
            Automações por Status
          </h3>
          {Object.keys(metrics.automations_by_status).length === 0 ? (
            <p className="text-sm text-gray-500">Nenhuma automação registrada</p>
          ) : (
            <div className="space-y-2">
              {Object.entries(metrics.automations_by_status).map(([status, count]) => (
                <div key={status} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                  <span className="text-sm text-gray-700">{status}</span>
                  <span className="font-bold text-gray-900">{count}</span>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {/* Time savings detail */}
      <Card className="p-5">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Clock className="w-5 h-5 text-blue-500" />
          Estimativa de Produtividade
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Tempo Manual Estimado</p>
            <p className="text-2xl font-bold text-blue-900 mt-1">
              {metrics.estimated_manual_minutes} min
            </p>
          </div>
          <div className="bg-green-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Tempo Poupado Estimado</p>
            <p className="text-2xl font-bold text-green-900 mt-1">
              {metrics.estimated_time_saved_minutes} min
            </p>
          </div>
          <div className="bg-purple-50 rounded-lg p-4">
            <p className="text-sm text-gray-600">Confiança Média</p>
            <p className="text-2xl font-bold text-purple-900 mt-1">
              {metrics.average_confidence_score}/100
            </p>
          </div>
        </div>
        <p className="text-xs text-gray-400 italic mt-4">{metrics.estimation_notice}</p>
      </Card>
    </div>
  )
}

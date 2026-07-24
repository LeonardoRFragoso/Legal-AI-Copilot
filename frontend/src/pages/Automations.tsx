import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { automationService, type AutomationRun } from '../services/automationService'
import { Zap, RefreshCw, AlertCircle, CheckCircle, Clock, XCircle } from 'lucide-react'

const statusConfig: Record<string, { color: string; icon: typeof CheckCircle; label: string }> = {
  PENDING: { color: 'bg-gray-100 text-gray-700', icon: Clock, label: 'PENDING' },
  RUNNING: { color: 'bg-blue-100 text-blue-700', icon: Zap, label: 'RUNNING' },
  COMPLETED: { color: 'bg-green-100 text-green-700', icon: CheckCircle, label: 'COMPLETED' },
  FAILED: { color: 'bg-red-100 text-red-700', icon: XCircle, label: 'FAILED' },
  PARTIAL_SUCCESS: { color: 'bg-yellow-100 text-yellow-700', icon: AlertCircle, label: 'PARTIAL' },
}

const stepLabels: Record<string, string> = {
  DOCUMENT_PROCESSING: 'Processando Documento',
  SUMMARY: 'Gerando Resumo',
  RISK_ANALYSIS: 'Analisando Riscos',
  WEBHOOK: 'Enviando Webhook',
  COMPLETED: 'Concluído',
}

export default function Automations() {
  const navigate = useNavigate()
  const [runs, setRuns] = useState<AutomationRun[]>([])
  const [loading, setLoading] = useState(true)
  const [filterStatus, setFilterStatus] = useState('')
  const [retrying, setRetrying] = useState<string | null>(null)

  const loadRuns = async () => {
    setLoading(true)
    try {
      const data = await automationService.listRuns(
        filterStatus ? { status: filterStatus } : undefined
      )
      setRuns(data)
    } catch (error) {
      console.error('Error loading automation runs:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadRuns()
  }, [filterStatus])

  const handleRetry = async (runId: string) => {
    setRetrying(runId)
    try {
      await automationService.retryRun(runId)
      await loadRuns()
    } catch (error) {
      console.error('Error retrying:', error)
    } finally {
      setRetrying(null)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Automações</h2>
        <div className="flex gap-2">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg"
          >
            <option value="">Todos os Status</option>
            <option value="PENDING">PENDING</option>
            <option value="RUNNING">RUNNING</option>
            <option value="COMPLETED">COMPLETED</option>
            <option value="FAILED">FAILED</option>
            <option value="PARTIAL_SUCCESS">PARTIAL_SUCCESS</option>
          </select>
          <Button onClick={loadRuns} disabled={loading}>
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Atualizar
          </Button>
        </div>
      </div>

      {runs.length === 0 ? (
        <Card className="p-12 text-center">
          <Zap className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhuma automação encontrada
          </h3>
          <p className="text-gray-500 mb-4">
            Faça upload de um documento para iniciar a automação
          </p>
          <Button onClick={() => navigate('/upload')}>
            Ir para Upload
          </Button>
        </Card>
      ) : (
        <div className="space-y-4">
          {runs.map((run) => {
            const config = statusConfig[run.status] || statusConfig.PENDING
            const StatusIcon = config.icon

            return (
              <Card key={run.id} className="p-5">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <StatusIcon className="w-5 h-5 text-gray-600" />
                    <div>
                      <span className={`inline-block px-2 py-1 text-xs rounded font-bold ${config.color}`}>
                        {config.label}
                      </span>
                      <span className="ml-2 text-sm text-gray-500">
                        {stepLabels[run.current_step] || run.current_step}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-gray-500">
                      {new Date(run.created_at).toLocaleString('pt-BR')}
                    </div>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="mb-3">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>Progresso</span>
                    <span>{run.progress_percent}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${
                        run.status === 'COMPLETED' ? 'bg-green-500' :
                        run.status === 'FAILED' ? 'bg-red-500' :
                        run.status === 'PARTIAL_SUCCESS' ? 'bg-yellow-500' :
                        'bg-blue-500'
                      }`}
                      style={{ width: `${run.progress_percent}%` }}
                    />
                  </div>
                </div>

                {/* Details */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                  <div>
                    <span className="text-gray-500">Documento:</span>
                    <button
                      onClick={() => navigate(`/analysis?doc=${run.document_id}`)}
                      className="ml-1 text-blue-600 hover:underline"
                    >
                      Ver documento
                    </button>
                  </div>
                  <div>
                    <span className="text-gray-500">Riscos:</span>
                    <button
                      onClick={() => navigate(`/risks?doc=${run.document_id}`)}
                      className="ml-1 text-blue-600 hover:underline"
                    >
                      Ver riscos
                    </button>
                  </div>
                  <div>
                    <span className="text-gray-500">Webhook:</span>
                    <span className={`ml-1 font-medium ${
                      run.webhook_status === 'sent' ? 'text-green-600' :
                      run.webhook_status === 'failed' ? 'text-red-600' :
                      'text-gray-600'
                    }`}>
                      {run.webhook_status}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">Tipo:</span>
                    <span className="ml-1">{run.automation_type}</span>
                  </div>
                </div>

                {/* Error message */}
                {run.error_message && (
                  <div className="mt-3 bg-red-50 border border-red-200 rounded p-3">
                    <p className="text-sm text-red-700">
                      <span className="font-semibold">Erro: </span>
                      {run.error_message}
                    </p>
                  </div>
                )}

                {/* Webhook error */}
                {run.webhook_error && (
                  <div className="mt-2 bg-yellow-50 border border-yellow-200 rounded p-3">
                    <p className="text-sm text-yellow-700">
                      <span className="font-semibold">Webhook: </span>
                      {run.webhook_error}
                    </p>
                  </div>
                )}

                {/* Retry button */}
                {(run.status === 'FAILED' || run.status === 'PARTIAL_SUCCESS') && (
                  <div className="mt-3">
                    <Button
                      onClick={() => handleRetry(run.id)}
                      disabled={retrying === run.id}
                      className="text-sm"
                    >
                      <RefreshCw className={`w-4 h-4 mr-2 ${retrying === run.id ? 'animate-spin' : ''}`} />
                      {retrying === run.id ? 'Tentando novamente...' : 'Tentar Novamente'}
                    </Button>
                  </div>
                )}
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}

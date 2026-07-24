import { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { documentService } from '../services/documentService'
import { analysisService, type RiskAnalysisResponse, type RiskItem } from '../services/analysisService'
import type { Document } from '../types'
import { AlertTriangle, Shield, FileText, ChevronDown, ChevronUp } from 'lucide-react'

const severityColors: Record<string, string> = {
  low: 'bg-green-100 text-green-800 border-green-200',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  high: 'bg-orange-100 text-orange-800 border-orange-200',
  critical: 'bg-red-100 text-red-800 border-red-200',
}

const severityLabels: Record<string, string> = {
  low: 'LOW',
  medium: 'MEDIUM',
  high: 'HIGH',
  critical: 'CRITICAL',
}

const confidenceColors: Record<string, string> = {
  high: 'text-green-600',
  moderate: 'text-yellow-600',
  low: 'text-red-600',
}

function RiskCard({ risk }: { risk: RiskItem }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <Card className={`p-4 border-l-4 ${
      risk.severity === 'critical' ? 'border-red-500' :
      risk.severity === 'high' ? 'border-orange-500' :
      risk.severity === 'medium' ? 'border-yellow-500' :
      'border-green-500'
    }`}>
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className={`inline-block px-2 py-1 text-xs rounded font-bold border ${severityColors[risk.severity] || severityColors.medium}`}>
              {severityLabels[risk.severity] || risk.severity.toUpperCase()}
            </span>
            <span className="inline-block px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded font-medium capitalize">
              {risk.category.replace(/_/g, ' ')}
            </span>
          </div>
          <h4 className="font-bold text-gray-900">{risk.title}</h4>
          <p className="text-sm text-gray-600 mt-1">{risk.description}</p>
        </div>
        <div className="text-right ml-4">
          <div className="text-xs text-gray-500">Confidence</div>
          <div className="text-lg font-bold text-gray-900">{risk.confidence_score}%</div>
        </div>
      </div>

      <div className="mt-3 bg-blue-50 border border-blue-200 rounded p-3">
        <p className="text-sm text-blue-900">
          <span className="font-semibold">Recommendation: </span>
          {risk.recommendation}
        </p>
      </div>

      {risk.citations.length > 0 && (
        <div className="mt-3">
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900"
          >
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            Sources ({risk.citations.length})
          </button>
          {expanded && (
            <div className="mt-2 space-y-2">
              {risk.citations.map((citation, i) => (
                <div key={i} className="bg-gray-50 border border-gray-200 rounded p-3 text-sm">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-gray-700">{citation.document_title}</span>
                    {citation.page_number && (
                      <span className="text-xs text-gray-500">Page {citation.page_number}</span>
                    )}
                  </div>
                  <p className="text-gray-600 italic">"{citation.excerpt}"</p>
                  {citation.similarity_score && (
                    <div className="mt-1 text-xs text-gray-400">
                      Similarity: {(citation.similarity_score * 100).toFixed(0)}%
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </Card>
  )
}

export default function RiskAnalysis() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const docId = searchParams.get('doc')
  const [documents, setDocuments] = useState<Document[]>([])
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null)
  const [riskResult, setRiskResult] = useState<RiskAnalysisResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const docs = await documentService.list()
      setDocuments(docs)
      if (docId) {
        const doc = docs.find(d => d.id === docId)
        if (doc) setSelectedDocument(doc)
      } else if (docs.length > 0) {
        setSelectedDocument(docs[0])
      }
    } catch (error) {
      console.error('Error loading documents:', error)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedDocument) return
    setLoading(true)
    setError('')
    setRiskResult(null)
    try {
      const result = await analysisService.analyzeRisks(selectedDocument.id)
      setRiskResult(result)
    } catch (err) {
      console.error('Error analyzing risks:', err)
      setError('Erro ao analisar riscos. Verifique se o documento foi processado.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Análise de Riscos</h2>
        <select
          value={selectedDocument?.id || ''}
          onChange={(e) => {
            const doc = documents.find(d => d.id === e.target.value)
            if (doc) setSelectedDocument(doc)
          }}
          className="px-4 py-2 border border-gray-300 rounded-lg"
        >
          {documents.map((doc) => (
            <option key={doc.id} value={doc.id}>
              {doc.title}
            </option>
          ))}
        </select>
      </div>

      {!selectedDocument ? (
        <Card className="p-12 text-center">
          <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhum documento selecionado
          </h3>
          <p className="text-gray-500 mb-4">
            Selecione um documento para analisar riscos
          </p>
          <Button onClick={() => navigate('/dashboard')}>
            Ir para Dashboard
          </Button>
        </Card>
      ) : (
        <>
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Shield className="w-5 h-5 text-blue-600" />
                  Análise de Riscos Contratuais
                </h3>
                <p className="text-sm text-gray-500 mt-1">
                  Identifica riscos potenciais no contrato usando heurísticas e RAG
                </p>
              </div>
              <Button
                onClick={handleAnalyze}
                disabled={loading}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700"
              >
                <AlertTriangle className="w-4 h-4" />
                {loading ? 'Analisando...' : 'Analyze Risks'}
              </Button>
            </div>
          </Card>

          {error && (
            <Card className="p-4 bg-red-50 border border-red-200">
              <p className="text-red-700">{error}</p>
            </Card>
          )}

          {loading && (
            <Card className="p-12 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
              <p>Analisando riscos do documento...</p>
            </Card>
          )}

          {riskResult && !loading && (
            <div className="space-y-6">
              {/* Overall Risk Header */}
              <Card className={`p-6 border-2 ${
                riskResult.overall_risk === 'critical' ? 'border-red-300 bg-red-50' :
                riskResult.overall_risk === 'high' ? 'border-orange-300 bg-orange-50' :
                riskResult.overall_risk === 'medium' ? 'border-yellow-300 bg-yellow-50' :
                'border-green-300 bg-green-50'
              }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Overall Risk</p>
                    <p className={`text-3xl font-bold ${
                      riskResult.overall_risk === 'critical' ? 'text-red-700' :
                      riskResult.overall_risk === 'high' ? 'text-orange-700' :
                      riskResult.overall_risk === 'medium' ? 'text-yellow-700' :
                      'text-green-700'
                    }`}>
                      {riskResult.overall_risk.toUpperCase()}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600 mb-1">Sustentação Documental</p>
                    <p className={`text-3xl font-bold ${confidenceColors[riskResult.confidence_level] || 'text-gray-700'}`}>
                      {riskResult.confidence_score}%
                    </p>
                    <p className="text-xs text-gray-500 capitalize">{riskResult.confidence_level}</p>
                  </div>
                </div>
                <p className="mt-4 text-gray-700">{riskResult.summary}</p>
              </Card>

              {/* Risk List */}
              {riskResult.risks.length > 0 ? (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Riscos Identificados ({riskResult.risks.length})
                  </h3>
                  {riskResult.risks.map((risk, i) => (
                    <RiskCard key={i} risk={risk} />
                  ))}
                </div>
              ) : (
                <Card className="p-8 text-center">
                  <Shield className="w-12 h-12 mx-auto text-green-600 mb-3" />
                  <p className="text-green-700 font-medium">
                    Nenhum risco significativo detectado
                  </p>
                </Card>
              )}

              {/* Disclaimer */}
              <Card className="p-4 bg-gray-50 border border-gray-200">
                <p className="text-sm text-gray-600 italic">
                  {riskResult.disclaimer}
                </p>
              </Card>
            </div>
          )}
        </>
      )}
    </div>
  )
}

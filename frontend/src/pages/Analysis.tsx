import { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { documentService } from '../services/documentService'
import { analysisService } from '../services/analysisService'
import { chatService } from '../services/chatService'
import type { Document, ExtractionData } from '../types'
import { FileText, BarChart3, Users, Calendar, DollarSign, Scale, MessageSquare } from 'lucide-react'

export default function Analysis() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const docId = searchParams.get('doc')
  const [documents, setDocuments] = useState<Document[]>([])
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null)
  const [summary, setSummary] = useState('')
  const [extraction, setExtraction] = useState<ExtractionData | null>(null)
  const [loading, setLoading] = useState(false)
  const [startingChat, setStartingChat] = useState(false)

  useEffect(() => {
    loadDocuments()
    if (docId) {
      const doc = documents.find(d => d.id === docId)
      if (doc) setSelectedDocument(doc)
    }
  }, [docId])

  useEffect(() => {
    if (selectedDocument) {
      loadAnalysis()
    }
  }, [selectedDocument])

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

  const loadAnalysis = async () => {
    if (!selectedDocument) return

    setLoading(true)
    try {
      const [summaryData, extractionData] = await Promise.all([
        analysisService.generateSummary(selectedDocument.id),
        analysisService.extractInformation(selectedDocument.id),
      ])
      setSummary(summaryData.summary)
      setExtraction(extractionData)
    } catch (error) {
      console.error('Error loading analysis:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStartChat = async () => {
    if (!selectedDocument || !summary || !extraction) return

    setStartingChat(true)
    try {
      const newConv = await chatService.createConversation(
        selectedDocument.id,
        `Chat sobre ${selectedDocument.title}`
      )
      navigate(`/chat?conv=${newConv.id}`)
    } catch (error) {
      console.error('Error starting chat:', error)
      setStartingChat(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Análise de Contrato</h2>
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
            Selecione um documento para analisar
          </p>
          <Button onClick={() => navigate('/dashboard')}>
            Ir para Dashboard
          </Button>
        </Card>
      ) : loading ? (
        <Card className="p-12 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
          <p>Analisando documento...</p>
        </Card>
      ) : (
        <div className="space-y-6">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-semibold">Resumo</h3>
              </div>
              <Button 
                onClick={handleStartChat}
                disabled={startingChat}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700"
              >
                <MessageSquare className="w-4 h-4" />
                Iniciar Chat
              </Button>
            </div>
            <p className="text-gray-700 whitespace-pre-wrap">{summary || 'Resumo não disponível'}</p>
          </Card>

          <div className="grid md:grid-cols-2 gap-6">
            <Card className="p-6">
              <div className="flex items-center gap-2 mb-2">
                <Users className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-semibold">Partes Envolvidas</h3>
              </div>
              <p className="text-sm text-gray-500 mb-4">Pessoas jurídicas ou físicas envolvidas no contrato</p>
              <ul className="space-y-4">
                {extraction?.parties && extraction.parties.length > 0 ? (
                  extraction.parties.map((party: any, i: number) => (
                    <li key={i} className="border-l-4 border-blue-500 pl-3 py-2">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-bold text-gray-900">{party.name || party}</p>
                          {party.role && (
                            <p className="text-sm text-gray-600 mt-1">
                              <span className="font-semibold">Papel:</span> {party.role === 'contratante' ? 'Contratante (quem contrata)' : party.role === 'contratada' ? 'Contratada (prestadora)' : party.role}
                            </p>
                          )}
                          {party.description && (
                            <p className="text-sm text-gray-600 mt-1">{party.description}</p>
                          )}
                        </div>
                      </div>
                    </li>
                  ))
                ) : (
                  <li className="text-gray-500 italic">Nenhuma parte identificada</li>
                )}
              </ul>
            </Card>

            <Card className="p-6">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-5 h-5 text-green-600" />
                <h3 className="text-lg font-semibold">Datas Importantes</h3>
              </div>
              <p className="text-sm text-gray-500 mb-4">Datas de início, término, renovação e prazos</p>
              <ul className="space-y-4">
                {extraction?.dates && extraction.dates.length > 0 ? (
                  extraction.dates.map((dateItem: any, i: number) => (
                    <li key={i} className="border-l-4 border-green-500 pl-3 py-2">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-bold text-gray-900">{dateItem.date || dateItem}</p>
                          {dateItem.description && (
                            <p className="text-sm text-gray-600 mt-1">{dateItem.description}</p>
                          )}
                          {dateItem.type && (
                            <span className="inline-block mt-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded font-medium">
                              {dateItem.type.charAt(0).toUpperCase() + dateItem.type.slice(1)}
                            </span>
                          )}
                        </div>
                      </div>
                    </li>
                  ))
                ) : (
                  <li className="text-gray-500 italic">Nenhuma data identificada</li>
                )}
              </ul>
            </Card>

            <Card className="p-6">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="w-5 h-5 text-amber-600" />
                <h3 className="text-lg font-semibold">Valores</h3>
              </div>
              <p className="text-sm text-gray-500 mb-4">Valores monetários, taxas, multas e custos</p>
              <ul className="space-y-4">
                {extraction?.values && extraction.values.length > 0 ? (
                  extraction.values.map((valueItem: any, i: number) => (
                    <li key={i} className="border-l-4 border-amber-500 pl-3 py-2">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-bold text-gray-900">{valueItem.amount || valueItem}</p>
                          {valueItem.description && (
                            <p className="text-sm text-gray-600 mt-1">{valueItem.description}</p>
                          )}
                          {valueItem.type && (
                            <span className="inline-block mt-2 px-2 py-1 bg-amber-100 text-amber-800 text-xs rounded font-medium">
                              {valueItem.type.replace(/_/g, ' ').charAt(0).toUpperCase() + valueItem.type.slice(1).replace(/_/g, ' ')}
                            </span>
                          )}
                        </div>
                      </div>
                    </li>
                  ))
                ) : (
                  <li className="text-gray-500 italic">Nenhum valor identificado</li>
                )}
              </ul>
            </Card>

            <Card className="p-6">
              <div className="flex items-center gap-2 mb-2">
                <Scale className="w-5 h-5 text-purple-600" />
                <h3 className="text-lg font-semibold">Cláusulas Importantes</h3>
              </div>
              <p className="text-sm text-gray-500 mb-4">Termos legais críticos como confidencialidade, multas, rescisão</p>
              <ul className="space-y-4">
                {extraction?.clauses && extraction.clauses.length > 0 ? (
                  extraction.clauses.map((clauseItem: any, i: number) => {
                    const riskColors: Record<string, string> = {
                      baixo: 'bg-green-50 border-green-200',
                      medio: 'bg-yellow-50 border-yellow-200',
                      alto: 'bg-red-50 border-red-200'
                    }
                    const riskBadgeColors: Record<string, string> = {
                      baixo: 'bg-green-100 text-green-800',
                      medio: 'bg-yellow-100 text-yellow-800',
                      alto: 'bg-red-100 text-red-800'
                    }
                    const riskLabels: Record<string, string> = {
                      baixo: 'Baixo Risco',
                      medio: 'Risco Médio',
                      alto: 'Alto Risco'
                    }
                    
                    const risk = clauseItem.risk || 'medio'
                    
                    return (
                      <li key={i} className={`border-l-4 border-purple-500 pl-3 py-2 rounded-r border ${riskColors[risk] || riskColors.medio}`}>
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <p className="font-bold text-gray-900 capitalize">{clauseItem.clause || clauseItem}</p>
                            {clauseItem.description && (
                              <p className="text-sm text-gray-600 mt-1">{clauseItem.description}</p>
                            )}
                            <div className="flex gap-2 mt-2">
                              {clauseItem.type && (
                                <span className="inline-block px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded font-medium">
                                  {clauseItem.type.charAt(0).toUpperCase() + clauseItem.type.slice(1)}
                                </span>
                              )}
                              {risk && (
                                <span className={`inline-block px-2 py-1 text-xs rounded font-medium ${riskBadgeColors[risk] || riskBadgeColors.medio}`}>
                                  {riskLabels[risk] || riskLabels.medio}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </li>
                    )
                  })
                ) : (
                  <li className="text-gray-500 italic">Nenhuma cláusula identificada</li>
                )}
              </ul>
            </Card>
          </div>
        </div>
      )}
    </div>
  )
}

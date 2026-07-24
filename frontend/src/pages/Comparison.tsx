import { useEffect, useState } from 'react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { documentService } from '../services/documentService'
import { analysisService } from '../services/analysisService'
import type { Document } from '../types'
import { GitCompare, ArrowRight } from 'lucide-react'

// Simple markdown parser for bold text
const parseMarkdown = (text: string) => {
  const parts: (string | JSX.Element)[] = []
  let lastIndex = 0
  const regex = /\*\*(.+?)\*\*/g
  let match

  while ((match = regex.exec(text)) !== null) {
    // Add text before the match
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index))
    }
    // Add bold text
    parts.push(
      <strong key={match.index} className="font-bold text-gray-900">
        {match[1]}
      </strong>
    )
    lastIndex = regex.lastIndex
  }

  // Add remaining text
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex))
  }

  return parts.length > 0 ? parts : text
}

export default function Comparison() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [docA, setDocA] = useState<Document | null>(null)
  const [docB, setDocB] = useState<Document | null>(null)
  const [comparison, setComparison] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const docs = await documentService.list()
      setDocuments(docs)
    } catch (error) {
      console.error('Error loading documents:', error)
    }
  }

  const handleCompare = async () => {
    if (!docA || !docB) return

    setLoading(true)
    try {
      const result = await analysisService.compareDocuments(docA.id, docB.id)
      setComparison(result)
    } catch (error) {
      console.error('Error comparing documents:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Comparação de Contratos</h2>

      <Card className="p-6">
        <div className="grid md:grid-cols-3 gap-6 items-center">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Documento A
            </label>
            <select
              value={docA?.id || ''}
              onChange={(e) => {
                const doc = documents.find(d => d.id === e.target.value)
                if (doc) setDocA(doc)
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            >
              <option value="">Selecione...</option>
              {documents.map((doc) => (
                <option key={doc.id} value={doc.id}>
                  {doc.title}
                </option>
              ))}
            </select>
          </div>

          <div className="flex justify-center">
            <ArrowRight className="w-6 h-6 text-gray-400" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Documento B
            </label>
            <select
              value={docB?.id || ''}
              onChange={(e) => {
                const doc = documents.find(d => d.id === e.target.value)
                if (doc) setDocB(doc)
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            >
              <option value="">Selecione...</option>
              {documents.map((doc) => (
                <option key={doc.id} value={doc.id}>
                  {doc.title}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="mt-6">
          <Button
            onClick={handleCompare}
            disabled={!docA || !docB || loading}
            className="w-full"
          >
            <GitCompare className="w-4 h-4 mr-2" />
            {loading ? 'Comparando...' : 'Comparar Documentos'}
          </Button>
        </div>
      </Card>

      {comparison && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Resultado da Comparação</h3>
          <div className="text-gray-700 space-y-4">
            {comparison.summary.split('\n').map((line: string, idx: number) => (
              <p key={idx} className="whitespace-pre-wrap">
                {parseMarkdown(line)}
              </p>
            ))}
          </div>
        </Card>
      )}
    </div>
  )
}

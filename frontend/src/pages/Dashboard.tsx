import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { documentService } from '../services/documentService'
import type { Document } from '../types'
import { FileText, Trash2, Upload } from 'lucide-react'

export default function Dashboard() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const docs = await documentService.list()
      setDocuments(docs)
    } catch (error) {
      console.error('Error loading documents:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (confirm('Tem certeza que deseja excluir este documento?')) {
      try {
        await documentService.delete(id)
        loadDocuments()
      } catch (error) {
        console.error('Error deleting document:', error)
      }
    }
  }

  if (loading) {
    return <div className="text-center py-12">Carregando...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Documentos</h2>
        <Button onClick={() => navigate('/upload')}>
          <Upload className="w-4 h-4 mr-2" />
          Upload PDF
        </Button>
      </div>

      {documents.length === 0 ? (
        <Card className="p-12 text-center">
          <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhum documento encontrado
          </h3>
          <p className="text-gray-500 mb-4">
            Faça upload de um contrato PDF para começar
          </p>
          <Button onClick={() => navigate('/upload')}>
            <Upload className="w-4 h-4 mr-2" />
            Upload PDF
          </Button>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {documents.map((doc) => (
            <Card key={doc.id} className="p-6">
              <div className="flex items-start justify-between mb-4">
                <FileText className="w-8 h-8 text-blue-600" />
                <span
                  className={`px-2 py-1 text-xs font-medium rounded-full ${
                    doc.status === 'ready'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}
                >
                  {doc.status === 'ready' ? 'Pronto' : 'Processando'}
                </span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">{doc.title}</h3>
              <p className="text-sm text-gray-500 mb-4">{doc.filename}</p>
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span>{doc.page_count || '-'} páginas</span>
                <span>{new Date(doc.created_at).toLocaleDateString('pt-BR')}</span>
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => navigate(`/chat?doc=${doc.id}`)}
                >
                  Chat
                </Button>
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => navigate(`/analysis?doc=${doc.id}`)}
                >
                  Análise
                </Button>
                <Button
                  variant="outline"
                  onClick={() => handleDelete(doc.id)}
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

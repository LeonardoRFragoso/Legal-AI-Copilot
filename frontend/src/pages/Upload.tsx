import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import { documentService } from '../services/documentService'
import { Upload as UploadIcon, CheckCircle } from 'lucide-react'

export default function Upload() {
  const [title, setTitle] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [success, setSuccess] = useState(false)
  const navigate = useNavigate()

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file || !title) return

    setUploading(true)
    try {
      await documentService.upload(title, file)
      setSuccess(true)
      setTimeout(() => {
        navigate('/dashboard')
      }, 2000)
    } catch (error) {
      console.error('Error uploading document:', error)
      alert('Erro ao fazer upload do documento')
    } finally {
      setUploading(false)
    }
  }

  if (success) {
    return (
      <Card className="max-w-md mx-auto p-8 text-center">
        <CheckCircle className="w-16 h-16 mx-auto text-green-600 mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Upload realizado com sucesso!
        </h2>
        <p className="text-gray-500">Redirecionando para o dashboard...</p>
      </Card>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload de Contrato</h2>
      <Card className="p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Título do Documento
            </label>
            <Input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Ex: Contrato de Prestação de Serviços"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Arquivo PDF
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer"
              >
                <UploadIcon className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                {file ? (
                  <p className="text-gray-900 font-medium">{file.name}</p>
                ) : (
                  <>
                    <p className="text-gray-900 font-medium">
                      Clique para selecionar um arquivo
                    </p>
                    <p className="text-gray-500 text-sm mt-1">
                      ou arraste e solte aqui
                    </p>
                  </>
                )}
              </label>
            </div>
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={!file || !title || uploading}
          >
            {uploading ? 'Processando...' : 'Fazer Upload'}
          </Button>
        </form>
      </Card>
    </div>
  )
}

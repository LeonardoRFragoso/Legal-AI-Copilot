export interface Document {
  id: string
  title: string
  filename: string
  status: string
  page_count?: number
  created_at: string
}

export interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  citations?: any[]
  created_at: string
}

export interface Conversation {
  id: string
  document_id?: string
  title?: string
  created_at: string
}

export interface ExtractionData {
  parties: string[]
  dates: string[]
  values: string[]
  clauses: string[]
}

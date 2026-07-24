import { useEffect, useState, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Textarea from '../components/ui/Textarea'
import { chatService } from '../services/chatService'
import type { Message, Conversation } from '../types'
import { Send, MessageSquare, Plus } from 'lucide-react'

export default function Chat() {
  const [searchParams] = useSearchParams()
  const convId = searchParams.get('conv')
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadConversations()
  }, [])

  useEffect(() => {
    if (convId && conversations.length > 0) {
      const conv = conversations.find(c => c.id === convId)
      if (conv) {
        setSelectedConversation(conv)
      }
    }
  }, [convId, conversations])

  useEffect(() => {
    if (selectedConversation) {
      loadMessages(selectedConversation.id)
    }
  }, [selectedConversation])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const loadConversations = async () => {
    try {
      const convs = await chatService.listConversations()
      setConversations(convs)
      if (convs.length > 0 && !selectedConversation) {
        setSelectedConversation(convs[0])
      }
    } catch (error) {
      console.error('Error loading conversations:', error)
    }
  }

  const loadMessages = async (conversationId: string) => {
    try {
      const msgs = await chatService.getMessages(conversationId)
      setMessages(msgs)
    } catch (error) {
      console.error('Error loading messages:', error)
    }
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleNewConversation = async () => {
    try {
      const newConv = await chatService.createConversation(undefined, 'Nova Conversa')
      setConversations([newConv, ...conversations])
      setSelectedConversation(newConv)
      setMessages([])
    } catch (error) {
      console.error('Error creating conversation:', error)
    }
  }

  const handleSendMessage = async () => {
    if (!input.trim() || !selectedConversation || loading) return

    setLoading(true)
    try {
      const userMsg = await chatService.sendMessage(selectedConversation.id, input)
      setMessages([...messages, userMsg])
      setInput('')
      
      // Reload messages to get the assistant response
      setTimeout(async () => {
        await loadMessages(selectedConversation.id)
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error sending message:', error)
      setLoading(false)
    }
  }

  return (
    <div className="flex gap-6 h-[calc(100vh-200px)]">
      <div className="w-64">
        <Card className="p-4 h-full">
          <Button onClick={handleNewConversation} className="w-full mb-4">
            <Plus className="w-4 h-4 mr-2" />
            Nova Conversa
          </Button>
          <div className="space-y-2 overflow-y-auto max-h-[calc(100%-60px)]">
            {conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => setSelectedConversation(conv)}
                className={`w-full text-left p-3 rounded-lg transition-colors ${
                  selectedConversation?.id === conv.id
                    ? 'bg-blue-50 text-blue-900'
                    : 'hover:bg-gray-50'
                }`}
              >
                <div className="font-medium truncate">{conv.title || 'Nova Conversa'}</div>
                <div className="text-xs text-gray-500">
                  {new Date(conv.created_at).toLocaleDateString('pt-BR')}
                </div>
              </button>
            ))}
          </div>
        </Card>
      </div>

      <div className="flex-1 flex flex-col">
        <Card className="flex-1 flex flex-col p-4">
          <div className="flex-1 overflow-y-auto mb-4 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 py-12">
                <MessageSquare className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <p>Inicie uma conversa sobre o documento</p>
              </div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${
                    msg.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <Card
                    className={`max-w-[80%] p-4 ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-300">
                        <div className="text-xs font-medium">Citações:</div>
                        {msg.citations.map((citation, i) => (
                          <div key={i} className="text-xs mt-1 opacity-80">
                            {citation.text?.substring(0, 100)}...
                          </div>
                        ))}
                      </div>
                    )}
                  </Card>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="flex gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSendMessage()
                }
              }}
              placeholder="Digite sua pergunta sobre o contrato..."
              className="flex-1"
              rows={2}
            />
            <Button onClick={handleSendMessage} disabled={loading}>
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </Card>
      </div>
    </div>
  )
}

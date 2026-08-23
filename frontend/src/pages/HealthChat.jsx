import { useState, useEffect, useRef } from 'react'
import { Send, MessageSquare, Bot, User } from 'lucide-react'
import api from '../utils/api'

const HealthChat = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages([...messages, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.post('/chat/query', { question: input })
      const botMessage = { 
        role: 'assistant', 
        content: response.data.answer,
        sources: response.data.sources
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Chat failed:', error)
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Health Chat</h1>
        <p className="mt-2 text-gray-600">Ask health questions to our AI assistant</p>
      </div>

      <div className="card h-[600px] flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <Bot className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">
                  Start a conversation by asking a health-related question
                </p>
                <div className="mt-4 space-y-2">
                  <p className="text-sm text-gray-500">Try asking:</p>
                  <div className="space-y-1">
                    <button
                      onClick={() => setInput('What are the symptoms of diabetes?')}
                      className="block w-full text-left text-sm text-primary-600 hover:text-primary-700"
                    >
                      What are the symptoms of diabetes?
                    </button>
                    <button
                      onClick={() => setInput('How can I reduce my blood pressure naturally?')}
                      className="block w-full text-left text-sm text-primary-600 hover:text-primary-700"
                    >
                      How can I reduce my blood pressure naturally?
                    </button>
                    <button
                      onClick={() => setInput('What foods are good for heart health?')}
                      className="block w-full text-left text-sm text-primary-600 hover:text-primary-700"
                    >
                      What foods are good for heart health?
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`flex items-start space-x-3 max-w-[80%] ${
                    msg.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                  }`}
                >
                  <div
                    className={`p-2 rounded-full ${
                      msg.role === 'user' ? 'bg-primary-100' : 'bg-green-100'
                    }`}
                  >
                    {msg.role === 'user' ? (
                      <User className="h-5 w-5 text-primary-600" />
                    ) : (
                      <Bot className="h-5 w-5 text-green-600" />
                    )}
                  </div>
                  <div
                    className={`p-3 rounded-lg ${
                      msg.role === 'user'
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p className="text-sm">{msg.content}</p>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <p className="text-xs text-gray-500">Sources: {msg.sources.length}</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="flex justify-start">
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-full bg-green-100">
                  <Bot className="h-5 w-5 text-green-600" />
                </div>
                <div className="p-3 rounded-lg bg-gray-100">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t p-4">
          <div className="flex space-x-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a health question..."
              className="flex-1 input-field"
              disabled={loading}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed px-4"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Disclaimer: This is not medical advice. Please consult a healthcare professional.
          </p>
        </div>
      </div>
    </div>
  )
}

export default HealthChat

import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Loader2, Sparkles } from 'lucide-react';
import { createChatSession, sendMessageStream } from '../services/geminiService';
import { ChatMessage } from '../types';
import { Chat, GenerateContentResponse } from '@google/genai';

const AiAssistant: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'model', text: 'Welcome to Sahwan Law. How may I assist you with your legal inquiries today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatSessionRef = useRef<Chat | null>(null);

  // Initialize chat session once
  useEffect(() => {
    try {
        chatSessionRef.current = createChatSession();
    } catch (e) {
        console.error("Failed to init chat", e);
    }
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !chatSessionRef.current) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setIsLoading(true);

    try {
      // Add a placeholder for the model response
      setMessages(prev => [...prev, { role: 'model', text: '', isStreaming: true }]);

      const stream = await sendMessageStream(chatSessionRef.current, userMsg);
      
      let fullText = '';
      
      for await (const chunk of stream) {
        const c = chunk as GenerateContentResponse;
        if (c.text) {
            fullText += c.text;
            setMessages(prev => {
                const newMessages = [...prev];
                const lastMsg = newMessages[newMessages.length - 1];
                if (lastMsg.role === 'model' && lastMsg.isStreaming) {
                    lastMsg.text = fullText;
                }
                return newMessages;
            });
        }
      }

      // Mark streaming as done
      setMessages(prev => {
        const newMessages = [...prev];
        const lastMsg = newMessages[newMessages.length - 1];
        lastMsg.isStreaming = false;
        return newMessages;
      });

    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { role: 'model', text: "I apologize, but I'm having trouble connecting right now. Please try again later or contact our office directly." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed bottom-6 right-6 z-50 p-4 rounded-full shadow-2xl transition-all duration-300 hover:scale-105 flex items-center justify-center
          ${isOpen ? 'bg-charcoal-900 rotate-90' : 'bg-accent text-white hover:bg-accent-dark'}`}
      >
        {isOpen ? <X size={24} className="text-white" /> : <MessageSquare size={24} />}
      </button>

      {/* Chat Window */}
      <div 
        className={`fixed bottom-24 right-6 w-[90vw] md:w-96 bg-white rounded-2xl shadow-2xl border border-gray-100 z-50 transition-all duration-300 origin-bottom-right transform flex flex-col overflow-hidden
        ${isOpen ? 'scale-100 opacity-100 translate-y-0' : 'scale-90 opacity-0 translate-y-10 pointer-events-none'}`}
        style={{ maxHeight: 'calc(100vh - 120px)', height: '500px' }}
      >
        {/* Header */}
        <div className="bg-charcoal-900 p-4 flex items-center gap-3">
            <div className="bg-accent/20 p-2 rounded-lg">
                <Sparkles size={18} className="text-accent" />
            </div>
            <div>
                <h3 className="text-white font-serif font-medium">Sahwan AI Assistant</h3>
                <p className="text-gray-400 text-xs">Always here to help</p>
            </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-pearl">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] p-3 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-accent text-white rounded-br-none'
                    : 'bg-white text-charcoal border border-gray-100 rounded-bl-none shadow-sm'
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} className="p-3 bg-white border-t border-gray-100 flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your inquiry..."
            className="flex-1 bg-pearl rounded-full px-4 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-accent text-charcoal"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="p-2.5 bg-charcoal-900 text-white rounded-full hover:bg-black disabled:opacity-50 transition-colors"
          >
            {isLoading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
          </button>
        </form>
      </div>
    </>
  );
};

export default AiAssistant;
import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../LanguageContext';
import { Mic, MicOff, Send, Volume2, Square } from 'lucide-react';

export default function TeammateSeams() {
  const { language, t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const recognitionRef = useRef(null);
  const synthRef = useRef(window.speechSynthesis);
  const messagesEndRef = useRef(null);

  // Initialize greeting on language change
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{ role: 'assistant', content: t('chat_greeting') }]);
    }
  }, [language, t]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Map our language codes to browser Speech API language codes
  const getSpeechLangCode = (lang) => {
    const map = { hi: 'hi-IN', mr: 'mr-IN', en: 'en-IN' };
    return map[lang] || 'en-US';
  };

  // --- SPEECH TO TEXT (MIC INPUT) ---
  const toggleRecording = () => {
    if (isRecording) {
      recognitionRef.current?.stop();
      setIsRecording(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser does not support voice input. Please use Chrome.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = getSpeechLangCode(language);
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      // We don't auto-send, so the user can verify the text first
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error", event.error);
      setIsRecording(false);
    };

    recognition.onend = () => {
      setIsRecording(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
    setIsRecording(true);
  };

  // --- TEXT TO SPEECH (AUDIO OUTPUT) ---
  const speakMessage = (text) => {
    if (synthRef.current.speaking) {
      synthRef.current.cancel();
    }
    
    setIsSpeaking(true);
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = getSpeechLangCode(language);
    
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    
    synthRef.current.speak(utterance);
  };

  const stopSpeaking = () => {
    synthRef.current.cancel();
    setIsSpeaking(false);
  };

  // --- API CALL TO BACKEND ---
  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userText = input.trim();
    setInput('');
    
    const newMessages = [...messages, { role: 'user', content: userText }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      // Send the entire chat history to our FastAPI backend
      const response = await fetch('http://127.0.0.1:8000/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages,
          language: language
        })
      });

      if (!response.ok) throw new Error('Failed to fetch from API');

      const data = await response.json();
      const replyText = data.reply;

      setMessages((prev) => [...prev, { role: 'assistant', content: replyText }]);
      
      // Auto-read the reply out loud!
      speakMessage(replyText);

    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [...prev, { role: 'assistant', content: "Sorry, I am having trouble connecting to the server right now." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex flex-col h-[600px]">
      
      {/* Header */}
      <div className="flex items-center justify-between mb-4 border-b pb-2">
        <h2 className="font-bold text-slate-800 text-lg flex items-center gap-2">
          {t('nav_chat')}
        </h2>
        {isSpeaking && (
          <button onClick={stopSpeaking} className="text-red-500 flex items-center gap-1 text-sm bg-red-50 px-2 py-1 rounded">
            <Square className="w-4 h-4 fill-current" /> {t('stop_speaking')}
          </button>
        )}
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-2xl p-3 shadow-sm relative group ${
              msg.role === 'user' 
                ? 'bg-emerald-600 text-white rounded-br-none' 
                : 'bg-slate-100 text-slate-800 rounded-bl-none'
            }`}>
              {msg.content}
              
              {/* Tap to listen button on bot messages */}
              {msg.role === 'assistant' && (
                <button 
                  onClick={() => speakMessage(msg.content)}
                  className="absolute -right-8 top-2 text-slate-400 hover:text-emerald-600 opacity-0 group-hover:opacity-100 transition-opacity"
                  title="Listen"
                >
                  <Volume2 className="w-5 h-5" />
                </button>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-100 text-slate-500 rounded-2xl rounded-bl-none p-3 text-sm italic">
              {t('loading')}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSend} className="flex gap-2 items-center bg-slate-50 p-2 rounded-xl border border-slate-200">
        
        {/* Voice Input Button */}
        <button
          type="button"
          onClick={toggleRecording}
          className={`p-3 rounded-full transition-colors ${
            isRecording ? 'bg-red-500 text-white animate-pulse' : 'bg-slate-200 text-slate-600 hover:bg-slate-300'
          }`}
          title={t('speak')}
        >
          {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
        </button>

        {/* Text Input */}
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={isRecording ? "Listening..." : t('type_message')}
          className="flex-1 bg-transparent px-2 py-2 outline-none text-slate-700"
          disabled={isLoading}
        />

        {/* Send Button */}
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="p-3 bg-emerald-600 text-white rounded-full hover:bg-emerald-700 disabled:opacity-50 transition-colors"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>
    </div>
  );
}

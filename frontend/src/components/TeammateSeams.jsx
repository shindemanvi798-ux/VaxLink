import React, { useState } from 'react';

export default function TeammateSeams() {
  const [activeLang, setActiveLang] = useState('hi');
  const [recording, setRecording] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Namaste! Main VaxLink AI Sahayak hoon. Aap bacche ke teekakaran (vaccination) ke baare mein koi bhi sawal pooch sakte hain.' }
  ]);
  const [input, setInput] = useState('');

  const languages = [
    { code: 'hi', name: 'हिंदी (Hindi)' },
    { code: 'mr', name: 'मराठी (Marathi)' },
    { code: 'ta', name: 'தமிழ் (Tamil)' },
    { code: 'te', name: 'తెలుగు (Telugu)' },
    { code: 'en', name: 'English' }
  ];

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = input.trim();
    setMessages((prev) => [
      ...prev,
      { sender: 'user', text: userMsg },
      { sender: 'bot', text: `[Voice & AI Integration Seam]: Received query "${userMsg}" in ${activeLang.toUpperCase()}. Person 2 LLM/Voice service plugs in here.` }
    ]);
    setInput('');
  };

  const toggleVoice = () => {
    setRecording(!recording);
  };

  return (
    <div className="space-y-6">
      {/* Multilingual Selector Container */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
            <span>🌐</span> Language Preference (Person 2 Multilingual i18n Integration)
          </h3>
          <span className="text-[10px] bg-indigo-50 text-indigo-700 font-semibold px-2 py-0.5 rounded border border-indigo-200">
            Person 2 Plug-in Ready
          </span>
        </div>
        <div className="flex flex-wrap gap-2">
          {languages.map((l) => (
            <button
              key={l.code}
              onClick={() => setActiveLang(l.code)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg border transition ${
                activeLang === l.code
                  ? 'bg-emerald-600 text-white border-emerald-600 shadow-sm'
                  : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
              }`}
            >
              {l.name}
            </button>
          ))}
        </div>
      </div>

      {/* Voice Assistant & Health Q&A AI Container */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
            <span>🎙️</span> Multilingual Voice Assistant & Health Q&A
          </h3>
          <span className="text-[10px] bg-purple-50 text-purple-700 font-semibold px-2 py-0.5 rounded border border-purple-200">
            Voice-First AI Assistant
          </span>
        </div>

        {/* Chat window */}
        <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 h-64 overflow-y-auto space-y-3 mb-4">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl p-3 text-xs shadow-sm ${
                  m.sender === 'user'
                    ? 'bg-emerald-600 text-white rounded-br-none'
                    : 'bg-white text-slate-800 border border-slate-200 rounded-bl-none'
                }`}
              >
                {m.text}
              </div>
            </div>
          ))}
        </div>

        {/* Voice and input controls */}
        <form onSubmit={handleSend} className="flex gap-2">
          <button
            type="button"
            onClick={toggleVoice}
            className={`p-2.5 rounded-xl text-white font-bold transition flex items-center justify-center ${
              recording
                ? 'bg-rose-600 animate-bounce'
                : 'bg-indigo-600 hover:bg-indigo-700'
            }`}
            title="Click to speak (Voice-First Input)"
          >
            {recording ? '🛑 Speaking...' : '🎙️ Voice'}
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask health question in ${languages.find(l=>l.code===activeLang)?.name}...`}
            className="flex-1 px-3 py-2 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

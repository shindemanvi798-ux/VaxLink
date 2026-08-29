import React from 'react';

export default function Navigation({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'home', label: 'Home', icon: '🏠' },
    { id: 'schedule', label: 'Schedule', icon: '📋' },
    { id: 'camps', label: 'Find Camps', icon: '🏥' },
    { id: 'assist', label: 'Voice & AI', icon: '🎙️' }
  ];

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-14 z-30 shadow-sm">
      <div className="max-w-4xl mx-auto px-4 flex justify-around sm:justify-start sm:space-x-8">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-3 px-3 font-semibold text-sm flex items-center space-x-2 border-b-2 transition-colors ${
                isActive
                  ? 'border-emerald-600 text-emerald-700'
                  : 'border-transparent text-slate-500 hover:text-slate-800'
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}

import React from 'react';

export default function Header({ childrenList, selectedChildId, onSelectChild, onOpenAddModal }) {
  return (
    <header className="bg-emerald-700 text-white shadow-md sticky top-0 z-40">
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-white text-emerald-800 font-black px-3 py-1 rounded-lg text-xl tracking-tight shadow">
            Vax<span className="text-emerald-600">Link</span>
          </div>
          <div className="hidden sm:block text-xs text-emerald-100 border-l border-emerald-500 pl-3">
            Vaccination & Health Companion for India
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {childrenList && childrenList.length > 0 && (
            <div className="flex items-center bg-emerald-800 text-emerald-100 rounded-lg px-2 py-1 text-sm border border-emerald-600">
              <span className="hidden md:inline mr-2 text-xs text-emerald-300">Child:</span>
              <select
                value={selectedChildId || ''}
                onChange={(e) => onSelectChild(e.target.value)}
                className="bg-transparent text-white font-semibold focus:outline-none cursor-pointer"
              >
                {childrenList.map((c) => (
                  <option key={c.id} value={c.id} className="text-gray-800">
                    {c.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          <button
            onClick={onOpenAddModal}
            className="bg-emerald-500 hover:bg-emerald-400 text-white font-medium text-xs sm:text-sm px-3 py-1.5 rounded-lg shadow transition flex items-center space-x-1"
          >
            <span>+ Add Child</span>
          </button>
        </div>
      </div>
    </header>
  );
}

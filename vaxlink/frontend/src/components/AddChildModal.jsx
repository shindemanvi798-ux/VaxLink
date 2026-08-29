import React, { useState } from 'react';

export default function AddChildModal({ isOpen, onClose, onAddSuccess }) {
  const [name, setName] = useState('');
  const [dob, setDob] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Please enter the child\'s name');
      return;
    }
    if (!dob) {
      setError('Please select the date of birth');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await onAddSuccess(name.trim(), dob);
      setName('');
      setDob('');
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to add child');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl relative animate-in fade-in zoom-in duration-150">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 font-bold text-xl"
        >
          &times;
        </button>

        <h2 className="text-xl font-bold text-slate-800 mb-1 flex items-center gap-2">
          <span>👶</span> Add Child Profile
        </h2>
        <p className="text-xs text-slate-500 mb-5">
          Enter your child's date of birth to automatically generate their UIP vaccination schedule.
        </p>

        {error && (
          <div className="bg-rose-50 text-rose-700 text-xs p-3 rounded-lg border border-rose-200 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Child's Full Name *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Aarav Sharma"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none text-sm text-slate-800"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Date of Birth *
            </label>
            <input
              type="date"
              value={dob}
              onChange={(e) => setDob(e.target.value)}
              max={new Date().toISOString().split('T')[0]}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none text-sm text-slate-800"
              required
            />
          </div>

          <div className="pt-2 flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-md transition disabled:opacity-50"
            >
              {loading ? 'Generating Schedule...' : 'Save & Calculate Schedule'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

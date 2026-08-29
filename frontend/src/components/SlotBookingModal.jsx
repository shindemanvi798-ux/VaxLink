import React, { useState } from 'react';

export default function SlotBookingModal({ isOpen, onClose, camp, slot, child, onConfirmBooking }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen || !camp || !slot || !child) return null;

  const handleBooking = async () => {
    setLoading(true);
    setError(null);
    try {
      await onConfirmBooking(camp.id, slot.id, child.id);
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to book vaccination slot');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 font-bold text-xl"
        >
          &times;
        </button>

        <h2 className="text-xl font-bold text-slate-800 mb-1 flex items-center gap-2">
          <span>📅</span> Confirm Slot Booking
        </h2>
        <p className="text-xs text-slate-500 mb-4">
          Please review the details before confirming your appointment.
        </p>

        {error && (
          <div className="bg-rose-50 text-rose-700 text-xs p-3 rounded-lg border border-rose-200 mb-4">
            {error}
          </div>
        )}

        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2 mb-5 text-xs text-slate-700">
          <div className="flex justify-between border-b border-slate-200 pb-2">
            <span className="text-slate-500">Child:</span>
            <strong className="text-slate-800 font-bold text-sm">{child.name}</strong>
          </div>
          <div className="flex justify-between border-b border-slate-200 pb-2">
            <span className="text-slate-500">Health Center:</span>
            <strong className="text-slate-800">{camp.name}</strong>
          </div>
          <div className="flex justify-between border-b border-slate-200 pb-2">
            <span className="text-slate-500">Location:</span>
            <span className="text-slate-800 text-right max-w-[200px]">{camp.location}</span>
          </div>
          <div className="flex justify-between border-b border-slate-200 pb-2">
            <span className="text-slate-500">Date:</span>
            <strong className="text-slate-800">{new Date(camp.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}</strong>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Time Window:</span>
            <strong className="text-emerald-700 font-bold">{slot.time_range}</strong>
          </div>
        </div>

        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg"
          >
            Cancel
          </button>
          <button
            onClick={handleBooking}
            disabled={loading}
            className="px-5 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-md transition disabled:opacity-50"
          >
            {loading ? 'Booking...' : 'Confirm Appointment ✓'}
          </button>
        </div>
      </div>
    </div>
  );
}

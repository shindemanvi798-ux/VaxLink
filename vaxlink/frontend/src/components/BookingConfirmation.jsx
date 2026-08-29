import React from 'react';

export default function BookingConfirmation({ booking, onBackToHome }) {
  if (!booking) return null;

  return (
    <div className="max-w-xl mx-auto bg-white rounded-2xl border border-emerald-200 shadow-lg p-6 sm:p-8 text-center animate-in fade-in zoom-in duration-200">
      <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto text-3xl mb-4 shadow-inner">
        ✓
      </div>

      <h2 className="text-2xl font-black text-slate-800 mb-1">
        Booking Confirmed!
      </h2>
      <p className="text-xs text-slate-500 mb-6">
        Your vaccination appointment slot has been reserved. Please show this token at the health center.
      </p>

      {/* Reference Code Card */}
      <div className="bg-emerald-50 border-2 border-dashed border-emerald-300 rounded-2xl p-4 mb-6">
        <div className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">
          Appointment Reference Code
        </div>
        <div className="text-3xl font-black text-emerald-700 tracking-wider my-1">
          {booking.reference_code}
        </div>
        <div className="text-[11px] text-emerald-600">
          Status: <span className="font-bold uppercase">{booking.status}</span>
        </div>
      </div>

      {/* Booking Details Table */}
      <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 text-left text-xs space-y-2 mb-6">
        <div className="flex justify-between border-b border-slate-200 pb-2">
          <span className="text-slate-500">Child Name:</span>
          <strong className="text-slate-800 font-bold">{booking.child_name}</strong>
        </div>
        <div className="flex justify-between border-b border-slate-200 pb-2">
          <span className="text-slate-500">Center:</span>
          <strong className="text-slate-800">{booking.camp_name}</strong>
        </div>
        <div className="flex justify-between border-b border-slate-200 pb-2">
          <span className="text-slate-500">Address:</span>
          <span className="text-slate-800 text-right max-w-[220px]">{booking.camp_location}</span>
        </div>
        <div className="flex justify-between border-b border-slate-200 pb-2">
          <span className="text-slate-500">Date:</span>
          <strong className="text-slate-800">{new Date(booking.date).toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })}</strong>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-500">Time Window:</span>
          <strong className="text-emerald-700 font-bold">{booking.time_slot}</strong>
        </div>
      </div>

      <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-left text-xs text-amber-800 mb-6 flex items-start gap-2">
        <span className="text-base">💡</span>
        <div>
          <strong>ASHA Worker Tip:</strong> Please bring your child's Mother & Child Protection (MCP) card if available. No fee is required at government PHC camps.
        </div>
      </div>

      <button
        onClick={onBackToHome}
        className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 px-6 rounded-xl shadow-md transition text-sm"
      >
        ← Return to Dashboard
      </button>
    </div>
  );
}

import React from 'react';

export default function ChildProfile({ scheduleData, onBookVaccine }) {
  if (!scheduleData) {
    return (
      <div className="p-8 text-center text-slate-500 text-sm">
        Loading schedule...
      </div>
    );
  }

  const { child_name, age_months, progress_percentage, next_vaccine, doses } = scheduleData;

  const getStatusBadge = (status) => {
    switch (status) {
      case 'done':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
            ✓ Done
          </span>
        );
      case 'due':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300 animate-pulse">
            ⚠ Due Now
          </span>
        );
      case 'missed':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300">
            ❌ Overdue
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
            ○ Upcoming
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Child Overview Card */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-2xl font-bold text-slate-800">{child_name}</h2>
              <span className="bg-emerald-50 text-emerald-700 text-xs px-2.5 py-1 rounded-full font-semibold border border-emerald-200">
                {age_months} {age_months === 1 ? 'month' : 'months'} old
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              DOB: {new Date(scheduleData.dob).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
            </p>
          </div>

          <div className="w-full sm:w-48 text-right">
            <div className="flex justify-between items-center text-xs font-bold text-slate-700 mb-1">
              <span>Overall Protection</span>
              <span className="text-emerald-700">{progress_percentage}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-3 border border-slate-200 overflow-hidden">
              <div
                className="bg-emerald-600 h-full rounded-full transition-all duration-500"
                style={{ width: `${progress_percentage}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Next Vaccine Spotlight */}
        {next_vaccine && (
          <div className="mt-5 p-4 bg-emerald-50/80 border border-emerald-200 rounded-xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <div className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">
                Next Recommended Dose
              </div>
              <div className="text-base font-bold text-slate-800 mt-0.5">
                {next_vaccine.name}
              </div>
              <p className="text-xs text-slate-600 mt-0.5">
                Timing: <span className="font-semibold">{next_vaccine.due_timing_label}</span> ({new Date(next_vaccine.due_date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })})
              </p>
            </div>
            <button
              onClick={() => onBookVaccine(next_vaccine)}
              className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs px-4 py-2 rounded-lg shadow transition whitespace-nowrap self-stretch sm:self-auto text-center"
            >
              Book Camp Slot →
            </button>
          </div>
        )}
      </div>

      {/* Vaccination Schedule Table / Cards */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
            <span>🗓️</span> Universal Immunization Schedule
          </h3>
          <span className="text-xs text-slate-500">
            Source: Universal Immunization Programme (UIP) India
          </span>
        </div>

        <div className="divide-y divide-slate-100">
          {doses.map((dose, idx) => (
            <div
              key={idx}
              className={`p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-slate-50 transition ${
                dose.status === 'due' ? 'bg-amber-50/40' : ''
              }`}
            >
              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-slate-800 text-sm">{dose.name}</span>
                  {getStatusBadge(dose.status)}
                </div>
                <p className="text-xs text-slate-500 mt-1">{dose.description}</p>
                <div className="flex items-center gap-4 text-xs text-slate-400 mt-1">
                  <span>Due Window: <strong className="text-slate-600">{dose.due_timing_label}</strong></span>
                  <span>Calculated Date: <strong className="text-slate-600">{new Date(dose.due_date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}</strong></span>
                </div>
              </div>

              {(dose.status === 'due' || dose.status === 'missed') && (
                <button
                  onClick={() => onBookVaccine(dose)}
                  className="text-xs bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-3 py-1.5 rounded-lg shadow-sm self-start sm:self-center transition"
                >
                  Find Camp & Book
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

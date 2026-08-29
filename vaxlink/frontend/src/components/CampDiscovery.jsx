import React from 'react';

export default function CampDiscovery({ camps, onSelectSlot }) {
  const getCrowdBadge = (status) => {
    switch (status) {
      case 'LOW':
        return (
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-extrabold bg-emerald-100 text-emerald-800 border border-emerald-300">
            🟢 LOW CROWD (&lt;50%)
          </span>
        );
      case 'MEDIUM':
        return (
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-extrabold bg-amber-100 text-amber-800 border border-amber-300">
            🟡 MEDIUM CROWD (50-80%)
          </span>
        );
      case 'HIGH':
        return (
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-extrabold bg-rose-100 text-rose-800 border border-rose-300">
            🔴 HIGH CROWD (&gt;80%)
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-emerald-800 text-white p-5 rounded-2xl shadow-md">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <span>🏥</span> Nearby Vaccination Camps & Crowd Live Status
        </h2>
        <p className="text-xs text-emerald-100 mt-1">
          Real-time crowd visibility helps parents avoid long queues at government primary health centers (PHCs).
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {camps.map((camp) => (
          <div
            key={camp.id}
            className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:shadow-md transition"
          >
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-100 pb-4">
              <div>
                <h3 className="text-lg font-bold text-slate-800">{camp.name}</h3>
                <p className="text-xs text-slate-500 mt-0.5 flex items-center gap-1">
                  <span>📍</span> {camp.location}
                </p>
                <div className="text-xs text-slate-400 mt-1">
                  Date: <strong className="text-slate-700">{new Date(camp.date).toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })}</strong>
                </div>
              </div>

              <div className="flex flex-col items-start sm:items-end gap-1">
                {getCrowdBadge(camp.crowd_status)}
                <span className="text-xs text-slate-500 mt-1">
                  Booked: <strong className="text-slate-800">{camp.total_booked} / {camp.total_capacity}</strong> slots
                </span>
              </div>
            </div>

            {/* Time Slots */}
            <div className="mt-4">
              <h4 className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-3">
                Available Time Slots
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {camp.slots.map((slot) => {
                  const isFull = slot.available_slots <= 0;
                  return (
                    <div
                      key={slot.id}
                      className={`p-3 rounded-xl border flex flex-col justify-between transition ${
                        isFull
                          ? 'bg-slate-50 border-slate-200 opacity-60'
                          : 'bg-emerald-50/50 border-emerald-200 hover:border-emerald-400'
                      }`}
                    >
                      <div>
                        <div className="text-xs font-bold text-slate-800">{slot.time_range}</div>
                        <div className="text-xs text-slate-500 mt-1">
                          {isFull ? (
                            <span className="text-rose-600 font-bold">Fully Booked</span>
                          ) : (
                            <span className="text-emerald-700 font-semibold">{slot.available_slots} slots left</span>
                          )}
                        </div>
                      </div>

                      <button
                        disabled={isFull}
                        onClick={() => onSelectSlot(camp, slot)}
                        className={`mt-3 w-full py-1.5 px-3 rounded-lg text-xs font-bold transition shadow-sm ${
                          isFull
                            ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                            : 'bg-emerald-600 hover:bg-emerald-700 text-white'
                        }`}
                      >
                        {isFull ? 'Full' : 'Book Slot →'}
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

import React from 'react';

export default function HomeDashboard({ selectedChild, scheduleData, camps, onNavigate, onBookVaccine }) {
  if (!selectedChild || !scheduleData) {
    return (
      <div className="p-8 text-center text-slate-500 text-sm">
        Loading dashboard...
      </div>
    );
  }

  const { progress_percentage, next_vaccine, age_months } = scheduleData;
  const lowCrowdCamp = camps.find((c) => c.crowd_status === 'LOW') || camps[0];

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-emerald-800 to-emerald-600 text-white p-6 rounded-2xl shadow-md">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <span className="bg-emerald-900/60 text-emerald-200 text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider">
              VaxLink Health Dashboard
            </span>
            <h1 className="text-2xl font-black mt-1">
              Namaste, Priya! 🙏
            </h1>
            <p className="text-xs text-emerald-100 mt-1 max-w-lg">
              Making child immunization understandable, trackable, and queue-free for your family.
            </p>
          </div>

          <button
            onClick={() => onNavigate('schedule')}
            className="bg-white text-emerald-800 font-bold text-xs px-4 py-2.5 rounded-xl shadow-md hover:bg-emerald-50 transition self-stretch md:self-auto text-center"
          >
            View Full Schedule →
          </button>
        </div>
      </div>

      {/* Child Status Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Protection Score Card */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-3">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                Active Child Profile
              </span>
              <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                {age_months} months old
              </span>
            </div>
            <h2 className="text-xl font-bold text-slate-800">{selectedChild.name}</h2>
            <div className="mt-4">
              <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                <span>Vaccination Completion</span>
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

          <div className="mt-5 pt-3 border-t border-slate-100 flex justify-between items-center text-xs">
            <span className="text-slate-500">Scheduled under UIP India</span>
            <button
              onClick={() => onNavigate('schedule')}
              className="text-emerald-700 font-bold hover:underline"
            >
              See all doses →
            </button>
          </div>
        </div>

        {/* Next Vaccine Action Card */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <span className="text-xs font-bold text-amber-600 uppercase tracking-wider flex items-center gap-1 mb-2">
              <span>⚠️</span> Next Action Required
            </span>
            {next_vaccine ? (
              <>
                <h3 className="text-lg font-bold text-slate-800">{next_vaccine.name}</h3>
                <p className="text-xs text-slate-600 mt-1">{next_vaccine.description}</p>
                <div className="mt-3 bg-amber-50 p-2.5 rounded-lg border border-amber-200 text-xs text-amber-800 font-medium">
                  Due Timing: <strong>{next_vaccine.due_timing_label}</strong> ({new Date(next_vaccine.due_date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })})
                </div>
              </>
            ) : (
              <p className="text-xs text-slate-500 mt-2">All due vaccines up to date!</p>
            )}
          </div>

          <div className="mt-5 pt-3 border-t border-slate-100">
            {next_vaccine ? (
              <button
                onClick={() => onBookVaccine(next_vaccine)}
                className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded-xl shadow transition text-xs text-center"
              >
                Find Camp & Book Slot →
              </button>
            ) : (
              <button
                onClick={() => onNavigate('camps')}
                className="w-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-xl transition text-xs text-center"
              >
                Browse Health Camps
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Live Crowd & Camp Feature Banner */}
      {lowCrowdCamp && (
        <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="text-sm font-bold text-emerald-800">🏥 Nearby Recommended PHC</span>
              <span className="bg-emerald-200 text-emerald-900 text-[10px] font-extrabold px-2 py-0.5 rounded-full">
                🟢 LOW CROWD
              </span>
            </div>
            <div className="font-bold text-slate-800 text-base">{lowCrowdCamp.name}</div>
            <p className="text-xs text-slate-600">{lowCrowdCamp.location}</p>
          </div>

          <button
            onClick={() => onNavigate('camps')}
            className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs px-4 py-2.5 rounded-xl shadow transition self-stretch sm:self-auto text-center"
          >
            Book Slot (&lt; 10 min wait) →
          </button>
        </div>
      )}
    </div>
  );
}

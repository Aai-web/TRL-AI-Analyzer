import React, { useState } from 'react';
import { 
  AlertOctagon, 
  AlertTriangle, 
  CheckCircle, 
  HelpCircle, 
  Flame, 
  ShieldAlert,
  ArrowRight,
  TestTubes,
  Clock
} from 'lucide-react';
import { GapRequirement } from '../types';

interface GapAnalysisViewProps {
  gapAnalysis: GapRequirement[];
  nextTrlBarriers: string[];
  predictedTRL: number;
}

export const GapAnalysisView: React.FC<GapAnalysisViewProps> = ({
  gapAnalysis,
  nextTrlBarriers,
  predictedTRL,
}) => {
  const [statusFilter, setStatusFilter] = useState<'All' | 'Missing' | 'Partially Met' | 'Met'>('All');
  const nextTRL = Math.min(9, predictedTRL + 1);

  // Counts
  const missingCount = gapAnalysis.filter((g) => g.status === 'Missing').length;
  const partialCount = gapAnalysis.filter((g) => g.status === 'Partially Met').length;
  const metCount = gapAnalysis.filter((g) => g.status === 'Met').length;

  const filteredGaps = gapAnalysis.filter((g) => {
    if (statusFilter !== 'All' && g.status !== statusFilter) return false;
    return true;
  });

  return (
    <div className="glass-panel rounded-2xl p-6 border border-navy-700/80 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-navy-700/70">
        <div>
          <div className="flex items-center space-x-2">
            <h3 className="text-lg font-bold text-white flex items-center space-x-2">
              <ShieldAlert className="w-5 h-5 text-amber-400" />
              <span>Intelligent Gap Analysis</span>
            </h3>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-950/70 text-amber-300 border border-amber-500/30 font-mono">
              Next Gate: TRL {nextTRL}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Rigorous requirement audit detecting unfulfilled milestones, technical bottlenecks, and recommended test protocols
          </p>
        </div>

        {/* Status filters */}
        <div className="flex bg-navy-850 p-1 rounded-xl border border-navy-700">
          {(['All', 'Missing', 'Partially Met', 'Met'] as const).map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1 text-xs font-medium rounded-lg transition-all ${
                statusFilter === st
                  ? 'bg-electric-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {st} {st === 'Missing' ? `(${missingCount})` : st === 'Partially Met' ? `(${partialCount})` : ''}
            </button>
          ))}
        </div>
      </div>

      {/* Critical Next-TRL Advancement Blockers Callout */}
      {nextTrlBarriers.length > 0 && (
        <div className="rounded-xl p-4 bg-gradient-to-r from-red-950/40 via-navy-850 to-amber-950/30 border border-red-500/30">
          <div className="flex items-center space-x-2 text-xs font-bold text-red-300 uppercase tracking-wider mb-2">
            <AlertOctagon className="w-4 h-4 text-red-400" />
            <span>Primary Technical Impediments Blocking TRL {nextTRL}</span>
          </div>
          <div className="space-y-1.5">
            {nextTrlBarriers.map((barrier, idx) => (
              <div key={idx} className="flex items-start space-x-2 text-xs text-slate-200">
                <span className="text-red-400 font-bold shrink-0">•</span>
                <span>{barrier}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Requirements List */}
      <div className="space-y-3">
        {filteredGaps.map((item) => {
          const isMissing = item.status === 'Missing';
          const isPartial = item.status === 'Partially Met';
          const isMet = item.status === 'Met';

          const statusBadge = isMissing
            ? 'bg-red-950/80 text-red-300 border-red-500/40'
            : isPartial
            ? 'bg-amber-950/80 text-amber-300 border-amber-500/40'
            : 'bg-emerald-950/80 text-emerald-300 border-emerald-500/40';

          const severityBadge = item.gap_severity === 'Critical'
            ? 'text-red-400 bg-red-950/60 border-red-500/30'
            : item.gap_severity === 'Major'
            ? 'text-amber-400 bg-amber-950/60 border-amber-500/30'
            : 'text-slate-400 bg-navy-800 border-navy-700';

          return (
            <div
              key={item.requirement_id}
              className="bg-navy-850/80 rounded-xl p-4 border border-navy-750 space-y-3"
            >
              {/* Top Row: Title, Target TRL, Badges */}
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-bold px-2 py-0.5 rounded-lg bg-navy-800 text-electric-300 border border-navy-700 font-mono">
                    Target TRL {item.target_trl}
                  </span>
                  <span className="text-xs font-bold text-white">
                    {item.title}
                  </span>
                </div>

                <div className="flex items-center space-x-2">
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${severityBadge}`}>
                    {item.gap_severity} Severity
                  </span>
                  <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${statusBadge}`}>
                    {item.status}
                  </span>
                </div>
              </div>

              {/* Description */}
              <p className="text-xs text-slate-300 leading-relaxed">
                {item.description}
              </p>

              {/* Impediment & Prescriptive Action */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 border-t border-navy-800 text-xs">
                {/* Impediment */}
                <div className="bg-navy-900/60 rounded-lg p-2.5 border border-navy-800">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                    Identified Bottleneck
                  </span>
                  <p className="text-slate-300 text-[11px] leading-relaxed">
                    {item.impediment_explanation}
                  </p>
                </div>

                {/* Recommended Action & Tests */}
                <div className="bg-navy-900/60 rounded-lg p-2.5 border border-navy-800">
                  <span className="text-[11px] font-semibold text-cyan-400 uppercase tracking-wider block mb-1">
                    Recommended Validation Activity
                  </span>
                  <p className="text-slate-200 text-[11px] leading-relaxed mb-1.5">
                    {item.recommended_action}
                  </p>
                  {item.recommended_tests.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-1">
                      {item.recommended_tests.map((t, idx) => (
                        <span key={idx} className="text-[10px] px-2 py-0.5 rounded bg-electric-950 text-cyan-300 border border-electric-500/20 font-mono">
                          {t}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

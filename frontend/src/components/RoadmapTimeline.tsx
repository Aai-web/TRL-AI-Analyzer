import React from 'react';
import { 
  Calendar, 
  Flag, 
  CheckSquare, 
  FileCheck2, 
  Workflow,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { RoadmapPhase } from '../types';

interface RoadmapTimelineProps {
  roadmap: RoadmapPhase[];
  predictedTRL: number;
}

export const RoadmapTimeline: React.FC<RoadmapTimelineProps> = ({
  roadmap,
  predictedTRL,
}) => {
  return (
    <div className="glass-panel rounded-2xl p-6 border border-navy-700/80 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-navy-700/70">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center space-x-2">
            <Workflow className="w-5 h-5 text-electric-400" />
            <span>Prioritized Improvement & De-Risking Roadmap</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Sequential 3-phase progression pathway to advance technology readiness to next qualification levels
          </p>
        </div>

        <span className="text-xs px-2.5 py-1 rounded-full bg-navy-800 text-slate-300 border border-navy-700 font-mono">
          Baseline TRL {predictedTRL} ➔ Goal TRL {Math.min(9, predictedTRL + 2)}
        </span>
      </div>

      {/* 3-Phase Timeline Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 relative">
        {roadmap.map((phase, idx) => {
          const isHighPriority = phase.priority === 'High';
          const priorityStyle = isHighPriority
            ? 'bg-rose-950/70 text-rose-300 border-rose-500/30'
            : phase.priority === 'Medium'
            ? 'bg-amber-950/70 text-amber-300 border-amber-500/30'
            : 'bg-blue-950/70 text-blue-300 border-blue-500/30';

          return (
            <div
              key={phase.phase_id}
              className="bg-navy-850/80 rounded-2xl p-5 border border-navy-700 flex flex-col justify-between hover:border-electric-500/40 transition-all shadow-lg"
            >
              <div>
                {/* Top Badge Row */}
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold px-2.5 py-0.5 rounded-lg bg-electric-950 text-cyan-300 border border-electric-500/30 font-mono">
                    Target TRL {phase.target_trl}
                  </span>
                  <div className="flex items-center space-x-1.5">
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${priorityStyle}`}>
                      {phase.priority} Priority
                    </span>
                  </div>
                </div>

                {/* Phase Name */}
                <h4 className="text-sm font-bold text-white mb-2 leading-snug">
                  {phase.phase_name}
                </h4>

                {/* Timeline Pill */}
                <div className="flex items-center space-x-1.5 text-xs text-cyan-400 font-mono mb-4 bg-navy-900/80 px-2.5 py-1 rounded-lg w-fit border border-navy-800">
                  <Calendar className="w-3.5 h-3.5" />
                  <span>Estimated: {phase.timeline_estimate}</span>
                </div>

                {/* Milestones */}
                <div className="space-y-2 mb-4">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                    Key Milestones
                  </span>
                  <ul className="space-y-1.5">
                    {phase.milestones.map((ms, msIdx) => (
                      <li key={msIdx} className="flex items-start space-x-2 text-xs text-slate-300">
                        <CheckSquare className="w-3.5 h-3.5 text-electric-400 shrink-0 mt-0.5" />
                        <span className="leading-tight">{ms}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Recommended Validation Protocol */}
                <div className="space-y-1.5 mb-4 p-3 rounded-xl bg-navy-900/60 border border-navy-800 text-xs">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                    Recommended Protocol
                  </span>
                  <p className="text-slate-200 text-xs leading-relaxed">
                    {phase.validation_protocol}
                  </p>
                </div>
              </div>

              {/* Deliverables Footer */}
              <div className="pt-3 border-t border-navy-800">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">
                  Required Deliverables
                </span>
                <div className="flex flex-wrap gap-1">
                  {phase.deliverables.map((deliv, dIdx) => (
                    <span
                      key={dIdx}
                      className="text-[10px] px-2 py-0.5 rounded-md bg-navy-800 text-slate-300 border border-navy-700 font-mono"
                    >
                      {deliv}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

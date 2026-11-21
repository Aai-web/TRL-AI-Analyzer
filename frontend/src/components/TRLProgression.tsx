import React, { useState } from 'react';
import { 
  Check, 
  Lock, 
  Target, 
  Sparkles, 
  Info,
  ChevronRight
} from 'lucide-react';

interface TRLProgressionProps {
  currentTRL: number;
  evidenceCounts: Record<number, number>;
  onSelectLevel?: (trl: number) => void;
}

const TRL_STAGES = [
  { level: 1, name: 'Basic Principles', phase: 'Research', desc: 'Scientific research begins translation to applied R&D.' },
  { level: 2, name: 'Concept Formulated', phase: 'Research', desc: 'Practical applications invented; analytical formulations.' },
  { level: 3, name: 'Proof of Concept', phase: 'Feasibility', desc: 'Analytical & experimental critical function validated.' },
  { level: 4, name: 'Lab Breadboard', phase: 'Validation', desc: 'Basic components integrated in laboratory environment.' },
  { level: 5, name: 'Relevant Env.', phase: 'Validation', desc: 'Brassboard tested in simulated operational conditions.' },
  { level: 6, name: 'Model / Prototype', phase: 'Demonstration', desc: 'Representative engineering prototype tested in field.' },
  { level: 7, name: 'Operational Demo', phase: 'Demonstration', desc: 'Operational prototype tested in flight/vehicle/sea.' },
  { level: 8, name: 'Qualified System', phase: 'Pre-Deployment', desc: 'Final system qualified through test & certification.' },
  { level: 9, name: 'Mission Proven', phase: 'Commercial', desc: 'Proven through successful operational missions/fleet.' },
];

export const TRLProgression: React.FC<TRLProgressionProps> = ({
  currentTRL,
  evidenceCounts,
  onSelectLevel,
}) => {
  const [selectedTRL, setSelectedTRL] = useState<number>(currentTRL);
  const activeStage = TRL_STAGES.find((s) => s.level === selectedTRL) || TRL_STAGES[0];

  return (
    <div className="glass-panel rounded-2xl p-6 border border-navy-700/80 shadow-2xl">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-6">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>TRL 1–9 Maturity Progression Track</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Standardized NASA / DoD / ISO 16290 technology readiness continuum
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <span className="flex items-center space-x-1 text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span>Verified</span>
          </span>
          <span className="text-slate-600">•</span>
          <span className="flex items-center space-x-1 text-electric-400">
            <span className="w-2 h-2 rounded-full bg-electric-400" />
            <span>Assessed TRL {currentTRL}</span>
          </span>
          <span className="text-slate-600">•</span>
          <span className="flex items-center space-x-1 text-amber-400">
            <span className="w-2 h-2 rounded-full bg-amber-400" />
            <span>Next Target Gate</span>
          </span>
        </div>
      </div>

      {/* Progression Bar Track */}
      <div className="relative pt-3 pb-4">
        {/* Horizontal connector line */}
        <div className="absolute top-8 left-4 right-4 h-1 bg-navy-800 -translate-y-1/2 rounded-full hidden sm:block" />
        <div 
          className="absolute top-8 left-4 h-1 bg-gradient-to-r from-cyan-500 via-electric-500 to-indigo-500 -translate-y-1/2 rounded-full hidden sm:block transition-all duration-700"
          style={{ width: `${((currentTRL - 1) / 8) * 94}%` }}
        />

        <div className="grid grid-cols-3 sm:grid-cols-9 gap-3 relative z-10">
          {TRL_STAGES.map((stage) => {
            const isVerified = stage.level < currentTRL;
            const isCurrent = stage.level === currentTRL;
            const isNext = stage.level === currentTRL + 1;
            const isSelected = stage.level === selectedTRL;
            const evCount = evidenceCounts[stage.level] || 0;

            let circleStyle = 'bg-navy-850 border-navy-700 text-slate-500';
            if (isCurrent) {
              circleStyle = 'bg-electric-600 border-cyan-400 text-white shadow-glow-blue ring-4 ring-electric-500/30 scale-110';
            } else if (isVerified) {
              circleStyle = 'bg-emerald-950/80 border-emerald-500 text-emerald-400';
            } else if (isNext) {
              circleStyle = 'bg-amber-950/60 border-amber-500/80 text-amber-300 ring-2 ring-amber-500/20';
            }

            return (
              <button
                key={stage.level}
                onClick={() => {
                  setSelectedTRL(stage.level);
                  if (onSelectLevel) onSelectLevel(stage.level);
                }}
                className={`flex flex-col items-center text-center p-2 rounded-xl transition-all ${
                  isSelected ? 'bg-navy-800/90 border border-electric-500/40' : 'hover:bg-navy-850/50'
                }`}
              >
                {/* Node Icon */}
                <div className={`w-9 h-9 rounded-full border-2 flex items-center justify-center font-bold text-xs transition-all ${circleStyle}`}>
                  {isCurrent ? (
                    <Sparkles className="w-4 h-4 text-white animate-pulse" />
                  ) : isVerified ? (
                    <Check className="w-4 h-4" />
                  ) : isNext ? (
                    <Target className="w-4 h-4" />
                  ) : (
                    <span>{stage.level}</span>
                  )}
                </div>

                {/* Level Title */}
                <span className="text-xs font-bold text-white mt-2">
                  TRL {stage.level}
                </span>
                <span className="text-[10px] text-slate-400 truncate max-w-full hidden md:block">
                  {stage.name}
                </span>

                {/* Evidence Badge */}
                {evCount > 0 ? (
                  <span className="mt-1 text-[9px] px-1.5 py-0.2 rounded-full bg-cyan-950/80 text-cyan-300 border border-cyan-500/30 font-mono">
                    {evCount} ev
                  </span>
                ) : (
                  <span className="mt-1 text-[9px] text-slate-600 font-mono">
                    0 ev
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Selected Level Detail Card */}
      <div className="mt-4 p-4 rounded-xl bg-navy-850 border border-navy-700/80 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 rounded-lg bg-electric-600/20 border border-electric-500/30 flex items-center justify-center text-electric-400 shrink-0 mt-0.5">
            <Info className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-sm font-bold text-white">
                TRL {activeStage.level}: {activeStage.name}
              </span>
              <span className="text-[10px] px-2 py-0.2 rounded-full bg-navy-800 text-slate-300 border border-navy-700">
                Phase: {activeStage.phase}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              {activeStage.desc}
            </p>
          </div>
        </div>

        <div className="text-xs text-slate-400 shrink-0">
          <span className="font-semibold text-slate-300">
            {evidenceCounts[activeStage.level] || 0}
          </span> verified statements match this level.
        </div>
      </div>
    </div>
  );
};

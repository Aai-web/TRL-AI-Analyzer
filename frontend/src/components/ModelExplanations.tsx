import React from 'react';
import { 
  BrainCircuit, 
  CheckCircle, 
  AlertTriangle, 
  HelpCircle, 
  Scale, 
  BarChart3,
  ShieldAlert
} from 'lucide-react';
import { ModelExplanation } from '../types';

interface ModelExplanationsProps {
  explanation: ModelExplanation;
  predictedTRL: number;
}

export const ModelExplanations: React.FC<ModelExplanationsProps> = ({
  explanation,
  predictedTRL,
}) => {
  return (
    <div className="glass-panel rounded-2xl p-6 border border-navy-700/80 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-navy-700/70">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center space-x-2">
            <BrainCircuit className="w-5 h-5 text-cyan-400" />
            <span>AI Decision Rationale & Feature Attribution</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Transparent explanation of why TRL {predictedTRL} was predicted and how speculative claims were discounted
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-400">Model Epistemic Uncertainty:</span>
          <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
            explanation.uncertainty_level === 'Low'
              ? 'bg-emerald-950/70 text-emerald-300 border-emerald-500/30'
              : explanation.uncertainty_level === 'Moderate'
              ? 'bg-amber-950/70 text-amber-300 border-amber-500/30'
              : 'bg-rose-950/70 text-rose-300 border-rose-500/30'
          }`}>
            {explanation.uncertainty_level} Uncertainty
          </span>
        </div>
      </div>

      {/* Main Grid: Decision Drivers & Speculative Claim Modifiers */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Primary Decision Drivers */}
        <div className="bg-navy-850/80 rounded-xl p-4 border border-navy-750 space-y-3">
          <div className="flex items-center space-x-2 text-xs font-bold text-white uppercase tracking-wider">
            <CheckCircle className="w-4 h-4 text-cyan-400" />
            <span>Primary Decision Drivers</span>
          </div>

          <div className="space-y-2">
            {explanation.primary_reasons.map((reason, idx) => (
              <div key={idx} className="flex items-start space-x-2 text-xs text-slate-200">
                <span className="text-cyan-400 font-bold shrink-0 mt-0.5">•</span>
                <span className="leading-relaxed">{reason}</span>
              </div>
            ))}
          </div>

          {explanation.dominant_criteria_met.length > 0 && (
            <div className="pt-2 border-t border-navy-800">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                Dominant Milestone Verified
              </span>
              <p className="text-xs text-slate-300 font-medium italic">
                "{explanation.dominant_criteria_met[0]}"
              </p>
            </div>
          )}
        </div>

        {/* Claim Verification & Disqualifying Factors */}
        <div className="bg-navy-850/80 rounded-xl p-4 border border-navy-750 space-y-3">
          <div className="flex items-center space-x-2 text-xs font-bold text-white uppercase tracking-wider">
            <Scale className="w-4 h-4 text-amber-400" />
            <span>Evidence Discounting & Disqualifiers</span>
          </div>

          {explanation.is_claim_discounted && (
            <div className="p-2.5 rounded-lg bg-amber-950/40 border border-amber-500/30 text-xs text-amber-200 flex items-start space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              <span>
                Speculative future statements ('planned for', 'will be tested') were discounted to prevent artificial TRL inflation.
              </span>
            </div>
          )}

          {explanation.disqualifying_factors.length > 0 ? (
            <div className="space-y-2">
              {explanation.disqualifying_factors.map((factor, idx) => (
                <div key={idx} className="flex items-start space-x-2 text-xs text-slate-300">
                  <span className="text-amber-400 font-bold shrink-0 mt-0.5">•</span>
                  <span className="leading-relaxed">{factor}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-400 italic">
              No disqualifying negative indicators detected. Document evidence aligns consistently with the evaluated TRL range.
            </p>
          )}
        </div>
      </div>

      {/* Top Feature Contributions */}
      {explanation.top_feature_contributions.length > 0 && (
        <div className="bg-navy-850/60 rounded-xl p-4 border border-navy-750">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-1.5">
              <BarChart3 className="w-4 h-4 text-electric-400" />
              <span>Normative Feature Importance Weights</span>
            </span>
            <span className="text-[11px] text-slate-500">
              Frank & Hall Ordinal Feature Attribution
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
            {explanation.top_feature_contributions.map((feat, idx) => (
              <div
                key={idx}
                className="bg-navy-900/80 rounded-lg p-2.5 border border-navy-800 flex items-center justify-between text-xs"
              >
                <div className="truncate pr-2">
                  <span className="text-slate-300 block truncate">{feat.feature}</span>
                  <span className={`text-[10px] font-semibold ${
                    feat.impact === 'Positive' ? 'text-emerald-400' : 'text-slate-400'
                  }`}>
                    {feat.impact} Impact
                  </span>
                </div>
                <span className="text-cyan-400 font-mono font-bold">
                  {feat.weight.toFixed(3)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

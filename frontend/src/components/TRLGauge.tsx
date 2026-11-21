import React from 'react';
import { 
  Award, 
  AlertTriangle, 
  TrendingUp, 
  CheckCircle, 
  HelpCircle,
  FileDown,
  Compass
} from 'lucide-react';
import { TRLPredictionResult } from '../types';

interface TRLGaugeProps {
  prediction: TRLPredictionResult;
  documentTitle: string;
  onDownloadReport: () => void;
}

export const TRLGauge: React.FC<TRLGaugeProps> = ({
  prediction,
  documentTitle,
  onDownloadReport,
}) => {
  const trl = prediction.predicted_trl;

  // Determine stage and color theme based on TRL
  const getStageTheme = (level: number) => {
    if (level <= 2) {
      return {
        stage: 'Basic & Applied Research',
        bg: 'from-cyan-500/20 to-blue-600/10',
        border: 'border-cyan-500/40',
        text: 'text-cyan-400',
        badge: 'bg-cyan-950/60 text-cyan-300 border-cyan-500/40',
        ring: '#06b6d4',
      };
    } else if (level <= 4) {
      return {
        stage: 'Laboratory Feasibility & Breadboard',
        bg: 'from-electric-600/20 to-blue-600/10',
        border: 'border-electric-500/40',
        text: 'text-electric-400',
        badge: 'bg-electric-950/60 text-electric-300 border-electric-500/40',
        ring: '#2b75ff',
      };
    } else if (level <= 6) {
      return {
        stage: 'Relevant Environment & Prototype',
        bg: 'from-indigo-600/20 to-purple-600/10',
        border: 'border-indigo-500/40',
        text: 'text-indigo-400',
        badge: 'bg-indigo-950/60 text-indigo-300 border-indigo-500/40',
        ring: '#818cf8',
      };
    } else if (level <= 8) {
      return {
        stage: 'Operational Demonstration & Qualification',
        bg: 'from-amber-500/20 to-orange-600/10',
        border: 'border-amber-500/40',
        text: 'text-amber-400',
        badge: 'bg-amber-950/60 text-amber-300 border-amber-500/40',
        ring: '#f59e0b',
      };
    } else {
      return {
        stage: 'Commercial Flight & Mission Proven',
        bg: 'from-emerald-500/20 to-teal-600/10',
        border: 'border-emerald-500/40',
        text: 'text-emerald-400',
        badge: 'bg-emerald-950/60 text-emerald-300 border-emerald-500/40',
        ring: '#10b981',
      };
    }
  };

  const theme = getStageTheme(trl);
  const confidencePercent = Math.round(prediction.calibrated_confidence * 100);

  return (
    <div className="glass-panel rounded-2xl p-6 relative overflow-hidden border border-navy-700/80 shadow-2xl">
      {/* Background radial accent */}
      <div 
        className="absolute top-0 right-0 w-80 h-80 rounded-full blur-3xl opacity-20 pointer-events-none"
        style={{ backgroundColor: theme.ring }}
      />

      {/* Header Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-5 border-b border-navy-700/70">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Technology Readiness Assessment
            </span>
            <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full border ${theme.badge}`}>
              {theme.stage}
            </span>
          </div>
          <h3 className="text-lg font-bold text-white mt-1 line-clamp-1">
            {documentTitle}
          </h3>
        </div>

        <button
          onClick={onDownloadReport}
          className="flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-semibold bg-navy-800 hover:bg-navy-750 text-cyan-300 border border-cyan-500/30 hover:border-cyan-400 transition-all shadow-sm"
          title="Download Official PDF Assessment Report"
        >
          <FileDown className="w-4 h-4 text-cyan-400" />
          <span>Download PDF Report</span>
        </button>
      </div>

      {/* Main Grid: Gauge Hero + Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6 items-center">
        {/* Left: TRL Circle Hero */}
        <div className="lg:col-span-5 flex flex-col items-center justify-center p-4">
          <div className="relative flex items-center justify-center">
            {/* Outer SVG Gauge Ring */}
            <svg className="w-44 h-44 transform -rotate-90">
              {/* Background track */}
              <circle
                cx="88"
                cy="88"
                r="76"
                stroke="#15244f"
                strokeWidth="10"
                fill="transparent"
              />
              {/* Progress track */}
              <circle
                cx="88"
                cy="88"
                r="76"
                stroke={theme.ring}
                strokeWidth="10"
                strokeDasharray={477}
                strokeDashoffset={477 - (477 * (trl / 9))}
                strokeLinecap="round"
                fill="transparent"
                className="transition-all duration-1000 ease-out"
              />
            </svg>

            {/* Inner Badge Content */}
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest">
                Assessed Level
              </span>
              <div className="flex items-baseline space-x-1">
                <span className="text-xs font-bold text-slate-400">TRL</span>
                <span className={`text-5xl font-extrabold ${theme.text} tracking-tight`}>
                  {trl}
                </span>
              </div>
              <span className="text-[11px] font-medium text-slate-400">
                Level {trl} of 9
              </span>
            </div>
          </div>

          <p className="text-center font-semibold text-white mt-3 text-sm">
            {prediction.trl_title}
          </p>
          <p className="text-center text-xs text-slate-400 max-w-xs mt-1 leading-relaxed">
            {prediction.trl_definition}
          </p>
        </div>

        {/* Right: Confidence, Calibration & Alternatives */}
        <div className="lg:col-span-7 space-y-4">
          {/* Calibrated Confidence Box */}
          <div className="bg-navy-850/80 rounded-xl p-4 border border-navy-700/80">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-slate-300 flex items-center space-x-1.5">
                <TrendingUp className="w-3.5 h-3.5 text-cyan-400" />
                <span>Calibrated Model Confidence</span>
              </span>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-white font-mono">
                  {confidencePercent}%
                </span>
                <span className={`text-[10px] font-semibold px-2 py-0.2 rounded-full border ${
                  prediction.confidence_tier === 'High'
                    ? 'bg-emerald-950/60 text-emerald-300 border-emerald-500/30'
                    : 'bg-amber-950/60 text-amber-300 border-amber-500/30'
                }`}>
                  {prediction.confidence_tier}
                </span>
              </div>
            </div>

            {/* Confidence Bar */}
            <div className="w-full h-2.5 bg-navy-900 rounded-full overflow-hidden p-0.5 border border-navy-750">
              <div
                className="h-full rounded-full transition-all duration-700 ease-out"
                style={{
                  width: `${confidencePercent}%`,
                  backgroundColor: theme.ring,
                }}
              />
            </div>

            {/* Uncertainty Explanation */}
            <div className="mt-3 flex items-start space-x-2 text-[11px] text-slate-400 bg-navy-900/60 rounded-lg p-2.5 border border-navy-800">
              <Compass className="w-4 h-4 text-electric-400 shrink-0 mt-0.5" />
              <span>{prediction.model_explanation.uncertainty_reason}</span>
            </div>
          </div>

          {/* Alternative Levels Distribution */}
          <div className="bg-navy-850/80 rounded-xl p-4 border border-navy-700/80">
            <span className="text-xs font-medium text-slate-300 block mb-2.5">
              Alternative Technology Readiness Probabilities
            </span>

            <div className="space-y-2">
              {prediction.alternatives.length > 0 ? (
                prediction.alternatives.map((alt) => {
                  const altPercent = Math.round(alt.probability * 100);
                  return (
                    <div key={alt.trl} className="space-y-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-slate-300 font-medium">
                          TRL {alt.trl}: <span className="text-slate-400 font-normal">{alt.description}</span>
                        </span>
                        <span className="text-slate-400 font-mono text-[11px]">
                          {altPercent}%
                        </span>
                      </div>
                      <div className="w-full h-1.5 bg-navy-900 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-slate-500 rounded-full"
                          style={{ width: `${altPercent}%` }}
                        />
                      </div>
                    </div>
                  );
                })
              ) : (
                <p className="text-xs text-slate-400 italic">
                  High consensus; dominant TRL exhibits minimal ambiguity with adjacent levels.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

import React from 'react';
import { 
  Sparkles, 
  FileText, 
  ArrowRight, 
  Layers, 
  CheckCircle2,
  Atom,
  Battery,
  Radio,
  Compass,
  Satellite
} from 'lucide-react';
import { SampleDocumentInfo } from '../types';

interface SampleDocumentSelectorProps {
  samples: SampleDocumentInfo[];
  onSelectSample: (sampleId: string) => void;
  isLoading: boolean;
}

export const SampleDocumentSelector: React.FC<SampleDocumentSelectorProps> = ({
  samples,
  onSelectSample,
  isLoading,
}) => {
  const getIconForTRL = (trl: number) => {
    switch (trl) {
      case 1:
        return <Atom className="w-5 h-5 text-cyan-400" />;
      case 3:
        return <Battery className="w-5 h-5 text-electric-400" />;
      case 5:
        return <Radio className="w-5 h-5 text-indigo-400" />;
      case 7:
        return <Compass className="w-5 h-5 text-amber-400" />;
      case 9:
        return <Satellite className="w-5 h-5 text-emerald-400" />;
      default:
        return <Layers className="w-5 h-5 text-cyan-400" />;
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-6 border border-navy-700/80 shadow-2xl space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <span>Preloaded Benchmark Technical Documents</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Test reproducible evidence extraction and ordinal classification instantly with realistic technical papers
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
        {samples.map((sample) => (
          <button
            key={sample.sample_id}
            onClick={() => onSelectSample(sample.sample_id)}
            disabled={isLoading}
            className="text-left bg-navy-850 hover:bg-navy-800 rounded-xl p-3.5 border border-navy-750 hover:border-cyan-500/40 transition-all flex flex-col justify-between group disabled:opacity-50"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="w-8 h-8 rounded-lg bg-navy-900 flex items-center justify-center border border-navy-750 group-hover:scale-105 transition-transform">
                  {getIconForTRL(sample.expected_trl)}
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-navy-900 text-cyan-300 border border-navy-750 font-mono">
                  TRL {sample.expected_trl}
                </span>
              </div>

              <h4 className="text-xs font-bold text-white line-clamp-2 leading-snug group-hover:text-cyan-300 transition-colors">
                {sample.title}
              </h4>

              <p className="text-[10px] text-slate-400 mt-1.5 line-clamp-2 leading-relaxed">
                {sample.description}
              </p>
            </div>

            <div className="mt-3 pt-2 border-t border-navy-800/80 flex items-center justify-between text-[10px] text-slate-500 group-hover:text-cyan-400 transition-colors">
              <span className="truncate pr-1">{sample.domain}</span>
              <ArrowRight className="w-3 h-3 shrink-0 group-hover:translate-x-0.5 transition-transform" />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

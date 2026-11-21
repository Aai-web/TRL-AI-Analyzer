import React, { useState } from 'react';
import { 
  FileText, 
  Search, 
  Filter, 
  CheckCircle2, 
  AlertCircle, 
  ShieldCheck, 
  HelpCircle,
  Quote,
  SlidersHorizontal,
  Bookmark
} from 'lucide-react';
import { EvidenceItem, EvidenceStrength } from '../types';

interface EvidenceExplorerProps {
  evidenceItems: EvidenceItem[];
  predictedTRL: number;
}

export const EvidenceExplorer: React.FC<EvidenceExplorerProps> = ({
  evidenceItems,
  predictedTRL,
}) => {
  const [strengthFilter, setStrengthFilter] = useState<'All' | EvidenceStrength>('All');
  const [trlFilter, setTrlFilter] = useState<number | 'All'>('All');
  const [searchQuery, setSearchQuery] = useState('');

  // Count summaries
  const strongCount = evidenceItems.filter((e) => e.strength === 'Strong').length;
  const modCount = evidenceItems.filter((e) => e.strength === 'Moderate').length;
  const weakCount = evidenceItems.filter((e) => e.strength === 'Weak').length;
  const verifiedResultsCount = evidenceItems.filter((e) => e.verification_status === 'Verified Result').length;

  // Filter items
  const filteredItems = evidenceItems.filter((item) => {
    if (strengthFilter !== 'All' && item.strength !== strengthFilter) return false;
    if (trlFilter !== 'All' && item.trl_level !== trlFilter) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const inQuote = item.quote.toLowerCase().includes(q);
      const inCriterion = item.criterion_name.toLowerCase().includes(q);
      const inReason = item.reasoning.toLowerCase().includes(q);
      if (!inQuote && !inCriterion && !inReason) return false;
    }
    return true;
  });

  return (
    <div className="glass-panel rounded-2xl p-6 border border-navy-700/80 shadow-2xl">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-navy-700/70">
        <div>
          <div className="flex items-center space-x-2">
            <h3 className="text-lg font-bold text-white flex items-center space-x-2">
              <Quote className="w-5 h-5 text-cyan-400" />
              <span>Verified Evidence Explorer</span>
            </h3>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-electric-950/70 text-electric-300 border border-electric-500/30 font-mono">
              {evidenceItems.length} Citations
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Exact verbatim extractions with certified 1-indexed page references and strength scoring
          </p>
        </div>

        {/* Quick Stats Pills */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="px-2.5 py-1 rounded-lg bg-emerald-950/50 border border-emerald-500/30 text-xs text-emerald-300 font-medium">
            <strong className="text-emerald-400 font-bold">{strongCount}</strong> Strong
          </span>
          <span className="px-2.5 py-1 rounded-lg bg-amber-950/50 border border-amber-500/30 text-xs text-amber-300 font-medium">
            <strong className="text-amber-400 font-bold">{modCount}</strong> Moderate
          </span>
          <span className="px-2.5 py-1 rounded-lg bg-rose-950/50 border border-rose-500/30 text-xs text-rose-300 font-medium">
            <strong className="text-rose-400 font-bold">{weakCount}</strong> Speculative / Weak
          </span>
        </div>
      </div>

      {/* Filter and Search Controls */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-3 my-4">
        {/* Search */}
        <div className="md:col-span-5 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search within extracted statements or criteria..."
            className="w-full bg-navy-850 border border-navy-700 rounded-xl pl-9 pr-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
          />
        </div>

        {/* Strength Filter Tabs */}
        <div className="md:col-span-4 flex items-center bg-navy-850 p-1 rounded-xl border border-navy-700">
          {(['All', 'Strong', 'Moderate', 'Weak'] as const).map((s) => (
            <button
              key={s}
              onClick={() => setStrengthFilter(s)}
              className={`flex-1 py-1 text-xs font-medium rounded-lg transition-all ${
                strengthFilter === s
                  ? 'bg-electric-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        {/* TRL Filter Select */}
        <div className="md:col-span-3">
          <select
            value={trlFilter}
            onChange={(e) => setTrlFilter(e.target.value === 'All' ? 'All' : Number(e.target.value))}
            className="w-full bg-navy-850 border border-navy-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-400"
          >
            <option value="All">All TRL Levels (1–9)</option>
            {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((lvl) => (
              <option key={lvl} value={lvl}>
                TRL {lvl} {lvl === predictedTRL ? '★ Assessed' : ''}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Evidence Cards List */}
      <div className="space-y-3 max-h-[520px] overflow-y-auto pr-1">
        {filteredItems.length > 0 ? (
          filteredItems.map((item) => {
            const isStrong = item.strength === 'Strong';
            const isMod = item.strength === 'Moderate';
            const isWeak = item.strength === 'Weak';

            const badgeBg = isStrong 
              ? 'bg-emerald-950/70 text-emerald-300 border-emerald-500/40' 
              : isMod 
              ? 'bg-amber-950/70 text-amber-300 border-amber-500/40' 
              : 'bg-rose-950/70 text-rose-300 border-rose-500/40';

            const borderAccent = isStrong
              ? 'hover:border-emerald-500/50'
              : isMod
              ? 'hover:border-amber-500/50'
              : 'hover:border-rose-500/50';

            return (
              <div
                key={item.evidence_id}
                className={`bg-navy-850/70 rounded-xl p-4 border border-navy-750 transition-all ${borderAccent}`}
              >
                {/* Meta row */}
                <div className="flex flex-wrap items-center justify-between gap-2 mb-2.5">
                  <div className="flex items-center space-x-2">
                    <span className="px-2 py-0.5 rounded-lg text-xs font-bold bg-electric-950 text-cyan-300 border border-cyan-500/30">
                      TRL {item.trl_level}
                    </span>
                    <span className="flex items-center space-x-1 px-2 py-0.5 rounded-lg text-xs font-semibold bg-navy-800 text-slate-300 border border-navy-700">
                      <FileText className="w-3 h-3 text-cyan-400" />
                      <span>Page {item.page_number}</span>
                    </span>
                    <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${badgeBg}`}>
                      {item.strength} Evidence
                    </span>
                  </div>

                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-slate-400">Status:</span>
                    <span className="font-medium text-slate-200">
                      {item.verification_status}
                    </span>
                    <span className="text-slate-500">•</span>
                    <span className="text-slate-400 font-mono">
                      {Math.round(item.confidence_score * 100)}% conf
                    </span>
                  </div>
                </div>

                {/* Verbatim Quote */}
                <blockquote className="text-xs text-slate-100 font-mono bg-navy-900/80 rounded-lg p-3 border-l-4 border-cyan-400 leading-relaxed italic">
                  "{item.quote}"
                </blockquote>

                {/* Criterion and Reasoning */}
                <div className="mt-2.5 pt-2 border-t border-navy-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                  <div className="text-slate-400">
                    <span className="text-slate-500 font-semibold">Matched Criterion: </span>
                    <span className="text-slate-300">{item.criterion_name}</span>
                  </div>
                  <div className="text-[11px] text-cyan-400/90 italic">
                    {item.reasoning}
                  </div>
                </div>
              </div>
            );
          })
        ) : (
          <div className="text-center py-12 rounded-xl bg-navy-850/30 border border-navy-800">
            <Quote className="w-8 h-8 text-slate-600 mx-auto mb-2" />
            <p className="text-sm font-semibold text-slate-300">No matching evidence found</p>
            <p className="text-xs text-slate-500 mt-1">
              Try adjusting your strength filter or search terms.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

import React from 'react';
import { 
  X, 
  History, 
  FileText, 
  Calendar, 
  ArrowRight,
  Sparkles,
  Layers
} from 'lucide-react';
import { DocumentAnalysisResponse } from '../types';

interface DocumentHistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  history: DocumentAnalysisResponse[];
  currentDocId?: string;
  onSelectDoc: (doc: DocumentAnalysisResponse) => void;
}

export const DocumentHistoryDrawer: React.FC<DocumentHistoryDrawerProps> = ({
  isOpen,
  onClose,
  history,
  currentDocId,
  onSelectDoc,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-sm animate-fade-in flex justify-end">
      <div 
        className="w-full max-w-md bg-navy-900 border-l border-navy-750 h-full p-6 flex flex-col shadow-2xl relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-navy-750">
          <div className="flex items-center space-x-2">
            <History className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base font-bold text-white">Session History</h3>
            <span className="text-xs px-2 py-0.5 rounded-full bg-navy-800 text-slate-400 font-mono">
              {history.length}
            </span>
          </div>

          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-navy-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* History List */}
        <div className="flex-1 overflow-y-auto py-4 space-y-3">
          {history.length > 0 ? (
            history.map((doc) => {
              const isSelected = doc.document_id === currentDocId;
              const dateStr = new Date(doc.processed_at).toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
              });

              return (
                <div
                  key={doc.document_id}
                  onClick={() => {
                    onSelectDoc(doc);
                    onClose();
                  }}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-navy-800 border-cyan-400 shadow-glow-cyan'
                      : 'bg-navy-850 border-navy-750 hover:border-slate-600'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-bold text-cyan-300 font-mono">
                      TRL {doc.prediction.predicted_trl}
                    </span>
                    <span className="text-[10px] text-slate-500 flex items-center space-x-1">
                      <Calendar className="w-3 h-3" />
                      <span>{dateStr}</span>
                    </span>
                  </div>

                  <h4 className="text-xs font-bold text-white line-clamp-1">
                    {doc.filename}
                  </h4>

                  <div className="flex items-center justify-between mt-2 pt-2 border-t border-navy-800 text-[10px] text-slate-400">
                    <span>{doc.technical_domain}</span>
                    <span>{doc.page_count} pages • {doc.prediction.evidence_items.length} ev</span>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="text-center py-12 text-slate-500 text-xs">
              No documents analyzed in this session yet.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

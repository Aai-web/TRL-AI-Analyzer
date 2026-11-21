import React, { useState, useRef } from 'react';
import { 
  Upload, 
  FileText, 
  Type, 
  AlertCircle, 
  Loader2, 
  FileCheck,
  CheckCircle2,
  Sparkles
} from 'lucide-react';

interface FileUploadProps {
  onUploadFile: (file: File) => Promise<void>;
  onAnalyzeText: (text: string, title?: string) => Promise<void>;
  isLoading: boolean;
  onSelectSample: (sampleId: string) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onUploadFile,
  onAnalyzeText,
  isLoading,
  onSelectSample,
}) => {
  const [activeTab, setActiveTab] = useState<'upload' | 'paste'>('upload');
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [rawText, setRawText] = useState('');
  const [docTitle, setDocTitle] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const validateAndSetFile = (file: File) => {
    setErrorMessage(null);
    const validExtensions = ['.pdf', '.txt'];
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();

    if (!validExtensions.includes(ext)) {
      setErrorMessage(`Unsupported file format. Please upload a PDF (.pdf) or Text document (.txt).`);
      return false;
    }

    if (file.size > 25 * 1024 * 1024) {
      setErrorMessage(`File exceeds 25MB maximum limit (${(file.size / (1024 * 1024)).toFixed(1)}MB).`);
      return false;
    }

    setSelectedFile(file);
    return true;
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleUploadSubmit = async () => {
    if (!selectedFile) return;
    try {
      setErrorMessage(null);
      await onUploadFile(selectedFile);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to analyze document.');
    }
  };

  const handleTextSubmit = async () => {
    if (rawText.trim().length < 50) {
      setErrorMessage('Please provide at least 50 characters of technical text for accurate assessment.');
      return;
    }
    try {
      setErrorMessage(null);
      await onAnalyzeText(rawText, docTitle.trim() || undefined);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to analyze text.');
    }
  };

  return (
    <div className="w-full glass-panel rounded-2xl p-6 shadow-2xl relative overflow-hidden">
      {/* Decorative gradient glow */}
      <div className="absolute -top-24 -left-24 w-72 h-72 bg-electric-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -right-24 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Mode Navigation Tabs */}
      <div className="flex items-center justify-between border-b border-navy-700/80 pb-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <span>Analyze Technical Document</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Evaluate patents, research papers, and technical reports for TRL 1–9 maturity
          </p>
        </div>

        <div className="flex bg-navy-850 p-1 rounded-xl border border-navy-700/60">
          <button
            onClick={() => { setActiveTab('upload'); setErrorMessage(null); }}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'upload'
                ? 'bg-electric-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Upload Document</span>
          </button>
          <button
            onClick={() => { setActiveTab('paste'); setErrorMessage(null); }}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'paste'
                ? 'bg-electric-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Type className="w-3.5 h-3.5" />
            <span>Paste Text / Abstract</span>
          </button>
        </div>
      </div>

      {/* Error Alert */}
      {errorMessage && (
        <div className="mb-4 p-3 rounded-xl bg-red-950/40 border border-red-500/30 flex items-start space-x-2.5 text-xs text-red-200">
          <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* TAB 1: Document Upload */}
      {activeTab === 'upload' && (
        <div>
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`cursor-pointer rounded-2xl border-2 border-dashed p-8 text-center transition-all ${
              isDragging
                ? 'border-cyan-400 bg-cyan-950/20 shadow-glow-cyan'
                : selectedFile
                ? 'border-electric-500/60 bg-navy-850/60'
                : 'border-navy-700 hover:border-electric-500/50 hover:bg-navy-850/40'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.txt"
              className="hidden"
              onChange={handleFileChange}
            />

            {selectedFile ? (
              <div className="flex flex-col items-center justify-center space-y-3">
                <div className="w-14 h-14 rounded-2xl bg-electric-600/20 border border-electric-500/40 flex items-center justify-center text-electric-400 shadow-glow-blue">
                  <FileCheck className="w-7 h-7" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">{selectedFile.name}</p>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • Ready for evidence extraction
                  </p>
                </div>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedFile(null);
                  }}
                  className="text-xs text-slate-400 hover:text-red-400 transition"
                >
                  Choose a different file
                </button>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center space-y-3">
                <div className="w-14 h-14 rounded-2xl bg-navy-800 border border-navy-700 flex items-center justify-center text-cyan-400">
                  <Upload className="w-7 h-7" />
                </div>
                <div>
                  <p className="text-sm font-medium text-white">
                    Drop your technical paper or report here, or <span className="text-cyan-400 hover:underline">browse</span>
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    Supports <span className="text-slate-300 font-mono">PDF</span> and <span className="text-slate-300 font-mono">TXT</span> up to 25MB • Preserves page numbers
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Action Bar */}
          <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
            <div className="text-xs text-slate-400 flex items-center space-x-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
              <span>Multi-page chunking & verified evidence attribution</span>
            </div>

            <button
              onClick={handleUploadSubmit}
              disabled={!selectedFile || isLoading}
              className={`flex items-center space-x-2 px-6 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                !selectedFile || isLoading
                  ? 'bg-navy-800 text-slate-500 cursor-not-allowed border border-navy-700'
                  : 'bg-gradient-to-r from-electric-600 to-cyan-600 hover:from-electric-500 hover:to-cyan-500 text-white shadow-glow-blue'
              }`}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Evaluating TRL 1–9...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Start AI Assessment</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* TAB 2: Text / Abstract Paste */}
      {activeTab === 'paste' && (
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">
              Document Title or Technology Name (Optional)
            </label>
            <input
              type="text"
              value={docTitle}
              onChange={(e) => setDocTitle(e.target.value)}
              placeholder="e.g., Solid-State Vanadium Battery Proof-of-Concept"
              className="w-full bg-navy-850 border border-navy-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-semibold text-slate-300">
                Technical Text, Abstract, or Patent Specification
              </label>
              <span className="text-[11px] text-slate-500 font-mono">
                {rawText.length} characters
              </span>
            </div>
            <textarea
              rows={6}
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              placeholder="Paste research paper abstract, patent claims, or engineering test logs here. Use '--- Page 2 ---' to simulate page boundaries..."
              className="w-full bg-navy-850 border border-navy-700 rounded-xl p-3.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 font-mono leading-relaxed resize-y"
            />
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
            <div className="flex items-center space-x-2">
              <span className="text-xs text-slate-400">Quick fill:</span>
              <button
                type="button"
                onClick={() => onSelectSample('SAMPLE-TRL3')}
                className="text-xs px-2.5 py-1 rounded-lg bg-navy-800 text-cyan-300 hover:bg-navy-750 border border-navy-700"
              >
                Lab Proof (TRL 3)
              </button>
              <button
                type="button"
                onClick={() => onSelectSample('SAMPLE-TRL7')}
                className="text-xs px-2.5 py-1 rounded-lg bg-navy-800 text-electric-300 hover:bg-navy-750 border border-navy-700"
              >
                Sea Trial (TRL 7)
              </button>
            </div>

            <button
              onClick={handleTextSubmit}
              disabled={rawText.trim().length < 50 || isLoading}
              className={`flex items-center space-x-2 px-6 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                rawText.trim().length < 50 || isLoading
                  ? 'bg-navy-800 text-slate-500 cursor-not-allowed border border-navy-700'
                  : 'bg-gradient-to-r from-electric-600 to-cyan-600 hover:from-electric-500 hover:to-cyan-500 text-white shadow-glow-blue'
              }`}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Evaluating Evidence...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Analyze Text</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

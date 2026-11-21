import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { 
  Quote, 
  ShieldAlert, 
  Workflow, 
  BrainCircuit, 
  Sparkles 
} from 'lucide-react';

import { api } from './services/api';
import { 
  DocumentAnalysisResponse, 
  SampleDocumentInfo, 
  ModelInfoResponse,
  UserProfile 
} from './types';

import { Navbar } from './components/Navbar';
import { FileUpload } from './components/FileUpload';
import { TRLGauge } from './components/TRLGauge';
import { TRLProgression } from './components/TRLProgression';
import { EvidenceExplorer } from './components/EvidenceExplorer';
import { GapAnalysisView } from './components/GapAnalysisView';
import { RoadmapTimeline } from './components/RoadmapTimeline';
import { ModelExplanations } from './components/ModelExplanations';
import { SampleDocumentSelector } from './components/SampleDocumentSelector';
import { DocumentHistoryDrawer } from './components/DocumentHistoryDrawer';
import { ModelInfoModal } from './components/ModelInfoModal';
import { AuthPage } from './components/AuthPage';

export const App: React.FC = () => {
  // Compulsory User Authentication State
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(() => {
    try {
      const stored = localStorage.getItem('trl_user');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const [currentAnalysis, setCurrentAnalysis] = useState<DocumentAnalysisResponse | null>(null);
  const [samples, setSamples] = useState<SampleDocumentInfo[]>([]);
  const [history, setHistory] = useState<DocumentAnalysisResponse[]>([]);
  const [modelInfo, setModelInfo] = useState<ModelInfoResponse | null>(null);

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [loadingStep, setLoadingStep] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [isModelInfoOpen, setIsModelInfoOpen] = useState<boolean>(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'evidence' | 'gaps' | 'roadmap' | 'explanation'>('evidence');

  // Load initial samples, history, and model metadata when authenticated
  useEffect(() => {
    if (!currentUser) return;

    const fetchInitialData = async () => {
      try {
        const [sampleDocs, historyDocs, info] = await Promise.all([
          api.getSampleDocuments().catch(() => []),
          api.getHistory().catch(() => []),
          api.getModelInfo().catch(() => null),
        ]);
        setSamples(sampleDocs);
        setHistory(historyDocs);
        setModelInfo(info);

        // If history has items, select the most recent one
        if (historyDocs && historyDocs.length > 0) {
          setCurrentAnalysis(historyDocs[0]);
        }
      } catch (err) {
        console.warn('Initial data fetch notice:', err);
      }
    };
    fetchInitialData();
  }, [currentUser]);

  const handleLoginSuccess = (user: UserProfile, token: string) => {
    try {
      localStorage.setItem('trl_user', JSON.stringify(user));
      localStorage.setItem('trl_token', token);
    } catch {
      // localStorage fallback
    }
    setCurrentUser(user);
    try {
      confetti({
        particleCount: 40,
        spread: 60,
        origin: { y: 0.6 },
        colors: ['#06b6d4', '#1e60ff', '#10b981'],
      });
    } catch {
      // confetti fallback
    }
  };

  const handleSignOut = () => {
    try {
      localStorage.removeItem('trl_user');
      localStorage.removeItem('trl_token');
    } catch {
      // localStorage fallback
    }
    setCurrentUser(null);
    setCurrentAnalysis(null);
    setHistory([]);
  };

  const triggerCelebration = (trl: number) => {
    try {
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.7 },
        colors: trl >= 7 ? ['#10b981', '#06b6d4', '#3b82f6'] : ['#2b75ff', '#67e8f9', '#a855f7']
      });
    } catch {
      // Confetti fallback
    }
  };

  const handleUploadFile = async (file: File) => {
    setIsLoading(true);
    setLoadingStep('Uploading and parsing multi-page layout...');
    setErrorMessage(null);

    try {
      const result = await api.uploadDocument(file);
      setCurrentAnalysis(result);
      setHistory((prev) => [result, ...prev.filter((d) => d.document_id !== result.document_id)]);
      triggerCelebration(result.prediction.predicted_trl);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to analyze document.');
      throw err;
    } finally {
      setIsLoading(false);
      setLoadingStep('');
    }
  };

  const handleAnalyzeText = async (text: string, title?: string) => {
    setIsLoading(true);
    setLoadingStep('Evaluating technical criteria & evidence verification...');
    setErrorMessage(null);

    try {
      const result = await api.analyzeText(text, title);
      setCurrentAnalysis(result);
      setHistory((prev) => [result, ...prev.filter((d) => d.document_id !== result.document_id)]);
      triggerCelebration(result.prediction.predicted_trl);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to analyze text.');
      throw err;
    } finally {
      setIsLoading(false);
      setLoadingStep('');
    }
  };

  const handleSelectSample = async (sampleId: string) => {
    setIsLoading(true);
    setLoadingStep('Loading benchmark dataset paper & executing ML pipeline...');
    setErrorMessage(null);

    try {
      const result = await api.analyzeSample(sampleId);
      setCurrentAnalysis(result);
      setHistory((prev) => [result, ...prev.filter((d) => d.document_id !== result.document_id)]);
      triggerCelebration(result.prediction.predicted_trl);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to analyze sample document.');
    } finally {
      setIsLoading(false);
      setLoadingStep('');
    }
  };

  const handleDownloadReport = () => {
    if (!currentAnalysis) return;
    const url = api.getReportDownloadUrl(currentAnalysis.document_id);
    window.open(url, '_blank');
  };

  // COMPULSORY AUTH GATE: If user is not signed in, show AuthPage exclusively
  if (!currentUser) {
    return <AuthPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Navbar with User Profile & Sign Out */}
      <Navbar
        onOpenModelInfo={() => setIsModelInfoOpen(true)}
        onOpenHistory={() => setIsHistoryOpen(true)}
        onOpenSamples={() => {
          const el = document.getElementById('samples-section');
          el?.scrollIntoView({ behavior: 'smooth' });
        }}
        historyCount={history.length}
        currentUser={currentUser}
        onSignOut={handleSignOut}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Hero Banner */}
        <section className="text-center max-w-3xl mx-auto space-y-3">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-navy-800 border border-cyan-500/30 text-xs text-cyan-300 shadow-glow-cyan">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span className="font-semibold">Evidence-Based Ordinal TRL Assessment Engine</span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
            Predict Technology Readiness Level (TRL 1–9) with <span className="gradient-text-blue">Certified Evidence</span>
          </h1>

          <p className="text-sm text-slate-400 leading-relaxed max-w-2xl mx-auto">
            Automated intelligence system for research papers, patents, and engineering reports.
            Extracts verbatim citations with page references, discounts speculative claims, and produces actionable gap-closure roadmaps.
          </p>
        </section>

        {/* Upload Zone */}
        <section>
          <FileUpload
            onUploadFile={handleUploadFile}
            onAnalyzeText={handleAnalyzeText}
            isLoading={isLoading}
            onSelectSample={handleSelectSample}
          />
        </section>

        {/* Analysis Results View */}
        {currentAnalysis && (
          <section className="space-y-6 animate-slide-up">
            {/* TRL Gauge Hero */}
            <TRLGauge
              prediction={currentAnalysis.prediction}
              documentTitle={currentAnalysis.filename}
              onDownloadReport={handleDownloadReport}
            />

            {/* 1–9 Maturity Ladder Progression */}
            <TRLProgression
              currentTRL={currentAnalysis.prediction.predicted_trl}
              evidenceCounts={currentAnalysis.prediction.evidence_counts_by_trl}
            />

            {/* View Navigation Tabs */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-navy-750 pb-2">
              <div className="flex flex-wrap items-center space-x-2">
                <button
                  onClick={() => setActiveTab('evidence')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                    activeTab === 'evidence'
                      ? 'bg-electric-600 text-white shadow-glow-blue'
                      : 'text-slate-400 hover:text-white bg-navy-850 hover:bg-navy-800 border border-navy-750'
                  }`}
                >
                  <Quote className="w-3.5 h-3.5" />
                  <span>Supporting Evidence ({currentAnalysis.prediction.evidence_items.length})</span>
                </button>

                <button
                  onClick={() => setActiveTab('gaps')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                    activeTab === 'gaps'
                      ? 'bg-electric-600 text-white shadow-glow-blue'
                      : 'text-slate-400 hover:text-white bg-navy-850 hover:bg-navy-800 border border-navy-750'
                  }`}
                >
                  <ShieldAlert className="w-3.5 h-3.5" />
                  <span>Gap Analysis ({currentAnalysis.prediction.gap_analysis.length})</span>
                </button>

                <button
                  onClick={() => setActiveTab('roadmap')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                    activeTab === 'roadmap'
                      ? 'bg-electric-600 text-white shadow-glow-blue'
                      : 'text-slate-400 hover:text-white bg-navy-850 hover:bg-navy-800 border border-navy-750'
                  }`}
                >
                  <Workflow className="w-3.5 h-3.5" />
                  <span>Actionable Roadmap (3 Phases)</span>
                </button>

                <button
                  onClick={() => setActiveTab('explanation')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                    activeTab === 'explanation'
                      ? 'bg-electric-600 text-white shadow-glow-blue'
                      : 'text-slate-400 hover:text-white bg-navy-850 hover:bg-navy-800 border border-navy-750'
                  }`}
                >
                  <BrainCircuit className="w-3.5 h-3.5" />
                  <span>AI Decision Rationale</span>
                </button>
              </div>

              <div className="text-xs text-slate-400">
                Document ID: <span className="font-mono text-cyan-400">{currentAnalysis.document_id}</span>
              </div>
            </div>

            {/* Tab Contents */}
            <div>
              {activeTab === 'evidence' && (
                <EvidenceExplorer
                  evidenceItems={currentAnalysis.prediction.evidence_items}
                  predictedTRL={currentAnalysis.prediction.predicted_trl}
                />
              )}

              {activeTab === 'gaps' && (
                <GapAnalysisView
                  gapAnalysis={currentAnalysis.prediction.gap_analysis}
                  nextTrlBarriers={currentAnalysis.prediction.next_trl_barriers}
                  predictedTRL={currentAnalysis.prediction.predicted_trl}
                />
              )}

              {activeTab === 'roadmap' && (
                <RoadmapTimeline
                  roadmap={currentAnalysis.prediction.roadmap}
                  predictedTRL={currentAnalysis.prediction.predicted_trl}
                />
              )}

              {activeTab === 'explanation' && (
                <ModelExplanations
                  explanation={currentAnalysis.prediction.model_explanation}
                  predictedTRL={currentAnalysis.prediction.predicted_trl}
                />
              )}
            </div>
          </section>
        )}

        {/* Preloaded Samples Section */}
        <section id="samples-section">
          <SampleDocumentSelector
            samples={samples}
            onSelectSample={handleSelectSample}
            isLoading={isLoading}
          />
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-navy-800 bg-navy-950 py-6 mt-12 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div>
            <strong>TRL Intelligence</strong> • Built for Techfest IIT Bombay 2nd APCTT Hackathon 2026
          </div>
          <div className="flex items-center space-x-4">
            <span>NASA SP-20205003605</span>
            <span>•</span>
            <span>DoD TRA Guidance</span>
            <span>•</span>
            <span>ISO 16290:2013</span>
          </div>
        </div>
      </footer>

      {/* Modals and Drawers */}
      <ModelInfoModal
        isOpen={isModelInfoOpen}
        onClose={() => setIsModelInfoOpen(false)}
        modelInfo={modelInfo}
      />

      <DocumentHistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        history={history}
        currentDocId={currentAnalysis?.document_id}
        onSelectDoc={(doc) => setCurrentAnalysis(doc)}
      />
    </div>
  );
};

export default App;

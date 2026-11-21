import React, { useState } from 'react';
import { 
  History, 
  Info, 
  Sparkles, 
  Layers,
  LogOut,
  User,
  ShieldCheck,
  ChevronDown
} from 'lucide-react';
import { UserProfile } from '../types';

interface NavbarProps {
  onOpenModelInfo: () => void;
  onOpenHistory: () => void;
  onOpenSamples: () => void;
  historyCount: number;
  currentUser: UserProfile | null;
  onSignOut: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenModelInfo,
  onOpenHistory,
  onOpenSamples,
  historyCount,
  currentUser,
  onSignOut,
}) => {
  const [showUserMenu, setShowUserMenu] = useState(false);

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((part) => part[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-navy-750 bg-navy-900/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-electric-600 via-blue-600 to-cyan-500 shadow-glow-blue">
            <Layers className="w-5 h-5 text-white" />
            <div className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-cyan-400 rounded-full animate-ping" />
            <div className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-cyan-400 rounded-full" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-bold tracking-tight text-white">
                TRL <span className="gradient-text-blue">INTELLIGENCE</span>
              </span>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-electric-700/30 text-cyan-300 border border-cyan-500/30 tracking-wider uppercase">
                v1.0 AI
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Techfest IIT Bombay • 2nd APCTT Hackathon 2026
            </p>
          </div>
        </div>

        {/* Action Controls & User Profile */}
        <div className="flex items-center space-x-2 sm:space-x-3">
          {/* Sample Papers button */}
          <button
            onClick={onOpenSamples}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-200 bg-navy-800 hover:bg-navy-750 border border-navy-700 hover:border-cyan-500/40 transition-all duration-150"
            title="Load Preloaded Benchmark Papers"
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>Sample Papers</span>
          </button>

          {/* Model Architecture Info */}
          <button
            onClick={onOpenModelInfo}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-200 bg-navy-800 hover:bg-navy-750 border border-navy-700 hover:border-electric-500/40 transition-all duration-150"
            title="View Ordinal ML Architecture & Validated Metrics"
          >
            <Info className="w-3.5 h-3.5 text-electric-400" />
            <span className="hidden md:inline">Model Info</span>
          </button>

          {/* Session History */}
          <button
            onClick={onOpenHistory}
            className="relative flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-200 bg-navy-800 hover:bg-navy-750 border border-navy-700 hover:border-electric-500/40 transition-all duration-150"
            title="Session Analysis History"
          >
            <History className="w-3.5 h-3.5 text-slate-300" />
            <span className="hidden md:inline">History</span>
            {historyCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-electric-600 text-white">
                {historyCount}
              </span>
            )}
          </button>

          {/* User Profile Pill & Sign Out Button */}
          {currentUser && (
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-2 pl-2 pr-2.5 py-1 rounded-xl bg-navy-850 hover:bg-navy-800 border border-navy-700 hover:border-cyan-500/40 transition-all text-xs"
              >
                <div className="w-6 h-6 rounded-lg bg-gradient-to-br from-electric-600 to-cyan-600 flex items-center justify-center font-bold text-white text-[10px]">
                  {getInitials(currentUser.name)}
                </div>
                <div className="text-left hidden sm:block">
                  <div className="font-semibold text-white leading-tight truncate max-w-[110px]">
                    {currentUser.name}
                  </div>
                  <div className="text-[10px] text-cyan-400 truncate max-w-[110px]">
                    {currentUser.role}
                  </div>
                </div>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
              </button>

              {/* User Dropdown Menu */}
              {showUserMenu && (
                <div 
                  className="absolute right-0 mt-2 w-64 rounded-2xl bg-navy-900 border border-navy-700 shadow-2xl p-3 z-50 animate-fade-in"
                  onClick={(e) => e.stopPropagation()}
                >
                  <div className="pb-3 border-b border-navy-800">
                    <p className="text-xs font-bold text-white truncate">{currentUser.name}</p>
                    <p className="text-[11px] text-slate-400 truncate mt-0.5">{currentUser.email}</p>
                    <div className="mt-2 inline-flex items-center space-x-1 px-2 py-0.5 rounded-md bg-navy-800 text-[10px] text-cyan-300 border border-navy-700">
                      <ShieldCheck className="w-3 h-3 text-cyan-400" />
                      <span className="truncate">{currentUser.organization}</span>
                    </div>
                  </div>

                  <div className="pt-2">
                    <button
                      onClick={() => {
                        setShowUserMenu(false);
                        onSignOut();
                      }}
                      className="w-full flex items-center space-x-2 px-3 py-2 rounded-xl text-xs font-bold text-rose-300 bg-rose-950/40 hover:bg-rose-900/40 border border-rose-500/30 hover:border-rose-500/60 transition-all text-left group"
                    >
                      <LogOut className="w-3.5 h-3.5 text-rose-400 group-hover:-translate-x-0.5 transition-transform" />
                      <span>Sign Out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Quick Sign Out direct button on larger screens */}
          {currentUser && (
            <button
              onClick={onSignOut}
              className="hidden lg:flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-rose-300 bg-rose-950/40 hover:bg-rose-900/50 border border-rose-500/30 hover:border-rose-400 transition-all"
              title="Sign Out of TRL Intelligence"
            >
              <LogOut className="w-3.5 h-3.5 text-rose-400" />
              <span>Sign Out</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

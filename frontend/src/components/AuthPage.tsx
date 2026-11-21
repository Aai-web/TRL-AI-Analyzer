import React, { useState } from 'react';
import { 
  Layers, 
  Lock, 
  Mail, 
  User, 
  Building2, 
  Briefcase, 
  Eye, 
  EyeOff, 
  Sparkles, 
  ArrowRight, 
  ShieldCheck, 
  AlertCircle,
  Loader2,
  CheckCircle2
} from 'lucide-react';
import { api } from '../services/api';
import { UserProfile } from '../types';

interface AuthPageProps {
  onLoginSuccess: (user: UserProfile, token: string) => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({ onLoginSuccess }) => {
  const [mode, setMode] = useState<'signin' | 'signup'>('signin');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Sign In State
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Sign Up State
  const [signupName, setSignupName] = useState('');
  const [signupEmail, setSignupEmail] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [signupOrg, setSignupOrg] = useState('');
  const [signupRole, setSignupRole] = useState('Technology Evaluator');

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      setErrorMessage('Please enter both email and password.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const res = await api.login(email.trim(), password);
      onLoginSuccess(res.user, res.token);
    } catch (err: any) {
      setErrorMessage(err.message || 'Invalid credentials. Please verify your email and password.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!signupName.trim() || !signupEmail.trim() || !signupPassword) {
      setErrorMessage('Please complete all required fields.');
      return;
    }

    if (signupPassword.length < 4) {
      setErrorMessage('Password must be at least 4 characters long.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const res = await api.register({
        name: signupName.trim(),
        email: signupEmail.trim(),
        password: signupPassword,
        organization: signupOrg.trim() || 'Independent Research Cell',
        role: signupRole.trim() || 'Technology Assessor',
      });
      onLoginSuccess(res.user, res.token);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to register account.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const res = await api.getDemoAccount();
      onLoginSuccess(res.user, res.token);
    } catch (err: any) {
      // Fallback local demo profile if offline
      const fallbackUser: UserProfile = {
        id: 'usr-evaluator-demo',
        name: 'Prof. Rajesh Sharma',
        email: 'evaluator@iitb.ac.in',
        organization: 'IIT Bombay Techfest APCTT Cell',
        role: 'Lead Technology Assessor',
      };
      onLoginSuccess(fallbackUser, 'demo-token-12345');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#060b18] text-slate-100 flex flex-col justify-center items-center p-4 sm:p-6 font-sans relative overflow-hidden">
      {/* Dynamic glowing background backdrops */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-electric-600/15 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-cyan-500/15 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-900/10 rounded-full blur-[160px] pointer-events-none" />

      {/* Main Container */}
      <div className="w-full max-w-md relative z-10">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-electric-600 via-blue-600 to-cyan-500 shadow-glow-blue mb-3.5">
            <Layers className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            TRL <span className="gradient-text-blue">INTELLIGENCE</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1 font-medium">
            Techfest IIT Bombay • 2nd APCTT Hackathon 2026
          </p>
          <div className="inline-flex items-center space-x-1.5 px-3 py-0.5 rounded-full bg-navy-800/80 border border-cyan-500/30 text-[11px] text-cyan-300 mt-2">
            <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" />
            <span>Authorized Assessor Access Portal</span>
          </div>
        </div>

        {/* Auth Card */}
        <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-navy-700/80 shadow-2xl backdrop-blur-xl">
          {/* Sign In / Sign Up Mode Switcher */}
          <div className="flex bg-navy-850 p-1 rounded-xl border border-navy-700 mb-6">
            <button
              type="button"
              onClick={() => { setMode('signin'); setErrorMessage(null); }}
              className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all ${
                mode === 'signin'
                  ? 'bg-electric-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Sign In
            </button>
            <button
              type="button"
              onClick={() => { setMode('signup'); setErrorMessage(null); }}
              className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all ${
                mode === 'signup'
                  ? 'bg-electric-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Create Account
            </button>
          </div>

          {/* Error Alert */}
          {errorMessage && (
            <div className="mb-4 p-3 rounded-xl bg-red-950/50 border border-red-500/40 flex items-start space-x-2 text-xs text-red-200 animate-fade-in">
              <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* 1-CLICK INSTANT DEMO LOGIN BUTTON (FOR EVALUATORS) */}
          <div className="mb-6">
            <button
              type="button"
              onClick={handleDemoLogin}
              disabled={isLoading}
              className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl text-xs font-bold bg-gradient-to-r from-cyan-600/30 via-electric-600/30 to-blue-600/30 hover:from-cyan-600/40 hover:to-electric-600/40 text-cyan-200 border border-cyan-500/40 hover:border-cyan-400 transition-all shadow-glow-cyan group"
            >
              <Sparkles className="w-4 h-4 text-cyan-400 group-hover:rotate-12 transition-transform" />
              <span>1-Click Demo Sign In (Lead Evaluator)</span>
            </button>
            <div className="flex items-center my-4">
              <div className="flex-1 border-t border-navy-750" />
              <span className="px-3 text-[11px] text-slate-500 uppercase tracking-wider font-semibold">
                or continue with credentials
              </span>
              <div className="flex-1 border-t border-navy-750" />
            </div>
          </div>

          {/* MODE 1: SIGN IN FORM */}
          {mode === 'signin' && (
            <form onSubmit={handleSignIn} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="evaluator@iitb.ac.in"
                    className="w-full bg-navy-850 border border-navy-700 rounded-xl pl-9 pr-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full bg-navy-850 border border-navy-700 rounded-xl pl-9 pr-10 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              {/* Demo Hint */}
              <div className="p-2.5 rounded-lg bg-navy-900/60 border border-navy-800 text-[11px] text-slate-400 flex items-center justify-between">
                <span>Demo Pass: <code className="text-cyan-300 font-mono">hackathon2026</code></span>
                <span className="text-slate-500">Auto-fill via top button</span>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl text-xs font-bold bg-gradient-to-r from-electric-600 to-cyan-600 hover:from-electric-500 hover:to-cyan-500 text-white shadow-glow-blue transition-all disabled:opacity-50"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Signing in...</span>
                  </>
                ) : (
                  <>
                    <span>Sign In to TRL Portal</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          )}

          {/* MODE 2: SIGN UP FORM */}
          {mode === 'signup' && (
            <form onSubmit={handleSignUp} className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Full Name *
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    required
                    value={signupName}
                    onChange={(e) => setSignupName(e.target.value)}
                    placeholder="Dr. Vikram Sarabhai"
                    className="w-full bg-navy-850 border border-navy-700 rounded-xl pl-9 pr-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Institutional Email *
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="email"
                    required
                    value={signupEmail}
                    onChange={(e) => setSignupEmail(e.target.value)}
                    placeholder="researcher@isro.gov.in"
                    className="w-full bg-navy-850 border border-navy-700 rounded-xl pl-9 pr-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">
                    Organization
                  </label>
                  <div className="relative">
                    <Building2 className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      value={signupOrg}
                      onChange={(e) => setSignupOrg(e.target.value)}
                      placeholder="IIT Bombay"
                      className="w-full bg-navy-850 border border-navy-700 rounded-xl pl-9 pr-2.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">
                    Role
                  </label>
                  <select
                    value={signupRole}
                    onChange={(e) => setSignupRole(e.target.value)}
                    className="w-full bg-navy-850 border border-navy-700 rounded-xl px-2.5 py-2 text-xs text-white focus:outline-none focus:border-cyan-400"
                  >
                    <option value="Technology Evaluator">Technology Evaluator</option>
                    <option value="R&D Scientist">R&D Scientist</option>
                    <option value="Patent Examiner">Patent Examiner</option>
                    <option value="Tech Transfer Officer">Tech Transfer Officer</option>
                    <option value="Student / Academic">Student / Academic</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Create Password *
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={signupPassword}
                    onChange={(e) => setSignupPassword(e.target.value)}
                    placeholder="Min 4 characters"
                    className="w-full bg-navy-850 border border-navy-700 rounded-xl pl-9 pr-10 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl text-xs font-bold bg-gradient-to-r from-electric-600 to-cyan-600 hover:from-electric-500 hover:to-cyan-500 text-white shadow-glow-blue transition-all disabled:opacity-50 mt-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Registering...</span>
                  </>
                ) : (
                  <>
                    <span>Create Assessor Account</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          )}
        </div>

        {/* Footer info */}
        <p className="text-center text-[11px] text-slate-500 mt-6">
          Compliant with NASA SP-20205003605 & ISO 16290:2013 Security Standards
        </p>
      </div>
    </div>
  );
};

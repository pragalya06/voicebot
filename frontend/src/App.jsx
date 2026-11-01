import React, { useState, useEffect, useRef } from 'react';
import { Mic, ArrowRight, FileCheck, CheckCircle2, BookOpen, Sparkles, MessageSquareQuote, ExternalLink, HelpCircle, Loader2 } from 'lucide-react';
import { LanguageProvider, useTranslation } from './i18n';
import { Header } from './components/Header';
import { LanguageSelectorModal } from './components/LanguageSelectorModal';
import { VoiceInputModal } from './components/VoiceInputModal';
import { AudioPlayer } from './components/AudioPlayer';
import { EligibilityForm } from './components/EligibilityForm';
import { DocumentChecker } from './components/DocumentChecker';
import { ApplicationGuide } from './components/ApplicationGuide';
import { speechService } from './services/speech';

// ── Session helpers ──────────────────────────────────────────────────────────
// Session ID lives in sessionStorage so it is unique per browser tab and is
// automatically cleared when the tab closes. No login, no persistent tracking.
function getOrCreateSessionId() {
  const key = 'sevamitra_session_id';
  let sid = sessionStorage.getItem(key);
  if (!sid) {
    // Simple UUID v4-like generator (no dependency needed)
    sid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
    });
    sessionStorage.setItem(key, sid);
  }
  return sid;
}

function MainApp() {
  const { t, currentLanguage, changeLanguage } = useTranslation();
  const [backendStatus, setBackendStatus] = useState('checking');
  const [queryInput, setQueryInput] = useState('');
  const [activeModule, setActiveModule] = useState('home');
  const [isVoiceModalOpen, setIsVoiceModalOpen] = useState(false);

  // Active conversation response
  const [currentResponse, setCurrentResponse] = useState(null);

  // Session ID: stable per tab, stored in sessionStorage
  const sessionIdRef = useRef(getOrCreateSessionId());

  // Conversation history: last 6 messages (3 exchanges) sent with each request
  // so the backend can resolve follow-ups. Not persisted after tab close.
  const [conversationHistory, setConversationHistory] = useState([]);

  // Request ID guard: prevents a stale/slow response from overwriting a newer one.
  // Each processQuery() call increments this; the fetch only applies its result
  // if the ID still matches when it completes.
  const requestIdRef = useRef(0);

  // Check backend health on mount
  useEffect(() => {
    fetch('/api/health')
      .then((res) => {
        if (res.ok) return res.json();
        throw new Error('Backend not healthy');
      })
      .then((data) => {
        if (data.status === 'healthy') {
          setBackendStatus('online');
        } else {
          setBackendStatus('offline');
        }
      })
      .catch(() => {
        setBackendStatus('offline');
      });
  }, []);

  const [isLoadingQuery, setIsLoadingQuery] = useState(false);

  const processQuery = async (questionText, targetLang = null) => {
    if (!questionText.trim()) return;

    const queryLang = targetLang || currentLanguage;

    // Stop any speech currently playing before processing the new question
    speechService.stop();

    setIsLoadingQuery(true);

    // Assign a unique ID for this request
    const thisRequestId = ++requestIdRef.current;

    // Build the last 6 messages (3 exchanges) to send as context.
    // Older messages are dropped to keep the payload small.
    const historyToSend = conversationHistory.slice(-6).map((m) => ({
      role: m.role,
      content: m.content,
    }));

    try {
      const res = await fetch('/api/assistant/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: questionText,
          language: queryLang,
          session_id: sessionIdRef.current,
          conversation_history: historyToSend,
        }),
      });

      // Guard: if a newer request has already fired, discard this response
      if (thisRequestId !== requestIdRef.current) return;

      if (!res.ok) throw new Error('API query failed');
      const data = await res.json();

      // Guard again after async JSON parsing
      if (thisRequestId !== requestIdRef.current) return;

      // Store the canonical session_id returned by the server
      // (may differ from our local one if the session had expired).
      if (data.session_id) {
        sessionIdRef.current = data.session_id;
        sessionStorage.setItem('sevamitra_session_id', data.session_id);
      }

      // Switch full website UI language to match the detected query language
      if (data.language && data.language !== currentLanguage) {
        changeLanguage(data.language);
      }

      // Append this exchange to local history
      setConversationHistory((prev) => [
        ...prev,
        { role: 'user', content: questionText },
        { role: 'assistant', content: data.answer || '' },
      ].slice(-10)); // keep last 10 messages (5 exchanges)

      setCurrentResponse({
        // Use the request ID as a stable key so AudioPlayer remounts
        // for each new answer (prevents replaying the previous audio).
        _id: thisRequestId,
        question: questionText,
        detected_language: data.language || queryLang,
        answer: data.answer,
        voice_summary: data.voice_summary,
        is_clarification: data.is_clarification,
        clarification_options: data.clarification_options,
        scheme_name: data.scheme_name,
        benefit: data.benefit,
        eligibility_rules: data.eligibility_rules,
        required_documents: data.required_documents,
        application_steps: data.application_steps,
        source: data.source_name,
        source_portal: data.source_portal,
        disclaimer: data.disclaimer,
      });
    } catch (err) {
      if (thisRequestId !== requestIdRef.current) return;
      console.error('Error contacting assistant backend:', err);
      setCurrentResponse({
        _id: thisRequestId,
        question: questionText,
        detected_language: queryLang,
        answer: t('status.error') || 'Could not connect to the assistant service. Please check your connection and try again.',
        voice_summary: t('status.error') || 'Connection error. Please try again.',
        source: 'SevaMitra Helpdesk',
        source_portal: 'https://india.gov.in',
      });
    } finally {
      // Only clear loading if this is still the latest request
      if (thisRequestId === requestIdRef.current) {
        setIsLoadingQuery(false);
      }
    }
  };

  const handleHeroSubmit = (e) => {
    e.preventDefault();
    if (!queryInput.trim()) return;
    processQuery(queryInput);
    setQueryInput('');
  };

  const handleVoiceQuerySubmit = (spokenText, detectedLang) => {
    processQuery(spokenText, detectedLang);
  };

  const handleRecoveryOptionSelect = (moduleName) => {
    setActiveModule(moduleName);

    let guideText = '';
    if (moduleName === 'recommendations') {
      guideText = t('voice_recovery.option_eligibility');
    } else if (moduleName === 'documents') {
      guideText = t('voice_recovery.option_documents');
    } else {
      guideText = t('voice_recovery.option_how_to_apply');
    }

    const thisId = ++requestIdRef.current;
    setCurrentResponse({
      _id: thisId,
      question: t('voice_recovery.or_choose'),
      answer: guideText,
      source: 'SevaMitra Guidance Desk',
    });
  };

  return (
    <div className="app-container">
      {/* First-visit Language Modal */}
      <LanguageSelectorModal />

      {/* Intelligent Voice Input & Failure Recovery Modal */}
      <VoiceInputModal
        isOpen={isVoiceModalOpen}
        onClose={() => setIsVoiceModalOpen(false)}
        onQuerySubmit={handleVoiceQuerySubmit}
        onSelectOption={handleRecoveryOptionSelect}
      />

      {/* Main Header */}
      <Header activeTab={activeModule} setActiveTab={setActiveModule} />

      {/* Content */}
      <main className="main-content">
        {activeModule === 'recommendations' ? (
          <EligibilityForm onBackToHome={() => setActiveModule('home')} />
        ) : activeModule === 'documents' ? (
          <DocumentChecker
            onBackToHome={() => setActiveModule('home')}
            onGoToGuide={() => setActiveModule('tracking')}
          />
        ) : activeModule === 'tracking' ? (
          <ApplicationGuide onBackToHome={() => setActiveModule('home')} />
        ) : (
          <>
            {/* Hero Banner */}
            <section className="hero-card">
              <span className="badge-official">
                🛡️ {t('hero.badge')}
              </span>

          <h2 className="hero-heading">{t('hero.heading')}</h2>
          <p className="hero-description">{t('hero.description')}</p>

          <div className="voice-action-bar">
            {/* Primary Voice Touch Target */}
            <button
              type="button"
              onClick={() => setIsVoiceModalOpen(true)}
              className="speak-cta-btn"
              aria-label={t('hero.speak_button')}
            >
              <Mic className="mic-pulse-icon" />
              <span>{t('hero.speak_button')}</span>
            </button>

            {/* Accessible Text Fallback */}
            <form onSubmit={handleHeroSubmit} className="search-input-box">
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                placeholder={t('hero.type_placeholder')}
                aria-label={t('hero.type_placeholder')}
              />
              <button type="submit" className="ask-submit-btn">
                {t('hero.ask_button')}
              </button>
            </form>
          </div>
        </section>

        {/* Loading Indicator */}
        {isLoadingQuery && (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', padding: '1.5rem', background: '#eff6ff', borderRadius: '12px', marginBottom: '1.5rem', border: '1px solid #bfdbfe' }}>
            <Loader2 style={{ animation: 'spin 1s linear infinite' }} size={24} color="#2563eb" />
            <span style={{ fontWeight: 600, color: '#1e40af' }}>{t('status.loading')}</span>
          </div>
        )}

        {/* Dynamic Voice & Text Assistant Response Card */}
        {currentResponse && !isLoadingQuery && (
          <section className="response-card" style={{
            background: '#ffffff',
            border: '2px solid #bfdbfe',
            borderRadius: '16px',
            padding: '1.5rem',
            marginBottom: '2rem',
            boxShadow: '0 4px 12px rgba(37, 99, 235, 0.08)'
          }}>
            {/* User Question */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#1e40af', fontWeight: 600, marginBottom: '0.75rem' }}>
              <MessageSquareQuote size={20} />
              <span>{currentResponse.question}</span>
            </div>

            {/* Scheme Title Badge if matched */}
            {currentResponse.scheme_name && (
              <div style={{ display: 'inline-block', background: '#dbeafe', color: '#1e40af', padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.75rem' }}>
                🏛️ {currentResponse.scheme_name}
              </div>
            )}

            {/* Main Answer Text */}
            <p style={{ fontSize: '1.05rem', color: '#1e293b', lineHeight: 1.6, marginBottom: '1rem', whiteSpace: 'pre-line' }}>
              {currentResponse.answer}
            </p>

            {/* Interactive Clarification Options if Ambiguous */}
            {currentResponse.is_clarification && currentResponse.clarification_options && (
              <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '12px', border: '1.5px dashed #93c5fd', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#0369a1', fontWeight: 600, fontSize: '0.9rem', marginBottom: '0.75rem' }}>
                  <HelpCircle size={18} />
                  <span>{t('voice_recovery.or_choose')}</span>
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {currentResponse.clarification_options.map((opt, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => processQuery(opt.query)}
                      style={{
                        background: '#ffffff',
                        border: '1.5px solid #2563eb',
                        color: '#1d4ed8',
                        padding: '0.5rem 1rem',
                        borderRadius: '9999px',
                        fontSize: '0.875rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.4rem'
                      }}
                    >
                      <span>{opt.label}</span>
                      <ArrowRight size={14} />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/*
              AudioPlayer key={currentResponse._id} ensures React remounts the
              component on every new answer, which:
               - Stops the previous audio immediately
               - Starts fresh auto-play for the new answer
               - Prevents any stale text from replaying
            */}
            <AudioPlayer
              key={currentResponse._id}
              text={currentResponse.voice_summary || currentResponse.answer}
              lang={currentResponse.detected_language || currentLanguage}
              autoPlay={true}
            />

            {/* Official Source & Portal Link */}
            <div style={{ marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid #e2e8f0', fontSize: '0.825rem', color: '#64748b', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span>📜 {currentResponse.source}</span>
                {currentResponse.source_portal && (
                  <a
                    href={currentResponse.source_portal}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: '#2563eb', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '3px', textDecoration: 'none' }}
                  >
                    <span>{t('nav.home') === 'Home' ? 'Official Portal' : 'அரசு தளம்'}</span>
                    <ExternalLink size={14} />
                  </a>
                )}
              </div>
              <button
                type="button"
                onClick={() => { speechService.stop(); setCurrentResponse(null); }}
                style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontWeight: 600, textDecoration: 'underline' }}
              >
                {currentLanguage === 'ta' ? 'அகற்று' : currentLanguage === 'hi' ? 'हटाएं' : currentLanguage === 'mr' ? 'काढा' : currentLanguage === 'bn' ? 'মুছুন' : 'Clear'}
              </button>
            </div>
          </section>
        )}

        {/* Modules Overview */}
        <section className="modules-section">
          <div className="modules-grid">
            {/* Module A */}
            <div className="module-card">
              <div className="module-icon-wrap" style={{ background: '#eff6ff', color: '#1d4ed8' }}>
                <Sparkles size={24} />
              </div>
              <h3 className="module-title">{t('modules.assistant_title')}</h3>
              <p className="module-desc">{t('modules.assistant_desc')}</p>
              <button className="module-action-btn" onClick={() => setIsVoiceModalOpen(true)}>
                <span>{t('hero.ask_button')}</span>
                <ArrowRight size={16} />
              </button>
            </div>

            {/* Module B */}
            <div className="module-card">
              <div className="module-icon-wrap" style={{ background: '#ecfdf5', color: '#047857' }}>
                <CheckCircle2 size={24} />
              </div>
              <h3 className="module-title">{t('modules.recommend_title')}</h3>
              <p className="module-desc">{t('modules.recommend_desc')}</p>
              <button className="module-action-btn" onClick={() => setActiveModule('recommendations')}>
                <span>{t('voice_recovery.option_eligibility')}</span>
                <ArrowRight size={16} />
              </button>
            </div>

            {/* Module D */}
            <div className="module-card">
              <div className="module-icon-wrap" style={{ background: '#fffbeb', color: '#b45309' }}>
                <FileCheck size={24} />
              </div>
              <h3 className="module-title">{t('modules.doc_checker_title')}</h3>
              <p className="module-desc">{t('modules.doc_checker_desc')}</p>
              <button className="module-action-btn" onClick={() => setActiveModule('documents')}>
                <span>{t('voice_recovery.option_documents')}</span>
                <ArrowRight size={16} />
              </button>
            </div>

            {/* Module E */}
            <div className="module-card">
              <div className="module-icon-wrap" style={{ background: '#fdf2f8', color: '#be185d' }}>
                <BookOpen size={24} />
              </div>
              <h3 className="module-title">{t('modules.tracking_title')}</h3>
              <p className="module-desc">{t('modules.tracking_desc')}</p>
              <button className="module-action-btn" onClick={() => setActiveModule('tracking')}>
                <span>{t('voice_recovery.option_how_to_apply')}</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        </section>

        {/* Disclaimer Card */}
        <section style={{ marginTop: '2.5rem', padding: '1rem', background: '#f1f5f9', borderRadius: '12px', fontSize: '0.85rem', color: '#475569', textAlign: 'center' }}>
          <p>
            ℹ️ <strong>{t('disclaimers.source_label')}:</strong> {t('disclaimers.official_note')}
          </p>
        </section>
      </>
    )}
  </main>

      {/* Footer & Live Backend Status Indicator */}
      <footer className="status-bar">
        <span>© 2026 {t('app.title')} • {t('app.subtitle')}</span>
        <div className="status-pill">
          <span className={`status-dot ${backendStatus === 'online' ? '' : 'offline'}`} />
          <span>
            {backendStatus === 'online' ? t('status.backend_online') : t('status.backend_offline')}
          </span>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <MainApp />
    </LanguageProvider>
  );
}

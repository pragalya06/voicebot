import React, { useState, useEffect } from 'react';
import { Mic, ArrowRight, FileCheck, CheckCircle2, BookOpen, Sparkles, MessageSquareQuote, ExternalLink, HelpCircle, Loader2 } from 'lucide-react';
import { LanguageProvider, useTranslation } from './i18n';
import { Header } from './components/Header';
import { LanguageSelectorModal } from './components/LanguageSelectorModal';
import { VoiceInputModal } from './components/VoiceInputModal';
import { AudioPlayer } from './components/AudioPlayer';
import { EligibilityForm } from './components/EligibilityForm';
import { DocumentChecker } from './components/DocumentChecker';
import { ApplicationGuide } from './components/ApplicationGuide';

function MainApp() {
  const { t, currentLanguage } = useTranslation();
  const [backendStatus, setBackendStatus] = useState('checking');
  const [queryInput, setQueryInput] = useState('');
  const [activeModule, setActiveModule] = useState('home');
  const [isVoiceModalOpen, setIsVoiceModalOpen] = useState(false);
  
  // Active conversation response
  const [currentResponse, setCurrentResponse] = useState(null);

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
    setIsLoadingQuery(true);
    try {
      const res = await fetch('/api/assistant/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: questionText,
          language: queryLang
        })
      });

      if (!res.ok) throw new Error('API query failed');
      const data = await res.json();

      setCurrentResponse({
        question: questionText,
        detected_language: queryLang,
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
        disclaimer: data.disclaimer
      });
    } catch (err) {
      console.error('Error contacting assistant backend:', err);
      const isTamil = (queryLang === 'ta');
      setCurrentResponse({
        question: questionText,
        detected_language: queryLang,
        answer: isTamil
          ? 'பின்புல சேவையுடன் இணைப்பதில் சிக்கல் ஏற்பட்டது. உங்கள் இணைய இணைப்பை சரிபார்க்கவும்.'
          : 'Could not connect to the verification service. Please verify your connection.',
        voice_summary: isTamil
          ? 'சேவையில் பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.'
          : 'Service error occurred. Please try again.',
        source: isTamil ? 'சேவாமித்ரா உதவி' : 'SevaMitra Helpdesk',
        source_portal: 'https://tn.gov.in'
      });
    } finally {
      setIsLoadingQuery(false);
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
    const isTamil = currentLanguage === 'ta';

    let guideText = '';
    if (moduleName === 'recommendations') {
      guideText = isTamil
        ? 'திட்ட தகுதியை அறிய: உங்கள் வயது, தொழில் மற்றும் குடும்ப வருமானத்தை உள்ளிடவும்.'
        : 'Check scheme eligibility: Enter your age, occupation, and family income.';
    } else if (moduleName === 'documents') {
      guideText = isTamil
        ? 'ஆவண சரிபார்ப்பு: ஆதார் அல்லது வருமானச் சான்றிதழை பதிவேற்றி தயார்நிலையை சோதிக்கவும்.'
        : 'Document checker: Upload your Aadhaar or income proof to check readiness.';
    } else {
      guideText = isTamil
        ? 'விண்ணப்ப வழிகாட்டி: இ-சேவை மையம் செல்வதற்கு முன் தேவையான படிகளை வரிசையாக காணவும்.'
        : 'Application guide: Follow the ordered steps before visiting the e-Seva center.';
    }

    setCurrentResponse({
      question: isTamil ? 'தேர்ந்தெடுக்கப்பட்ட சேவை' : 'Selected Service',
      answer: guideText,
      source: isTamil ? 'சேவாமித்ரா வழிகாட்டி' : 'SevaMitra Guidance Desk'
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
                  <span>{currentLanguage === 'ta' ? 'கீழே உள்ள விருப்பங்களில் ஒன்றைத் தேர்ந்தெடுக்கவும்:' : 'Choose a specific option to proceed:'}</span>
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

            {/* Universal Audio Player reading Voice Summary in Detected Language */}
            <AudioPlayer
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
                    <span>{currentLanguage === 'ta' ? 'அரசு தளம்' : 'Official Portal'}</span>
                    <ExternalLink size={14} />
                  </a>
                )}
              </div>
              <button 
                type="button"
                onClick={() => setCurrentResponse(null)}
                style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontWeight: 600, textDecoration: 'underline' }}
              >
                {currentLanguage === 'ta' ? 'அகற்று' : 'Clear'}
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
                <span>Ask Question</span>
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
                <span>Check Eligibility</span>
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
                <span>Verify Papers</span>
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
                <span>View Checklist & Guide</span>
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

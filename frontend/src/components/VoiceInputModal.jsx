import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Mic, X, RefreshCw, HelpCircle, FileText, CheckCircle, Compass, Globe, Type } from 'lucide-react';
import { speechService } from '../services/speech';
import { useTranslation } from '../i18n';

/**
 * VoiceInputModal
 *
 * Improvements over previous version:
 *  1. Voice interruption: opening the modal (or retrying) immediately stops
 *     any currently playing assistant speech.
 *  2. Single recognizer: speechService.getRecognizer() aborts any previous
 *     session before creating a new one — no stacked sessions.
 *  3. modalState stale-closure fix: all handlers read from a ref (`modalStateRef`)
 *     rather than from captured state, so onend/onerror callbacks always see
 *     the current state.
 *  4. Submission guard: `submittedRef` prevents the same transcript from being
 *     submitted twice (e.g. from both `isFinal` branch and `onend`).
 *  5. Language detection: backend /api/speech/detect_language is called for all
 *     five supported languages. Client fallback handles network failures.
 *  6. Text input continues to work unchanged.
 */
export const VoiceInputModal = ({ isOpen, onClose, onQuerySubmit, onSelectOption }) => {
  const { currentLanguage, changeLanguage, t, isAudioMuted } = useTranslation();
  const [modalState, setModalState] = useState('LISTENING');
  const [transcript, setTranscript] = useState('');
  const [detectedInfo, setDetectedInfo] = useState(null);
  const [recoveryReason, setRecoveryReason] = useState('no_speech');
  const [textInput, setTextInput] = useState('');

  // ── Refs ─────────────────────────────────────────────────────────────────
  const recognitionRef = useRef(null);
  const timeoutRef = useRef(null);

  // Transcript ref: avoids stale closures in recognition callbacks
  const transcriptRef = useRef('');

  // modalState ref: lets onend/onerror read the CURRENT state (not captured)
  const modalStateRef = useRef('LISTENING');

  // Submission guard: prevents double-submission of the same transcript
  const submittedRef = useRef(false);

  // ── Sync modalState ref whenever state changes ────────────────────────────
  const setModalStateSynced = useCallback((newState) => {
    modalStateRef.current = newState;
    setModalState(newState);
  }, []);

  // Demo phrases for 1-click testing of language detection
  const demoVoicePhrases = [
    { lang: 'ta', label: '🇮🇳 தமிழ்', text: 'முதியோர் ஓய்வூதியத் திட்டம் பற்றி சொல்லுங்கள்' },
    { lang: 'hi', label: '🇮🇳 हिन्दी', text: 'पासपोर्ट के लिए आवेदन कैसे करें' },
    { lang: 'mr', label: '🇮🇳 मराठी', text: 'शेतकरी योजना कशी मिळेल मला माहिती पाहिजे' },
    { lang: 'bn', label: '🇮🇳 বাংলা', text: 'পাসপোর্ট আবেদন কিভাবে করবো' },
    { lang: 'en', label: '🌐 English', text: 'How do I apply for a passport?' },
  ];

  // ── Core: handle a recognized (or demo) transcript ───────────────────────
  const handleRecognizedText = useCallback(async (spokenText) => {
    if (!spokenText || !spokenText.trim()) return;

    // Guard: don't submit twice for the same utterance
    if (submittedRef.current) return;
    submittedRef.current = true;

    // Run backend language detection on the transcript text
    const detectResult = await speechService.detectLanguage(spokenText);
    const newLang = detectResult.detected_language;

    setDetectedInfo(detectResult);
    setModalStateSynced('DETECTED');

    // Switch full-page UI language if different from current
    if (newLang && newLang !== currentLanguage) {
      changeLanguage(newLang);
    }

    // Submit query after brief confirmation display
    setTimeout(() => {
      onQuerySubmit(spokenText, newLang);
      handleClose();
    }, 900);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentLanguage, changeLanguage, onQuerySubmit]);

  // ── Start listening ───────────────────────────────────────────────────────
  const startListening = useCallback(() => {
    // Stop any currently playing assistant speech immediately (voice interruption)
    speechService.interruptAll();

    // Reset all state for fresh session
    submittedRef.current = false;
    transcriptRef.current = '';
    setTranscript('');
    setDetectedInfo(null);
    setRecoveryReason('no_speech');
    setModalStateSynced('LISTENING');

    // Use current UI language as recognition locale.
    // Backend language detection on the transcript then confirms/corrects.
    // speechService.getRecognizer() automatically aborts any previous session.
    const recognizer = speechService.getRecognizer(currentLanguage);

    if (!recognizer) {
      setRecoveryReason('not_supported');
      setModalStateSynced('RECOVERY');
      return;
    }

    recognizer.onstart = () => {
      // Safety timeout: if no speech detected within 8 seconds, trigger recovery
      timeoutRef.current = setTimeout(() => {
        if (!transcriptRef.current) {
          try { recognizer.stop(); } catch (_) { /* already stopped */ }
          triggerRecovery('no_speech');
        }
      }, 8000);
    };

    recognizer.onresult = (event) => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);

      let currentText = '';
      for (let i = 0; i < event.results.length; i++) {
        currentText += event.results[i][0].transcript;
      }

      // Update BOTH state (for display) and ref (for reliable reading in callbacks)
      setTranscript(currentText);
      transcriptRef.current = currentText;

      if (event.results[0].isFinal) {
        recognizer.stop();
        handleRecognizedText(currentText);
      }
    };

    recognizer.onerror = (event) => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      console.warn('Speech recognition error:', event.error);

      if (event.error === 'no-speech') {
        triggerRecovery('no_speech');
      } else if (event.error === 'not-allowed') {
        triggerRecovery('not_allowed');
      } else if (event.error === 'aborted') {
        // Silently ignore — triggered by our own interruptAll() call
      } else {
        triggerRecovery('unclear');
      }
    };

    recognizer.onend = () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      // Use refs (not state) to read current values without stale closures
      if (!transcriptRef.current && modalStateRef.current === 'LISTENING' && !submittedRef.current) {
        triggerRecovery('no_speech');
      }
    };

    try {
      recognizer.start();
      recognitionRef.current = recognizer;
    } catch (err) {
      console.warn('Error starting recognition:', err);
      triggerRecovery('unclear');
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentLanguage, handleRecognizedText]);

  // ── Recovery ──────────────────────────────────────────────────────────────
  const triggerRecovery = useCallback((reason) => {
    setModalStateSynced('RECOVERY');
    setRecoveryReason(reason);
    if (!isAudioMuted && reason !== 'not_allowed') {
      const msg = reason === 'unclear'
        ? t('voice_recovery.unclear')
        : t('voice_recovery.no_speech');
      speechService.speak(msg, currentLanguage);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAudioMuted, currentLanguage, t]);

  // ── Text input submit ─────────────────────────────────────────────────────
  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (!textInput.trim()) return;
    handleRecognizedText(textInput.trim());
    setTextInput('');
  };

  // ── Close / cleanup ───────────────────────────────────────────────────────
  const handleClose = useCallback(() => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    // Stop recognition and speech
    speechService.interruptAll();
    recognitionRef.current = null;
    onClose();
  }, [onClose]);

  // ── Demo click ────────────────────────────────────────────────────────────
  const handleDemoClick = (phrase) => {
    // Stop any active recognition session before simulating
    speechService.stopRecognizer();
    setTranscript(phrase.text);
    transcriptRef.current = phrase.text;
    handleRecognizedText(phrase.text);
  };

  // ── Effect: start / stop when modal opens / closes ────────────────────────
  useEffect(() => {
    if (isOpen) {
      startListening();
    } else {
      // Modal closed externally — clean up everything
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      speechService.interruptAll();
      recognitionRef.current = null;
    }
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      speechService.interruptAll();
      recognitionRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  if (!isOpen) return null;

  // ─────────────────────────────────────────────────────────────────────────
  // Render
  // ─────────────────────────────────────────────────────────────────────────
  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="voice-modal-title">
      <div className="modal-content voice-modal" style={{ maxWidth: '520px' }}>

        {/* Close */}
        <button className="modal-close-btn" onClick={handleClose} aria-label="Close voice input">
          <X size={20} />
        </button>

        {/* ── DETECTED state ── */}
        {modalState === 'DETECTED' ? (
          <div style={{ textAlign: 'center', padding: '1.5rem 0' }}>
            <div style={{
              display: 'inline-flex', padding: '16px', borderRadius: '50%',
              background: '#ecfdf5', color: '#059669', marginBottom: '1rem', border: '2px solid #a7f3d0'
            }}>
              <Globe size={40} />
            </div>
            <div style={{
              display: 'inline-block', background: '#dbeafe', color: '#1e40af',
              padding: '0.35rem 0.85rem', borderRadius: '9999px', fontWeight: 700,
              fontSize: '0.85rem', marginBottom: '0.5rem'
            }}>
              ✨ {detectedInfo?.flag} {detectedInfo?.native_name} ({detectedInfo?.language_name}) Detected
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0f172a', marginBottom: '0.5rem' }}>
              Page switching to {detectedInfo?.native_name}
            </h3>
            <p style={{ color: '#475569', fontSize: '0.95rem', fontStyle: 'italic', margin: 0 }}>
              "{transcript}"
            </p>
          </div>

        /* ── LISTENING state ── */
        ) : modalState === 'LISTENING' ? (
          <div className="listening-state-view">
            <div className="mic-pulsing-orb" aria-hidden="true">
              <Mic size={36} color="#ffffff" />
            </div>
            <h2 id="voice-modal-title" className="voice-modal-title">
              {t('voice_recovery.listening')}
            </h2>
            <div className="transcript-preview-box">
              {transcript ? (
                <p className="live-transcript-text">"{transcript}"</p>
              ) : (
                <p className="listening-hint-text">
                  {t('voice_recovery.listening_hint') || 'Speak now — we will detect your language automatically.'}
                </p>
              )}
            </div>

            {/* Text-input fallback — always visible below mic */}
            <div style={{ marginTop: '1rem', width: '100%' }}>
              <button
                type="button"
                onClick={() => setModalStateSynced('TEXT_INPUT')}
                style={{
                  width: '100%', background: 'none', border: '1.5px dashed #94a3b8',
                  borderRadius: '10px', padding: '0.6rem 1rem', color: '#475569',
                  fontSize: '0.85rem', cursor: 'pointer', display: 'flex',
                  alignItems: 'center', justifyContent: 'center', gap: '0.5rem'
                }}
              >
                <Type size={16} />
                {t('voice_recovery.type_instead') || 'Prefer typing? Click here'}
              </button>
            </div>

            {/* 1-click demo phrases */}
            <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid #f1f5f9', width: '100%' }}>
              <p style={{ fontSize: '0.78rem', fontWeight: 700, color: '#64748b', marginBottom: '0.5rem', textAlign: 'center' }}>
                💡 {t('voice_recovery.demo_label') || 'Test language detection:'}
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', justifyContent: 'center' }}>
                {demoVoicePhrases.map((phrase, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleDemoClick(phrase)}
                    style={{
                      background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '9999px',
                      padding: '0.35rem 0.75rem', fontSize: '0.78rem', fontWeight: 600,
                      color: '#334155', cursor: 'pointer'
                    }}
                  >
                    {phrase.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

        /* ── TEXT INPUT state ── */
        ) : modalState === 'TEXT_INPUT' ? (
          <div style={{ padding: '1rem 0' }}>
            <h2 id="voice-modal-title" className="voice-modal-title" style={{ marginBottom: '1rem' }}>
              {t('voice_recovery.type_question') || 'Type your question'}
            </h2>
            <form onSubmit={handleTextSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <textarea
                autoFocus
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                placeholder={t('hero.type_placeholder') || "e.g. 'How do I apply for a passport?'"}
                rows={3}
                style={{
                  width: '100%', padding: '0.75rem', border: '1.5px solid #93c5fd',
                  borderRadius: '10px', fontSize: '1rem', resize: 'vertical',
                  fontFamily: 'inherit', outline: 'none'
                }}
              />
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  type="button"
                  onClick={() => { submittedRef.current = false; startListening(); }}
                  style={{
                    flex: 1, padding: '0.65rem', background: '#f1f5f9',
                    border: '1px solid #cbd5e1', borderRadius: '9999px',
                    fontWeight: 600, fontSize: '0.875rem', cursor: 'pointer', color: '#334155'
                  }}
                >
                  ← {t('voice_recovery.retry') || 'Use Mic Instead'}
                </button>
                <button
                  type="submit"
                  disabled={!textInput.trim()}
                  className="speak-cta-btn"
                  style={{ flex: 2, padding: '0.65rem 1rem', fontSize: '0.95rem' }}
                >
                  {t('hero.ask_button') || 'Ask Assistant'}
                </button>
              </div>
            </form>
          </div>

        /* ── RECOVERY state ── */
        ) : (
          <div className="recovery-state-view">
            <div className="recovery-icon-circle">
              <HelpCircle size={32} color="#ea580c" />
            </div>
            <h2 id="voice-modal-title" className="voice-modal-title">
              {recoveryReason === 'not_allowed'
                ? (t('voice_recovery.not_allowed') || 'Microphone permission denied.')
                : recoveryReason === 'unclear'
                  ? t('voice_recovery.unclear')
                  : t('voice_recovery.no_speech')}
            </h2>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', width: '100%' }}>
              {/* Retry mic */}
              {recoveryReason !== 'not_allowed' && (
                <button
                  onClick={() => { submittedRef.current = false; startListening(); }}
                  className="speak-cta-btn retry-speak-btn"
                >
                  <RefreshCw size={20} />
                  <span>{t('voice_recovery.retry')}</span>
                </button>
              )}

              {/* Switch to text input */}
              <button
                type="button"
                onClick={() => setModalStateSynced('TEXT_INPUT')}
                style={{
                  width: '100%', padding: '0.65rem 1rem', background: '#ffffff',
                  border: '1.5px solid #2563eb', borderRadius: '9999px', color: '#1d4ed8',
                  fontWeight: 700, fontSize: '0.875rem', cursor: 'pointer',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem'
                }}
              >
                <Type size={18} />
                <span>{t('voice_recovery.type_instead') || 'Type your question instead'}</span>
              </button>
            </div>

            {/* Quick-access options */}
            <div className="recovery-choices-container">
              <p className="recovery-choices-header">{t('voice_recovery.or_choose')}</p>
              <div className="recovery-chips-grid">
                <button type="button" className="recovery-chip-btn"
                  onClick={() => { handleClose(); onSelectOption('recommendations'); }}>
                  <CheckCircle size={18} color="#2563eb" />
                  <span>{t('voice_recovery.option_eligibility')}</span>
                </button>
                <button type="button" className="recovery-chip-btn"
                  onClick={() => { handleClose(); onSelectOption('documents'); }}>
                  <FileText size={18} color="#2563eb" />
                  <span>{t('voice_recovery.option_documents')}</span>
                </button>
                <button type="button" className="recovery-chip-btn"
                  onClick={() => { handleClose(); onSelectOption('documents'); }}>
                  <Compass size={18} color="#2563eb" />
                  <span>{t('voice_recovery.option_how_to_apply')}</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

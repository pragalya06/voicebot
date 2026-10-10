import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, X, RefreshCw, HelpCircle, FileText, CheckCircle, Search, Compass, Globe, Sparkles } from 'lucide-react';
import { speechService } from '../services/speech';
import { useTranslation } from '../i18n';

export const VoiceInputModal = ({ isOpen, onClose, onQuerySubmit, onSelectOption }) => {
  const { currentLanguage, changeLanguage, t, isAudioMuted } = useTranslation();
  const [modalState, setModalState] = useState('LISTENING'); // LISTENING | DETECTED | RECOVERY
  const [transcript, setTranscript] = useState('');
  const [detectedInfo, setDetectedInfo] = useState(null);
  const [recoveryReason, setRecoveryReason] = useState('no_speech');
  const recognitionRef = useRef(null);
  const timeoutRef = useRef(null);

  // Sample spoken phrases across verified Indian languages for 1-click test verification
  const demoVoicePhrases = [
    { lang: 'ta', label: '🇮🇳 தமிழ் (Tamil)', text: 'முதியோர் ஓய்வூதியத் திட்டம் பற்றி சொல்லுங்கள்' },
    { lang: 'hi', label: '🇮🇳 हिन्दी (Hindi)', text: 'मुझे किसान सम्मान निधि योजना की जानकारी चाहिए' },
    { lang: 'mr', label: '🇮🇳 मराठी (Marathi)', text: 'शेतकरी योजना कशी मिळेल मला माहिती पाहिजे' },
    { lang: 'bn', label: '🇮🇳 বাংলা (Bengali)', text: 'বৃদ্ধ পেনশন যোজনা সম্পর্কে জানতে চাই' },
    { lang: 'en', label: '🌐 English', text: 'Tell me about government pension schemes' },
  ];

  const handleRecognizedText = async (spokenText) => {
    if (!spokenText || !spokenText.trim()) return;

    // Run language detection
    const detectResult = await speechService.detectLanguage(spokenText);
    const newLang = detectResult.detected_language;

    setDetectedInfo(detectResult);
    setModalState('DETECTED');

    // Automatically adapt website language if different
    if (newLang && newLang !== currentLanguage) {
      changeLanguage(newLang);
    }

    // Submit query with detected language after brief confirmation visual
    setTimeout(() => {
      onQuerySubmit(spokenText, newLang);
      handleClose();
    }, 900);
  };

  const startListening = () => {
    setModalState('LISTENING');
    setTranscript('');
    setDetectedInfo(null);
    setRecoveryReason('no_speech');

    // Use current language or auto-fallback
    const recognizer = speechService.getRecognizer(currentLanguage);

    if (!recognizer) {
      setRecoveryReason('not_supported');
      setModalState('RECOVERY');
      speakRecoveryNotice('not_supported');
      return;
    }

    recognizer.onstart = () => {
      // 8-second safety timeout for silence detection
      timeoutRef.current = setTimeout(() => {
        if (!transcript) {
          recognizer.stop();
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
      setTranscript(currentText);

      // If final result obtained
      if (event.results[0].isFinal) {
        recognizer.stop();
        handleRecognizedText(currentText);
      }
    };

    recognizer.onerror = (event) => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      console.warn('Speech recognition event error:', event.error);

      if (event.error === 'no-speech') {
        triggerRecovery('no_speech');
      } else if (event.error === 'not-allowed') {
        triggerRecovery('not_allowed');
      } else {
        triggerRecovery('unclear');
      }
    };

    recognizer.onend = () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      if (!transcript && modalState === 'LISTENING') {
        triggerRecovery('no_speech');
      }
    };

    try {
      recognizer.start();
      recognitionRef.current = recognizer;
    } catch (err) {
      console.warn('Error starting speech recognition:', err);
      triggerRecovery('unclear');
    }
  };

  const triggerRecovery = (reason) => {
    setModalState('RECOVERY');
    setRecoveryReason(reason);
    speakRecoveryNotice(reason);
  };

  const speakRecoveryNotice = (reason) => {
    if (isAudioMuted) return;

    let messageToSpeak = t('voice_recovery.no_speech');
    if (reason === 'unclear') {
      messageToSpeak = t('voice_recovery.unclear');
    }

    speechService.speak(messageToSpeak, currentLanguage);
  };

  const handleClose = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {}
    }
    speechService.stop();
    onClose();
  };

  const handleDemoClick = (phrase) => {
    setTranscript(phrase.text);
    handleRecognizedText(phrase.text);
  };

  useEffect(() => {
    if (isOpen) {
      startListening();
    } else {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch (e) {}
      }
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    }

    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch (e) {}
      }
      speechService.stop();
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="voice-modal-title">
      <div className="modal-content voice-modal" style={{ maxWidth: '520px' }}>
        {/* Close Button */}
        <button className="modal-close-btn" onClick={handleClose} aria-label="Close voice input">
          <X size={20} />
        </button>

        {modalState === 'DETECTED' ? (
          /* Detected Language Transition State */
          <div style={{ textAlign: 'center', padding: '1.5rem 0' }}>
            <div style={{
              display: 'inline-flex',
              padding: '16px',
              borderRadius: '50%',
              background: '#ecfdf5',
              color: '#059669',
              marginBottom: '1rem',
              border: '2px solid #a7f3d0'
            }}>
              <Globe size={40} />
            </div>

            <div style={{
              display: 'inline-block',
              background: '#dbeafe',
              color: '#1e40af',
              padding: '0.35rem 0.85rem',
              borderRadius: '9999px',
              fontWeight: 700,
              fontSize: '0.85rem',
              marginBottom: '0.5rem'
            }}>
              ✨ {detectedInfo?.flag} {detectedInfo?.native_name} ({detectedInfo?.language_name}) Detected
            </div>

            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0f172a', marginBottom: '0.5rem' }}>
              Website Adapted to {detectedInfo?.native_name}
            </h3>

            <p style={{ color: '#475569', fontSize: '0.95rem', fontStyle: 'italic', margin: 0 }}>
              "{transcript}"
            </p>
          </div>
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
                  Speak in any language (Tamil, Hindi, Marathi, Bengali, English). We'll auto-detect it!
                </p>
              )}
            </div>

            {/* 1-Click Multi-Language Speech Verification Buttons */}
            <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid #f1f5f9', width: '100%' }}>
              <p style={{ fontSize: '0.785rem', fontWeight: 700, color: '#64748b', marginBottom: '0.5rem', textAlign: 'center' }}>
                💡 Or test 1-click spoken language detection:
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', justifyContent: 'center' }}>
                {demoVoicePhrases.map((phrase, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleDemoClick(phrase)}
                    style={{
                      background: '#f8fafc',
                      border: '1px solid #cbd5e1',
                      borderRadius: '9999px',
                      padding: '0.35rem 0.75rem',
                      fontSize: '0.785rem',
                      fontWeight: 600,
                      color: '#334155',
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '4px'
                    }}
                  >
                    <span>{phrase.label}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          /* Intelligent Voice Recovery View */
          <div className="recovery-state-view">
            <div className="recovery-icon-circle">
              <HelpCircle size={32} color="#ea580c" />
            </div>

            <h2 id="voice-modal-title" className="voice-modal-title">
              {recoveryReason === 'unclear'
                ? t('voice_recovery.unclear')
                : t('voice_recovery.no_speech')}
            </h2>

            {/* Retry Button */}
            <button
              onClick={startListening}
              className="speak-cta-btn retry-speak-btn"
            >
              <RefreshCw size={20} />
              <span>{t('voice_recovery.retry')}</span>
            </button>

            {/* Quick Service Recovery Choices */}
            <div className="recovery-choices-container">
              <p className="recovery-choices-header">
                {t('voice_recovery.or_choose')}
              </p>

              <div className="recovery-chips-grid">
                <button
                  type="button"
                  className="recovery-chip-btn"
                  onClick={() => {
                    handleClose();
                    onSelectOption('recommendations');
                  }}
                >
                  <CheckCircle size={18} color="#2563eb" />
                  <span>{t('voice_recovery.option_eligibility')}</span>
                </button>

                <button
                  type="button"
                  className="recovery-chip-btn"
                  onClick={() => {
                    handleClose();
                    onSelectOption('documents');
                  }}
                >
                  <FileText size={18} color="#2563eb" />
                  <span>{t('voice_recovery.option_documents')}</span>
                </button>

                <button
                  type="button"
                  className="recovery-chip-btn"
                  onClick={() => {
                    handleClose();
                    onSelectOption('tracking');
                  }}
                >
                  <Compass size={18} color="#2563eb" />
                  <span>{t('voice_recovery.option_how_to_apply')}</span>
                </button>

                <button
                  type="button"
                  className="recovery-chip-btn"
                  onClick={() => {
                    handleClose();
                    onSelectOption('tracking');
                  }}
                >
                  <Search size={18} color="#2563eb" />
                  <span>{t('voice_recovery.option_track_status')}</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

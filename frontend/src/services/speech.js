/**
 * Speech Service: Handles client-side Web Speech API for TTS (Text-to-Speech)
 * and STT (Speech-to-Text) with multi-language support for Indian languages:
 * Tamil (ta-IN), English (en-IN), Hindi (hi-IN), Marathi (mr-IN), and Bengali (bn-IN).
 *
 * Key design rules:
 *  - Only one utterance plays at a time. Calling speak() always cancels any
 *    current speech first (no duplicate/stacked speech).
 *  - Only one SpeechRecognition session runs at a time. Starting a new session
 *    aborts the previous one.
 *  - Language detection is done by the backend; the frontend script fallback
 *    handles network failures gracefully.
 *  - Language switching does NOT replay the previous answer — callers must
 *    explicitly pass the new text to speak().
 */

import { apiUrl } from './api';

const LOCALE_MAP = {
  ta: 'ta-IN',
  hi: 'hi-IN',
  mr: 'mr-IN',
  bn: 'bn-IN',
  en: 'en-IN',
};

class SpeechService {
  constructor() {
    this.synth = typeof window !== 'undefined' ? window.speechSynthesis : null;
    this.currentUtterance = null;
    this.voices = [];
    // Monotonically increasing token: each speak() call gets a new token.
    // Callbacks check this token to avoid acting on stale/cancelled speech.
    this._speakToken = 0;

    // Active SpeechRecognition instance — only one at a time.
    this._activeRecognizer = null;

    if (this.synth) {
      this.loadVoices();
      if (this.synth.onvoiceschanged !== undefined) {
        this.synth.onvoiceschanged = () => this.loadVoices();
      }
    }
  }

  loadVoices() {
    if (!this.synth) return;
    this.voices = this.synth.getVoices();
  }

  /**
   * Returns true if speech synthesis is currently playing.
   */
  get isSpeaking() {
    return this.synth ? this.synth.speaking : false;
  }

  /**
   * Speak given text in the specified language (ta, en, hi, mr, bn).
   * Always cancels any currently playing speech before starting.
   * Returns the speak token so callers can detect if their response was
   * superseded before it finishes.
   */
  speak(text, lang = 'en', onStart = null, onEnd = null, onError = null) {
    if (!this.synth) {
      if (onError) onError('Speech synthesis is not supported on this browser.');
      return -1;
    }

    // Cancel previous speech immediately (prevents stacking / replaying)
    this.stop();

    // Assign a new token for this utterance
    const token = ++this._speakToken;

    const utterance = new SpeechSynthesisUtterance(text);
    this.currentUtterance = utterance;

    const langLocale = LOCALE_MAP[lang] || 'en-IN';
    utterance.lang = langLocale;
    utterance.rate = 0.95; // Slightly slower pace for clear rural comprehension
    utterance.pitch = 1.0;

    // Pick best matching voice — re-fetch in case voices loaded after init
    const voices = this.synth.getVoices();
    if (voices.length > 0) this.voices = voices;

    const matchedVoice =
      this.voices.find((v) => v.lang === langLocale) ||
      this.voices.find((v) => v.lang.startsWith(lang)) ||
      this.voices.find((v) => v.lang.startsWith('en')); // graceful fallback

    if (matchedVoice) {
      utterance.voice = matchedVoice;
    }

    utterance.onstart = () => {
      // Guard: only fire if this is still the active speak() call
      if (token !== this._speakToken) return;
      if (onStart) onStart();
    };

    utterance.onend = () => {
      if (token !== this._speakToken) return;
      this.currentUtterance = null;
      if (onEnd) onEnd();
    };

    utterance.onerror = (event) => {
      // 'interrupted' fires when stop() cancels speech — not a real error
      if (event.error === 'interrupted' || event.error === 'canceled') return;
      if (token !== this._speakToken) return;
      this.currentUtterance = null;
      if (onError) onError(event);
    };

    this.synth.speak(utterance);
    return token;
  }

  /**
   * Stop speaking immediately. Cancels any pending / queued speech.
   */
  stop() {
    if (this.synth) {
      // Increment token so any in-flight callbacks become no-ops
      this._speakToken++;
      this.synth.cancel();
      this.currentUtterance = null;
    }
  }

  /**
   * Stop speaking AND stop any active recognizer immediately.
   * Used when the user interrupts to speak a new question.
   */
  interruptAll() {
    this.stop();
    this.stopRecognizer();
  }

  /**
   * Stop and discard the active SpeechRecognition session.
   */
  stopRecognizer() {
    if (this._activeRecognizer) {
      try { this._activeRecognizer.abort(); } catch (_) { /* already stopped */ }
      this._activeRecognizer = null;
    }
  }

  /**
   * Initialize browser Speech Recognition for a specific language.
   * Automatically aborts any previously running recognizer.
   */
  getRecognizer(lang = 'en') {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      return null;
    }

    // Abort any existing recognizer before creating a new one
    this.stopRecognizer();

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.lang = LOCALE_MAP[lang] || 'en-IN';

    // Track as the active recognizer
    this._activeRecognizer = recognition;

    return recognition;
  }

  /**
   * Identifies the language of spoken transcript via backend or script detection.
   * Falls back to client-side Unicode script analysis on network failure.
   */
  async detectLanguage(spokenText) {
    if (!spokenText || !spokenText.trim()) {
      return { detected_language: 'en', confidence: 0.0, is_uncertain: true };
    }

    try {
      const res = await fetch(apiUrl('/api/speech/detect_language'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: spokenText }),
      });

      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.warn('Backend language detection unreachable, using local fallback:', e);
    }

    // Client-side fallback script detection
    const text = spokenText.trim();

    if (/[\u0B80-\u0BFF]/.test(text)) {
      return { detected_language: 'ta', language_name: 'Tamil', native_name: 'தமிழ்', flag: '🇮🇳', confidence: 0.95 };
    }
    if (/[\u0980-\u09FF]/.test(text)) {
      return { detected_language: 'bn', language_name: 'Bengali', native_name: 'বাংলা', flag: '🇮🇳', confidence: 0.95 };
    }
    if (/[\u0900-\u097F]/.test(text)) {
      if (text.includes('ळ')) {
        return { detected_language: 'mr', language_name: 'Marathi', native_name: 'मराठी', flag: '🇮🇳', confidence: 0.96 };
      }
      // Check for Marathi lexical markers (whole words only)
      const words = new Set(text.split(/[\s,?.!;:'"\/।॥]+/));
      const marathiMarkers = new Set([
        'आहे', 'आहेत', 'नाही', 'नाहीत', 'शेतकरी', 'माहिती', 'कसे', 'कशी', 'कसा', 'काय',
        'अर्ज', 'मिळेल', 'पाहिजे', 'दाखला', 'परवाना', 'तक्रार', 'दुरुस्ती', 'पत्ता', 'नोंदणी', 'पॅन'
      ]);
      const hasMarathi = [...words].some((w) => marathiMarkers.has(w));
      if (hasMarathi) {
        return { detected_language: 'mr', language_name: 'Marathi', native_name: 'मराठी', flag: '🇮🇳', confidence: 0.94 };
      }
      return { detected_language: 'hi', language_name: 'Hindi', native_name: 'हिन्दी', flag: '🇮🇳', confidence: 0.92 };
    }

    return { detected_language: 'en', language_name: 'English', native_name: 'English', flag: '🌐', confidence: 0.85 };
  }
}

export const speechService = new SpeechService();

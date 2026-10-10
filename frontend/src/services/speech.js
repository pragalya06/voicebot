/**
 * Speech Service: Handles client-side Web Speech API for TTS (Text-to-Speech)
 * and STT (Speech-to-Text) with multi-language support for Indian languages:
 * Tamil (ta-IN), English (en-IN), Hindi (hi-IN), Marathi (mr-IN), and Bengali (bn-IN).
 */

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
   * Speak given text in the specified language (ta, en, hi, mr, bn)
   */
  speak(text, lang = 'en', onStart = null, onEnd = null, onError = null) {
    if (!this.synth) {
      if (onError) onError('Speech synthesis is not supported on this browser.');
      return;
    }

    // Stop any current utterance
    this.stop();

    const utterance = new SpeechSynthesisUtterance(text);
    this.currentUtterance = utterance;

    const langLocale = LOCALE_MAP[lang] || 'en-IN';
    utterance.lang = langLocale;
    utterance.rate = 0.95; // Slightly slower pace for clear rural comprehension
    utterance.pitch = 1.0;

    // Pick best matching voice
    const matchedVoice = this.voices.find(
      (v) => v.lang === langLocale || v.lang.startsWith(lang)
    );
    if (matchedVoice) {
      utterance.voice = matchedVoice;
    }

    utterance.onstart = () => {
      if (onStart) onStart();
    };

    utterance.onend = () => {
      this.currentUtterance = null;
      if (onEnd) onEnd();
    };

    utterance.onerror = (event) => {
      this.currentUtterance = null;
      if (onError) onError(event);
    };

    this.synth.speak(utterance);
  }

  /**
   * Stop speaking
   */
  stop() {
    if (this.synth) {
      this.synth.cancel();
      this.currentUtterance = null;
    }
  }

  /**
   * Initialize browser Speech Recognition for a specific language
   */
  getRecognizer(lang = 'en') {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      return null;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.lang = LOCALE_MAP[lang] || 'en-IN';

    return recognition;
  }

  /**
   * Identifies the language of spoken transcript via backend or script detection
   */
  async detectLanguage(spokenText) {
    if (!spokenText || !spokenText.trim()) {
      return { detected_language: 'en', confidence: 0.0, is_uncertain: true };
    }

    try {
      const res = await fetch('/api/speech/detect_language', {
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
      return { detected_language: 'ta', language_name: 'Tamil', native_name: 'தமிழ்', confidence: 0.95 };
    }
    if (/[\u0980-\u09FF]/.test(text)) {
      return { detected_language: 'bn', language_name: 'Bengali', native_name: 'বাংলা', confidence: 0.95 };
    }
    if (/[\u0900-\u097F]/.test(text)) {
      // Check for Marathi markers
      if (/आहे|नाही|शेतकरी|माहिती|कसे/.test(text)) {
        return { detected_language: 'mr', language_name: 'Marathi', native_name: 'मराठी', confidence: 0.92 };
      }
      return { detected_language: 'hi', language_name: 'Hindi', native_name: 'हिन्दी', confidence: 0.92 };
    }

    return { detected_language: 'en', language_name: 'English', native_name: 'English', confidence: 0.85 };
  }
}

export const speechService = new SpeechService();

import React, { useState, useEffect, useRef } from 'react';
import { RotateCcw, Square, AlertCircle } from 'lucide-react';
import { speechService } from '../services/speech';
import { useTranslation } from '../i18n';

/**
 * AudioPlayer — speaks the provided `text` in `lang`.
 *
 * Design rules:
 *  - Auto-plays when `text` changes (i.e. a new answer arrives).
 *  - Does NOT re-play when the UI language changes — language switching must
 *    not trigger old answers to replay.
 *  - Cancels speech on unmount or when text changes to a new value.
 *  - Only one utterance plays at a time (enforced by speechService).
 */
export const AudioPlayer = ({ text, lang = null, autoPlay = true }) => {
  const { currentLanguage, isAudioMuted, t } = useTranslation();
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasError, setHasError] = useState(false);

  // The language to use: explicit `lang` prop (from the response) takes
  // priority over the current UI language.
  const activeLang = lang || currentLanguage;

  // Track the speak token so we know if our utterance was superseded
  const tokenRef = useRef(-1);

  const handlePlay = () => {
    if (isAudioMuted || !text) return;
    setHasError(false);
    setIsPlaying(true);

    tokenRef.current = speechService.speak(
      text,
      activeLang,
      () => setIsPlaying(true),   // onStart
      () => setIsPlaying(false),  // onEnd
      (err) => {
        setIsPlaying(false);
        setHasError(true);
        console.warn('AudioPlayer TTS error:', err);
      }
    );
  };

  const handleStop = () => {
    speechService.stop();
    setIsPlaying(false);
  };

  // Auto-play when the text changes (new answer).
  // Deliberately NOT including `currentLanguage` — language switches must
  // not cause the previous answer to replay.
  useEffect(() => {
    if (!text) return;
    if (autoPlay && !isAudioMuted) {
      handlePlay();
    }
    return () => {
      // Stop speech when this answer is replaced / component unmounts
      speechService.stop();
      setIsPlaying(false);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [text, isAudioMuted]);

  return (
    <div className="audio-player-card" role="region" aria-label="Audio narration controls">
      <div className="audio-controls-row">
        {/* Play / Replay button */}
        {!isPlaying ? (
          <button
            type="button"
            onClick={handlePlay}
            disabled={isAudioMuted}
            className="audio-btn play-btn"
            title={t('audio.replay')}
          >
            <RotateCcw size={18} />
            <span>{t('audio.replay')}</span>
          </button>
        ) : (
          <button
            type="button"
            onClick={handleStop}
            className="audio-btn stop-btn"
            title={t('audio.stop')}
          >
            <Square size={16} fill="currentColor" />
            <span>{t('audio.stop')}</span>
          </button>
        )}

        {/* Audio state and animated wave */}
        <div className="audio-status-wrap">
          {isPlaying ? (
            <div className="sound-wave-indicator" aria-label="Audio playing">
              <span className="wave-bar bar-1"></span>
              <span className="wave-bar bar-2"></span>
              <span className="wave-bar bar-3"></span>
              <span className="wave-bar bar-4"></span>
              <span className="wave-label">{t('audio.playing')}</span>
            </div>
          ) : (
            <span className="audio-idle-label">
              {isAudioMuted ? t('nav.sound_off') : t('audio.play')}
            </span>
          )}
        </div>
      </div>

      {/* Error fallback message */}
      {hasError && (
        <div className="audio-error-banner" role="alert">
          <AlertCircle size={16} />
          <span>{t('audio.audio_error')}</span>
        </div>
      )}
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { Volume2, RotateCcw, Square, AlertCircle } from 'lucide-react';
import { speechService } from '../services/speech';
import { useTranslation } from '../i18n';

export const AudioPlayer = ({ text, lang = null, autoPlay = true, title = null }) => {
  const { currentLanguage, isAudioMuted, t } = useTranslation();
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasError, setHasError] = useState(false);

  const activeLang = lang || currentLanguage;

  const handlePlay = () => {
    if (isAudioMuted || !text) return;

    setHasError(false);
    setIsPlaying(true);

    speechService.speak(
      text,
      activeLang,
      () => setIsPlaying(true),
      () => setIsPlaying(false),
      () => {
        setIsPlaying(false);
        setHasError(true);
      }
    );
  };

  const handleStop = () => {
    speechService.stop();
    setIsPlaying(false);
  };

  // Auto-play when text changes, unless muted
  useEffect(() => {
    if (autoPlay && !isAudioMuted && text) {
      handlePlay();
    }
    return () => {
      speechService.stop();
      setIsPlaying(false);
    };
  }, [text, currentLanguage, isAudioMuted]);

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

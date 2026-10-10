import React, { createContext, useContext, useState, useEffect } from 'react';
import enTranslations from './en.json';
import taTranslations from './ta.json';
import hiTranslations from './hi.json';
import mrTranslations from './mr.json';
import bnTranslations from './bn.json';

const dictionaries = {
  en: enTranslations,
  ta: taTranslations,
  hi: hiTranslations,
  mr: mrTranslations,
  bn: bnTranslations,
};

const LanguageContext = createContext(null);

export const LanguageProvider = ({ children }) => {
  // Retrieve saved language from localStorage, or default to null for first-time prompt
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    return localStorage.getItem('user_language') || 'ta'; // Default to Tamil for rural TN focus, or prompt
  });

  const [hasSelectedLanguage, setHasSelectedLanguage] = useState(() => {
    return localStorage.getItem('user_language_selected') === 'true';
  });

  const [isAudioMuted, setIsAudioMuted] = useState(() => {
    return localStorage.getItem('user_audio_muted') === 'true';
  });

  // Switch language and save to local storage
  const changeLanguage = (langCode) => {
    if (dictionaries[langCode]) {
      setCurrentLanguage(langCode);
      setHasSelectedLanguage(true);
      localStorage.setItem('user_language', langCode);
      localStorage.setItem('user_language_selected', 'true');
      document.documentElement.lang = langCode;
    }
  };

  const toggleAudioMute = () => {
    setIsAudioMuted((prev) => {
      const next = !prev;
      localStorage.setItem('user_audio_muted', String(next));
      if (next && window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
      return next;
    });
  };

  useEffect(() => {
    document.documentElement.lang = currentLanguage;
  }, [currentLanguage]);

  // Nested key resolver, e.g. t('hero.heading')
  const t = (path) => {
    const keys = path.split('.');
    let current = dictionaries[currentLanguage] || dictionaries.en;
    for (const key of keys) {
      if (current && typeof current === 'object' && key in current) {
        current = current[key];
      } else {
        // Fallback to English if translation is missing
        let fallback = dictionaries.en;
        for (const fbKey of keys) {
          if (fallback && typeof fallback === 'object' && fbKey in fallback) {
            fallback = fallback[fbKey];
          } else {
            return path; // Return key path if not found
          }
        }
        return fallback || path;
      }
    }
    return current;
  };

  return (
    <LanguageContext.Provider
      value={{
        currentLanguage,
        changeLanguage,
        hasSelectedLanguage,
        setHasSelectedLanguage,
        isAudioMuted,
        toggleAudioMute,
        t,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useTranslation must be used within a LanguageProvider');
  }
  return context;
};

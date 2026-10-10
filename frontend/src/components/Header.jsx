import React from 'react';
import { Volume2, VolumeX, Globe } from 'lucide-react';
import { useTranslation } from '../i18n';

export const Header = ({ activeTab, setActiveTab }) => {
  const { currentLanguage, changeLanguage, isAudioMuted, toggleAudioMute, t } = useTranslation();

  return (
    <header className="site-header">
      <div className="header-inner">
        <div className="brand-section" role="banner" style={{ cursor: 'pointer' }} onClick={() => setActiveTab('home')}>
          <div className="brand-logo-badge" aria-hidden="true">
            🏛️
          </div>
          <div>
            <h1 className="brand-text-title">{t('app.title')}</h1>
            <p className="brand-text-sub">{t('app.subtitle')}</p>
          </div>
        </div>

        {/* Primary Navigation Tabs */}
        <nav style={{ display: 'flex', gap: '0.4rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <button
            type="button"
            onClick={() => setActiveTab('home')}
            style={{
              background: activeTab === 'home' ? '#eff6ff' : 'transparent',
              color: activeTab === 'home' ? '#1e40af' : '#475569',
              fontWeight: 600,
              padding: '0.4rem 0.75rem',
              borderRadius: '9999px',
              border: activeTab === 'home' ? '1px solid #bfdbfe' : '1px solid transparent',
              fontSize: '0.85rem'
            }}
          >
            {t('nav.home')}
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('recommendations')}
            style={{
              background: activeTab === 'recommendations' ? '#eff6ff' : 'transparent',
              color: activeTab === 'recommendations' ? '#1e40af' : '#475569',
              fontWeight: 600,
              padding: '0.4rem 0.75rem',
              borderRadius: '9999px',
              border: activeTab === 'recommendations' ? '1px solid #bfdbfe' : '1px solid transparent',
              fontSize: '0.85rem'
            }}
          >
            {t('nav.recommendations')}
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('documents')}
            style={{
              background: activeTab === 'documents' ? '#eff6ff' : 'transparent',
              color: activeTab === 'documents' ? '#1e40af' : '#475569',
              fontWeight: 600,
              padding: '0.4rem 0.75rem',
              borderRadius: '9999px',
              border: activeTab === 'documents' ? '1px solid #bfdbfe' : '1px solid transparent',
              fontSize: '0.85rem'
            }}
          >
            {t('nav.documents')}
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('tracking')}
            style={{
              background: activeTab === 'tracking' ? '#eff6ff' : 'transparent',
              color: activeTab === 'tracking' ? '#1e40af' : '#475569',
              fontWeight: 600,
              padding: '0.4rem 0.75rem',
              borderRadius: '9999px',
              border: activeTab === 'tracking' ? '1px solid #bfdbfe' : '1px solid transparent',
              fontSize: '0.85rem'
            }}
          >
            {t('nav.tracking')}
          </button>
        </nav>

        <div className="header-controls">
          {/* Audio Mute/Unmute toggle */}
          <button
            onClick={toggleAudioMute}
            className={`icon-btn ${!isAudioMuted ? 'active' : ''}`}
            title={isAudioMuted ? t('nav.sound_off') : t('nav.sound_on')}
            aria-label={isAudioMuted ? t('nav.sound_off') : t('nav.sound_on')}
          >
            {isAudioMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
          </button>

          {/* Multilingual Selector (TA, EN, HI, MR, BN) */}
          <div className="lang-selector-group" role="group" aria-label={t('nav.language')} style={{ display: 'flex', gap: '2px', background: '#f1f5f9', padding: '3px', borderRadius: '9999px', border: '1px solid #cbd5e1' }}>
            <button
              onClick={() => changeLanguage('ta')}
              className={`lang-btn ${currentLanguage === 'ta' ? 'active' : ''}`}
              title="தமிழுக்கு மாற்றவும்"
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem', borderRadius: '9999px' }}
            >
              தமிழ்
            </button>
            <button
              onClick={() => changeLanguage('hi')}
              className={`lang-btn ${currentLanguage === 'hi' ? 'active' : ''}`}
              title="हिन्दी में बदलें"
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem', borderRadius: '9999px' }}
            >
              हिन्दी
            </button>
            <button
              onClick={() => changeLanguage('mr')}
              className={`lang-btn ${currentLanguage === 'mr' ? 'active' : ''}`}
              title="मराठीत बदला"
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem', borderRadius: '9999px' }}
            >
              मराठी
            </button>
            <button
              onClick={() => changeLanguage('bn')}
              className={`lang-btn ${currentLanguage === 'bn' ? 'active' : ''}`}
              title="বাংলায় পরিবর্তন করুন"
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem', borderRadius: '9999px' }}
            >
              বাংলা
            </button>
            <button
              onClick={() => changeLanguage('en')}
              className={`lang-btn ${currentLanguage === 'en' ? 'active' : ''}`}
              title="Switch to English"
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem', borderRadius: '9999px' }}
            >
              EN
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

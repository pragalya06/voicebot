import React, { useState } from 'react';
import { Globe, Check, Sparkles } from 'lucide-react';
import { useTranslation } from '../i18n';

export const LanguageSelectorModal = () => {
  const { currentLanguage, changeLanguage, hasSelectedLanguage, setHasSelectedLanguage, t } = useTranslation();
  const [selectedLang, setSelectedLang] = useState(currentLanguage || 'en');

  // If already selected previously, do not render modal
  if (hasSelectedLanguage) {
    return null;
  }

  const handleConfirm = () => {
    changeLanguage(selectedLang);
    setHasSelectedLanguage(true);
  };

  const availableLanguages = [
    { code: 'ta', native: 'தமிழ்', name: 'Tamil', desc: 'அனைத்து அரசுத் திட்டங்கள் மற்றும் குரல் வழிகாட்டல்' },
    { code: 'hi', native: 'हिन्दी', name: 'Hindi', desc: 'सभी सरकारी योजनाएं एवं आवाज में मार्गदर्शन' },
    { code: 'mr', native: 'मराठी', name: 'Marathi', desc: 'सर्व शासकीय योजना व आवाजात माहिती' },
    { code: 'bn', native: 'বাংলা', name: 'Bengali', desc: 'সমস্ত সরকারি প্রকল্প ও ভয়েস নির্দেশিকা' },
    { code: 'en', native: 'English', name: 'English', desc: 'All verified government schemes & voice guidance' },
  ];

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="lang-modal-title">
      <div className="modal-content" style={{ maxWidth: '520px' }}>
        <div style={{ display: 'inline-flex', padding: '10px', borderRadius: '50%', background: '#dbeafe', color: '#1e40af', marginBottom: '12px' }}>
          <Globe size={32} />
        </div>
        <h2 id="lang-modal-title" style={{ fontSize: '1.35rem', color: '#1e293b', marginBottom: '6px' }}>
          Choose Your Language / மொழியைத் தேர்ந்தெடுக்கவும்
        </h2>
        <p style={{ fontSize: '0.9rem', color: '#64748b', marginBottom: '1rem' }}>
          Select your preferred language, or speak anytime—the system automatically detects your spoken language!
        </p>

        <div className="lang-options-grid" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '0.5rem', marginBottom: '1.25rem' }}>
          {availableLanguages.map((lang) => (
            <button
              key={lang.code}
              type="button"
              className={`lang-choice-card ${selectedLang === lang.code ? 'selected' : ''}`}
              onClick={() => setSelectedLang(lang.code)}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '0.75rem 1rem',
                borderRadius: '12px',
                border: `2px solid ${selectedLang === lang.code ? '#2563eb' : '#e2e8f0'}`,
                background: selectedLang === lang.code ? '#eff6ff' : '#ffffff',
                cursor: 'pointer',
                textAlign: 'left'
              }}
            >
              <div>
                <div style={{ fontWeight: 800, fontSize: '1.05rem', color: selectedLang === lang.code ? '#1e40af' : '#1e293b' }}>
                  {lang.native} <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#64748b' }}>({lang.name})</span>
                </div>
                <div style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '2px' }}>
                  {lang.desc}
                </div>
              </div>
              {selectedLang === lang.code && <Check size={20} color="#2563eb" />}
            </button>
          ))}
        </div>

        <button
          onClick={handleConfirm}
          className="speak-cta-btn"
          style={{ width: '100%', padding: '0.9rem', fontSize: '1rem' }}
        >
          {t('lang_modal.confirm') || 'Continue / தொடரவும்'}
        </button>

        <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '12px' }}>
          {t('lang_modal.remember_note')}
        </p>
      </div>
    </div>
  );
};

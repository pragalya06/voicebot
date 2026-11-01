import React, { useState } from 'react';
import { CheckCircle, AlertTriangle, FileText, ExternalLink, Volume2 } from 'lucide-react';
import { speechService } from '../services/speech';
import { useTranslation } from '../i18n';

export const SchemeCard = ({ scheme }) => {
  const { currentLanguage, isAudioMuted, t } = useTranslation();
  const [isSpeaking, setIsSpeaking] = useState(false);

  const handleSpeakScheme = () => {
    if (isAudioMuted) return;
    setIsSpeaking(true);

    const benefitLabel = t('scheme_card.speak_benefit') || 'Benefit';
    const whyLabel = t('scheme_card.speak_why') || 'Why it matches';
    const fallbackCriteria = t('scheme_card.criteria_met') || 'Criteria fulfilled';
    const textToSpeak = `${scheme.scheme_name}. ${benefitLabel}: ${scheme.benefit}. ${whyLabel}: ${scheme.why_matched[0] || fallbackCriteria}.`;

    speechService.speak(
      textToSpeak,
      currentLanguage,
      () => setIsSpeaking(true),
      () => setIsSpeaking(false),
      () => setIsSpeaking(false)
    );
  };

  const getBadgeColor = (score) => {
    if (score >= 70) return { bg: '#dcfce7', text: '#15803d', border: '#86efac' };
    if (score >= 40) return { bg: '#fef3c7', text: '#b45309', border: '#fde68a' };
    return { bg: '#f1f5f9', text: '#64748b', border: '#cbd5e1' };
  };

  const badge = getBadgeColor(scheme.match_score);

  return (
    <div className="recommendation-card" style={{
      background: '#ffffff',
      border: '1.5px solid #e2e8f0',
      borderRadius: '16px',
      padding: '1.5rem',
      marginBottom: '1.25rem',
      boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
      position: 'relative'
    }}>
      {/* Top Header: Title & Match Score Badge */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem', marginBottom: '0.75rem', flexWrap: 'wrap' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase', fontWeight: 600, letterSpacing: '0.5px' }}>
            {scheme.category}
          </span>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1e3a8a', marginTop: '2px' }}>
            {scheme.scheme_name}
          </h3>
        </div>

        <div style={{
          background: badge.bg,
          color: badge.text,
          border: `1px solid ${badge.border}`,
          borderRadius: '9999px',
          padding: '0.35rem 0.85rem',
          fontSize: '0.875rem',
          fontWeight: 700,
          display: 'flex',
          alignItems: 'center',
          gap: '4px'
        }}>
          <span>{scheme.match_score}%</span>
          <span>{t('scheme_card.match')}</span>
        </div>
      </div>

      {/* Benefit Highlight Box */}
      <div style={{ background: '#eff6ff', borderRadius: '10px', padding: '0.75rem 1rem', marginBottom: '1rem', borderLeft: '4px solid #2563eb' }}>
        <p style={{ fontSize: '0.95rem', color: '#1e40af', fontWeight: 600 }}>
          🎁 {scheme.benefit}
        </p>
      </div>

      {/* Why Matched List */}
      {scheme.why_matched && scheme.why_matched.length > 0 && (
        <div style={{ marginBottom: '0.75rem' }}>
          <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: '#166534', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
            <CheckCircle size={16} />
            <span>{t('scheme_card.why_matched')}</span>
          </h4>
          <ul style={{ listStyle: 'none', paddingLeft: '1.25rem', fontSize: '0.875rem', color: '#334155' }}>
            {scheme.why_matched.map((r, i) => (
              <li key={i} style={{ marginBottom: '3px', position: 'relative' }}>
                <span style={{ position: 'absolute', left: '-1rem', color: '#16a34a' }}>✔</span>
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Missing Requirements / Verification Check */}
      {scheme.missing_info && scheme.missing_info.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: '#b45309', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
            <AlertTriangle size={16} />
            <span>{t('scheme_card.missing_reqs')}</span>
          </h4>
          <ul style={{ listStyle: 'none', paddingLeft: '1.25rem', fontSize: '0.875rem', color: '#64748b' }}>
            {scheme.missing_info.map((m, i) => (
              <li key={i} style={{ marginBottom: '3px', position: 'relative' }}>
                <span style={{ position: 'absolute', left: '-1rem', color: '#f59e0b' }}>⚠</span>
                {m}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Required Documents Checklist Preview */}
      <div style={{ background: '#f8fafc', padding: '0.75rem 1rem', borderRadius: '10px', marginBottom: '1rem', border: '1px dashed #cbd5e1' }}>
        <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#475569', display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '4px' }}>
          <FileText size={14} />
          {t('scheme_card.required_docs')}
        </span>
        <p style={{ fontSize: '0.825rem', color: '#64748b' }}>
          {scheme.required_documents.join(' • ')}
        </p>
      </div>

      {/* Action Footer */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem', paddingTop: '0.5rem', borderTop: '1px solid #f1f5f9' }}>
        {/* Listen Button */}
        <button
          type="button"
          onClick={handleSpeakScheme}
          disabled={isAudioMuted}
          style={{
            background: '#f1f5f9',
            border: '1px solid #cbd5e1',
            borderRadius: '9999px',
            padding: '0.4rem 0.85rem',
            fontSize: '0.85rem',
            fontWeight: 600,
            color: '#1e293b',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            cursor: 'pointer'
          }}
        >
          <Volume2 size={16} color="#2563eb" />
          <span>{isSpeaking ? (t('audio.playing') || 'Reading...') : (t('audio.play') || 'Listen')}</span>
        </button>

        {/* Official Portal Link */}
        <a
          href={scheme.official_portal}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '4px',
            color: '#2563eb',
            fontWeight: 600,
            fontSize: '0.875rem',
            textDecoration: 'none'
          }}
        >
          <span>{t('scheme_card.official_portal')}</span>
          <ExternalLink size={14} />
        </a>
      </div>
    </div>
  );
};

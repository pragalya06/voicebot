import React, { useState } from 'react';
import { UserCheck, Sparkles, Filter, RotateCcw, Loader2 } from 'lucide-react';
import { useTranslation } from '../i18n';
import { SchemeCard } from './SchemeCard';
import { AudioPlayer } from './AudioPlayer';
import { apiUrl } from '../services/api';

export const EligibilityForm = ({ onBackToHome }) => {
  const { currentLanguage, t } = useTranslation();

  // Form State
  const [age, setAge] = useState(45);
  const [gender, setGender] = useState('female');
  const [occupation, setOccupation] = useState('homemaker');
  const [incomeRange, setIncomeRange] = useState(24000);
  const [hasLand, setHasLand] = useState(false);
  const [maritalStatus, setMaritalStatus] = useState('married');

  // Results State
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const res = await fetch(apiUrl('/api/schemes/recommend'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: Number(age),
          gender,
          occupation,
          annual_income: Number(incomeRange),
          is_rural: true,
          has_cultivable_land: Boolean(hasLand),
          marital_status: maritalStatus,
          language: currentLanguage
        })
      });

      if (!res.ok) throw new Error('Recommendation request failed');
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error('Error fetching scheme recommendations:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="eligibility-container" style={{ maxWidth: '850px', margin: '0 auto' }}>
      {/* Header Banner */}
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <span className="badge-official">
          ✨ {t('eligibility.badge')}
        </span>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#1e3a8a', marginTop: '6px' }}>
          {t('eligibility.heading')}
        </h2>
        <p style={{ color: '#64748b', fontSize: '0.95rem', marginTop: '4px' }}>
          {t('eligibility.description')}
        </p>
      </div>

      {!results ? (
        /* Interview Form */
        <form onSubmit={handleSubmit} style={{
          background: '#ffffff',
          borderRadius: '16px',
          border: '1.5px solid #cbd5e1',
          padding: '2rem',
          boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
        }}>
          {/* Question 1: Age */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
              1. {t('eligibility.q_age')} ({age} {t('eligibility.years')})
            </label>
            <input
              type="range"
              min="18"
              max="90"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              style={{ width: '100%', accentColor: '#2563eb' }}
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: '#64748b' }}>
              <span>18</span>
              <span>40</span>
              <span>{t('eligibility.age_oap')}</span>
              <span>90</span>
            </div>
          </div>

          {/* Question 2: Gender */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
              2. {t('eligibility.q_gender')}
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
              <button
                type="button"
                onClick={() => setGender('female')}
                className={`lang-choice-card ${gender === 'female' ? 'selected' : ''}`}
                style={{ textAlign: 'center', padding: '0.85rem' }}
              >
                <span style={{ fontWeight: 700 }}>👩 {t('eligibility.female')}</span>
              </button>
              <button
                type="button"
                onClick={() => setGender('male')}
                className={`lang-choice-card ${gender === 'male' ? 'selected' : ''}`}
                style={{ textAlign: 'center', padding: '0.85rem' }}
              >
                <span style={{ fontWeight: 700 }}>👨 {t('eligibility.male')}</span>
              </button>
            </div>
          </div>

          {/* Question 3: Occupation */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
              3. {t('eligibility.q_occupation')}
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
              <button
                type="button"
                onClick={() => { setOccupation('farmer'); setHasLand(true); }}
                className={`lang-choice-card ${occupation === 'farmer' ? 'selected' : ''}`}
                style={{ padding: '0.75rem' }}
              >
                <span style={{ fontWeight: 700 }}>🌾 {t('eligibility.farmer')}</span>
              </button>
              <button
                type="button"
                onClick={() => { setOccupation('homemaker'); }}
                className={`lang-choice-card ${occupation === 'homemaker' ? 'selected' : ''}`}
                style={{ padding: '0.75rem' }}
              >
                <span style={{ fontWeight: 700 }}>🏠 {t('eligibility.homemaker')}</span>
              </button>
              <button
                type="button"
                onClick={() => { setOccupation('laborer'); }}
                className={`lang-choice-card ${occupation === 'laborer' ? 'selected' : ''}`}
                style={{ padding: '0.75rem' }}
              >
                <span style={{ fontWeight: 700 }}>🔨 {t('eligibility.laborer')}</span>
              </button>
              <button
                type="button"
                onClick={() => { setOccupation('other'); }}
                className={`lang-choice-card ${occupation === 'other' ? 'selected' : ''}`}
                style={{ padding: '0.75rem' }}
              >
                <span style={{ fontWeight: 700 }}>💼 {t('eligibility.other_retired')}</span>
              </button>
            </div>
          </div>

          {/* Question 4: Annual Family Income */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
              4. {t('eligibility.q_income')}
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
              <button
                type="button"
                onClick={() => setIncomeRange(20000)}
                className={`lang-choice-card ${incomeRange <= 24000 ? 'selected' : ''}`}
                style={{ padding: '0.75rem' }}
              >
                <span style={{ fontWeight: 700 }}>≤ ₹24,000</span>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{t('eligibility.bpl')}</span>
              </button>
              <button
                type="button"
                onClick={() => setIncomeRange(100000)}
                className={`lang-choice-card ${incomeRange > 24000 && incomeRange <= 120000 ? 'selected' : ''}`}
                style={{ padding: '0.75rem' }}
              >
                <span style={{ fontWeight: 700 }}>₹24,000 - ₹1.2 Lakh</span>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{t('eligibility.cmchis_cap')}</span>
              </button>
              <button
                type="button"
                onClick={() => setIncomeRange(200000)}
                className={`lang-choice-card ${incomeRange > 120000 && incomeRange <= 250000 ? 'selected' : ''}`}
                style={{ padding: '0.75rem' }}
              >
                <span style={{ fontWeight: 700 }}>₹1.2 - ₹2.5 Lakh</span>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{t('eligibility.kmut_ceiling')}</span>
              </button>
              <button
                type="button"
                onClick={() => setIncomeRange(350000)}
                className={`lang-choice-card ${incomeRange > 250000 ? 'selected' : ''}`}
                style={{ padding: '0.75rem' }}
              >
                <span style={{ fontWeight: 700 }}>&gt; ₹2.5 Lakh</span>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{t('eligibility.general')}</span>
              </button>
            </div>
          </div>

          {/* Question 5: Marital Status */}
          <div style={{ marginBottom: '2rem' }}>
            <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
              5. {t('eligibility.q_marital')}
            </label>
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
              <button
                type="button"
                onClick={() => setMaritalStatus('married')}
                className={`lang-choice-card ${maritalStatus === 'married' ? 'selected' : ''}`}
                style={{ flex: 1, padding: '0.65rem', textAlign: 'center' }}
              >
                <span style={{ fontWeight: 600 }}>{t('eligibility.married')}</span>
              </button>
              <button
                type="button"
                onClick={() => setMaritalStatus('widow')}
                className={`lang-choice-card ${maritalStatus === 'widow' ? 'selected' : ''}`}
                style={{ flex: 1, padding: '0.65rem', textAlign: 'center' }}
              >
                <span style={{ fontWeight: 600 }}>{t('eligibility.widowed')}</span>
              </button>
              <button
                type="button"
                onClick={() => setMaritalStatus('single')}
                className={`lang-choice-card ${maritalStatus === 'single' ? 'selected' : ''}`}
                style={{ flex: 1, padding: '0.65rem', textAlign: 'center' }}
              >
                <span style={{ fontWeight: 600 }}>{t('eligibility.single')}</span>
              </button>
            </div>
          </div>

          {/* Submit CTA */}
          <button
            type="submit"
            disabled={isLoading}
            className="speak-cta-btn"
            style={{ width: '100%', padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem' }}
          >
            {isLoading ? <Loader2 style={{ animation: 'spin 1s linear infinite' }} size={22} /> : <Sparkles size={22} />}
            <span>{isLoading ? t('eligibility.evaluating') : t('eligibility.find_schemes_btn')}</span>
          </button>
        </form>
      ) : (
        /* Recommendation Results View */
        <div>
          {/* Results Header Card with Audio Narration */}
          <div style={{
            background: '#ffffff',
            border: '2px solid #93c5fd',
            borderRadius: '16px',
            padding: '1.5rem',
            marginBottom: '1.5rem',
            boxShadow: '0 4px 12px rgba(37,99,235,0.06)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <UserCheck size={24} color="#15803d" />
                <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#1e3a8a' }}>
                  {t('eligibility.recommended_heading')} ({results.matched_count} {t('eligibility.high_matches')})
                </h3>
              </div>

              <button
                type="button"
                onClick={() => setResults(null)}
                style={{
                  background: '#f1f5f9',
                  border: '1px solid #cbd5e1',
                  borderRadius: '9999px',
                  padding: '0.4rem 0.85rem',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  color: '#334155',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                  cursor: 'pointer'
                }}
              >
                <RotateCcw size={14} />
                <span>{t('eligibility.modify_answers')}</span>
              </button>
            </div>

            {/* Read-Aloud Voice Audio Player */}
            <AudioPlayer text={results.voice_summary} autoPlay={true} />
          </div>

          {/* List of Scheme Cards */}
          <div>
            {results.recommendations.map((item) => (
              <SchemeCard key={item.scheme_id} scheme={item} />
            ))}
          </div>

          {/* Back Navigation */}
          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <button
              type="button"
              onClick={onBackToHome}
              style={{
                background: 'none',
                border: 'none',
                color: '#2563eb',
                fontWeight: 700,
                fontSize: '0.95rem',
                cursor: 'pointer',
                textDecoration: 'underline'
              }}
            >
              ← {t('eligibility.back_to_home')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { BookOpen, CheckSquare, Search, Clock, ShieldAlert, ArrowRight, CheckCircle2, AlertTriangle, UserCheck, MapPin, RefreshCw } from 'lucide-react';
import { useTranslation } from '../i18n';
import { AudioPlayer } from './AudioPlayer';
import { apiUrl } from '../services/api';

export const ApplicationGuide = ({ onBackToHome, initialScheme = 'old_age_pension' }) => {
  const { currentLanguage, t } = useTranslation();

  const getLocalized = (obj, field) => {
    if (!obj) return '';
    return obj[`${field}_${currentLanguage}`] || obj[`${field}_en`] || '';
  };

  const [activeSubTab, setActiveSubTab] = useState('roadmap'); // 'roadmap', 'checklist', 'tracker'
  const [selectedScheme, setSelectedScheme] = useState(initialScheme);
  const [roadmapData, setRoadmapData] = useState(null);
  const [isLoadingRoadmap, setIsLoadingRoadmap] = useState(false);

  // Saved Checklist State (Persisted in localStorage)
  const [checkedDocs, setCheckedDocs] = useState({});

  // Tracker State
  const [refInput, setRefInput] = useState('');
  const [trackerResult, setTrackerResult] = useState(null);
  const [isTracking, setIsTracking] = useState(false);

  // Load Scheme Roadmap from Backend
  useEffect(() => {
    setIsLoadingRoadmap(true);
    fetch(apiUrl(`/api/guidance/schemes/${selectedScheme}`))
      .then((res) => {
        if (res.ok) return res.json();
        throw new Error('Failed to fetch roadmap');
      })
      .then((data) => {
        setRoadmapData(data);
      })
      .catch((err) => {
        console.error('Error fetching scheme roadmap:', err);
      })
      .finally(() => {
        setIsLoadingRoadmap(false);
      });
  }, [selectedScheme]);

  // Load Saved Checklist from localStorage for current scheme
  useEffect(() => {
    try {
      const saved = localStorage.getItem(`sevamitra_checklist_${selectedScheme}`);
      if (saved) {
        setCheckedDocs(JSON.parse(saved));
      } else {
        setCheckedDocs({});
      }
    } catch (e) {
      console.error('Error loading checklist:', e);
    }
  }, [selectedScheme]);

  // Toggle Checklist Item Checkbox
  const handleToggleDoc = (docIndex) => {
    const updated = { ...checkedDocs, [docIndex]: !checkedDocs[docIndex] };
    setCheckedDocs(updated);
    try {
      localStorage.setItem(`sevamitra_checklist_${selectedScheme}`, JSON.stringify(updated));
    } catch (e) {
      console.error('Error saving checklist:', e);
    }
  };

  // Fetch Tracker Status
  const handleTrackSubmit = async (refNum) => {
    const targetRef = refNum || refInput;
    if (!targetRef.trim()) return;

    setIsTracking(true);
    try {
      const res = await fetch(apiUrl(`/api/guidance/tracker/status?ref_number=${encodeURIComponent(targetRef)}`));
      if (!res.ok) throw new Error('Tracker fetch failed');
      const data = await res.json();
      setTrackerResult(data);
    } catch (err) {
      console.error('Error tracking status:', err);
    } finally {
      setIsTracking(false);
    }
  };

  // Calculate Checklist Completion Rate
  const totalDocs = (
    roadmapData?.[`required_documents_${currentLanguage}`] ||
    roadmapData?.required_documents_en ||
    []
  );
  
  const checkedCount = Object.values(checkedDocs).filter(Boolean).length;
  const completionPercentage = totalDocs.length > 0
    ? Math.round((checkedCount / totalDocs.length) * 100)
    : 0;

  return (
    <div className="application-guide-container" style={{ maxWidth: '900px', margin: '0 auto' }}>
      {/* Header Banner */}
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <span className="badge-official">
          🗺️ {t('guide.badge')}
        </span>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#1e3a8a', marginTop: '6px' }}>
          {t('guide.title')}
        </h2>
        <p style={{ color: '#64748b', fontSize: '0.95rem', marginTop: '4px' }}>
          {t('guide.description')}
        </p>
      </div>

      {/* Sub-Tab Navigation Bar */}
      <div style={{
        display: 'flex',
        justify: 'center',
        gap: '0.5rem',
        marginBottom: '1.75rem',
        background: '#ffffff',
        padding: '0.5rem',
        borderRadius: '9999px',
        border: '1.5px solid #cbd5e1',
        boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
        flexWrap: 'wrap'
      }}>
        <button
          type="button"
          onClick={() => setActiveSubTab('roadmap')}
          style={{
            background: activeSubTab === 'roadmap' ? '#2563eb' : 'transparent',
            color: activeSubTab === 'roadmap' ? '#ffffff' : '#475569',
            fontWeight: 700,
            padding: '0.6rem 1.25rem',
            borderRadius: '9999px',
            border: 'none',
            cursor: 'pointer',
            fontSize: '0.9rem',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <BookOpen size={16} />
          <span>{t('guide.tab_roadmap')}</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveSubTab('checklist')}
          style={{
            background: activeSubTab === 'checklist' ? '#166534' : 'transparent',
            color: activeSubTab === 'checklist' ? '#ffffff' : '#475569',
            fontWeight: 700,
            padding: '0.6rem 1.25rem',
            borderRadius: '9999px',
            border: 'none',
            cursor: 'pointer',
            fontSize: '0.9rem',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <CheckSquare size={16} />
          <span>{t('guide.tab_checklist')}</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveSubTab('tracker')}
          style={{
            background: activeSubTab === 'tracker' ? '#0284c7' : 'transparent',
            color: activeSubTab === 'tracker' ? '#ffffff' : '#475569',
            fontWeight: 700,
            padding: '0.6rem 1.25rem',
            borderRadius: '9999px',
            border: 'none',
            cursor: 'pointer',
            fontSize: '0.9rem',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <Search size={16} />
          <span>{t('guide.tab_tracker')}</span>
        </button>
      </div>

      {/* Target Scheme Selector Dropdown */}
      <div style={{
        background: '#ffffff',
        borderRadius: '16px',
        border: '1.5px solid #cbd5e1',
        padding: '1.25rem 1.5rem',
        marginBottom: '1.75rem',
        boxShadow: '0 2px 8px rgba(0,0,0,0.04)'
      }}>
        <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
          🏛️ {t('guide.select_scheme')}
        </label>
        <select
          value={selectedScheme}
          onChange={(e) => setSelectedScheme(e.target.value)}
          style={{
            width: '100%',
            padding: '0.85rem 1rem',
            borderRadius: '12px',
            border: '2px solid #cbd5e1',
            background: '#f8fafc',
            fontWeight: 700,
            color: '#1e293b',
            fontSize: '0.95rem'
          }}
        >
          <option value="old_age_pension">
            {t('schemes.old_age_pension')}
          </option>
          <option value="kalaignar_magalir_urimai">
            {t('schemes.kalaignar_magalir_urimai')}
          </option>
          <option value="pm_kisan">
            {t('schemes.pm_kisan')}
          </option>
        </select>
      </div>

      {/* SUB-TAB 1: ROADMAP */}
      {activeSubTab === 'roadmap' && (
        <div>
          {roadmapData && (
            <>
              {/* Voice Audio Narration Bar */}
              <div style={{ marginBottom: '1.5rem' }}>
                <AudioPlayer
                  text={getLocalized(roadmapData, 'voice_summary')}
                  autoPlay={false}
                />
              </div>

              {/* Step Cards List */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                {roadmapData.steps.map((step, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: '#ffffff',
                      borderRadius: '16px',
                      border: '1.5px solid #e2e8f0',
                      padding: '1.5rem',
                      boxShadow: '0 4px 12px rgba(0,0,0,0.04)',
                      position: 'relative'
                    }}
                  >
                    {/* Step Badge & Title */}
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.85rem', marginBottom: '0.75rem' }}>
                      <span style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '36px',
                        height: '36px',
                        borderRadius: '50%',
                        background: '#2563eb',
                        color: '#ffffff',
                        fontWeight: 800,
                        fontSize: '1rem',
                        flexShrink: 0
                      }}>
                        {step.step_number}
                      </span>

                      <div>
                        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#2563eb', textTransform: 'uppercase' }}>
                          {t('guide.step_label')} {step.step_number}
                        </span>
                        <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#1e293b', marginTop: '2px' }}>
                          {getLocalized(step, 'title')}
                        </h3>
                      </div>
                    </div>

                    {/* Step Description */}
                    <p style={{ fontSize: '0.975rem', color: '#334155', lineHeight: 1.6, marginBottom: '1rem' }}>
                      {getLocalized(step, 'description')}
                    </p>

                    {/* Meta Metadata (Authority & Time) */}
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', fontSize: '0.85rem', marginBottom: '0.75rem' }}>
                      <span style={{ background: '#f1f5f9', color: '#475569', padding: '0.35rem 0.75rem', borderRadius: '8px', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                        <UserCheck size={15} color="#2563eb" />
                        <span>{t('guide.authority_label')} <strong>{getLocalized(step, 'authority')}</strong></span>
                      </span>

                      <span style={{ background: '#eff6ff', color: '#1d4ed8', padding: '0.35rem 0.75rem', borderRadius: '8px', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                        <Clock size={15} />
                        <span>{t('guide.time_label')} <strong>{step.estimated_days}</strong></span>
                      </span>
                    </div>

                    {/* Pitfall / Caution Box */}
                    {(step.pitfalls_en || step.pitfalls_ta || step[`pitfalls_${currentLanguage}`]) && (
                      <div style={{
                        background: '#fffbeb',
                        borderRadius: '10px',
                        border: '1px solid #fde68a',
                        padding: '0.75rem 1rem',
                        fontSize: '0.85rem',
                        color: '#92400e',
                        marginTop: '0.75rem'
                      }}>
                        <div style={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '2px' }}>
                          <AlertTriangle size={15} color="#d97706" />
                          <span>{t('guide.pitfall_label')}</span>
                        </div>
                        <p style={{ margin: 0 }}>
                          {getLocalized(step, 'pitfalls')}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {/* SUB-TAB 2: MY SAVED CHECKLIST */}
      {activeSubTab === 'checklist' && (
        <div style={{
          background: '#ffffff',
          borderRadius: '16px',
          border: '1.5px solid #cbd5e1',
          padding: '1.75rem',
          boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
        }}>
          {/* Progress Gauge Bar */}
          <div style={{ marginBottom: '1.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <span style={{ fontWeight: 800, color: '#166534', fontSize: '1.05rem' }}>
                {t('guide.checklist_progress')}
              </span>
              <span style={{ fontWeight: 800, color: '#15803d', fontSize: '1.05rem' }}>
                {checkedCount} / {totalDocs.length} {t('guide.checklist_ready_count')} ({completionPercentage}%)
              </span>
            </div>

            {/* Horizontal Progress Meter */}
            <div style={{ height: '14px', width: '100%', background: '#e2e8f0', borderRadius: '9999px', overflow: 'hidden' }}>
              <div style={{
                height: '100%',
                width: `${completionPercentage}%`,
                background: completionPercentage === 100 ? '#16a34a' : '#2563eb',
                transition: 'width 0.4s ease'
              }} />
            </div>
          </div>

          {/* Document Checkbox Items */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', marginBottom: '1.5rem' }}>
            {totalDocs.map((docItem, idx) => {
              const isChecked = !!checkedDocs[idx];
              return (
                <label
                  key={idx}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.85rem',
                    padding: '1rem 1.25rem',
                    borderRadius: '12px',
                    border: `2px solid ${isChecked ? '#86efac' : '#e2e8f0'}`,
                    background: isChecked ? '#f0fdf4' : '#f8fafc',
                    cursor: 'pointer',
                    userSelect: 'none',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() => handleToggleDoc(idx)}
                    style={{ width: '22px', height: '22px', cursor: 'pointer', accentColor: '#16a34a' }}
                  />
                  <span style={{
                    fontSize: '1rem',
                    fontWeight: 600,
                    color: isChecked ? '#14532d' : '#334155',
                    textDecoration: isChecked ? 'line-through' : 'none'
                  }}>
                    {docItem}
                  </span>
                </label>
              );
            })}
          </div>

          {/* Persistence Note & Reset Button */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem', paddingTop: '1rem', borderTop: '1px solid #f1f5f9', fontSize: '0.825rem', color: '#64748b' }}>
            <span>💾 {t('guide.checklist_note')}</span>

            <button
              type="button"
              onClick={() => { setCheckedDocs({}); localStorage.removeItem(`sevamitra_checklist_${selectedScheme}`); }}
              style={{
                background: 'none',
                border: 'none',
                color: '#ef4444',
                fontWeight: 700,
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px'
              }}
            >
              <RefreshCw size={14} />
              <span>{t('guide.reset_checklist')}</span>
            </button>
          </div>
        </div>
      )}

      {/* SUB-TAB 3: APPLICATION STATUS TRACKER */}
      {activeSubTab === 'tracker' && (
        <div>
          {/* Reference Input & Demo Buttons Card */}
          <div style={{
            background: '#ffffff',
            borderRadius: '16px',
            border: '1.5px solid #cbd5e1',
            padding: '1.75rem',
            marginBottom: '1.75rem',
            boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
          }}>
            <form onSubmit={(e) => { e.preventDefault(); handleTrackSubmit(); }} style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
                {t('guide.tracker_input_label')}
              </label>

              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <input
                  type="text"
                  value={refInput}
                  onChange={(e) => setRefInput(e.target.value)}
                  placeholder={t('guide.tracker_placeholder')}
                  style={{
                    flex: 1,
                    padding: '0.85rem 1rem',
                    borderRadius: '12px',
                    border: '2px solid #cbd5e1',
                    fontSize: '0.95rem',
                    fontWeight: 600
                  }}
                />
                <button
                  type="submit"
                  disabled={isTracking}
                  style={{
                    background: '#0284c7',
                    color: '#ffffff',
                    fontWeight: 700,
                    padding: '0.85rem 1.5rem',
                    borderRadius: '12px',
                    border: 'none',
                    cursor: 'pointer'
                  }}
                >
                  {t('guide.tracker_btn')}
                </button>
              </div>
            </form>

            {/* 1-Click Demo References */}
            <div>
              <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#64748b', marginBottom: '0.5rem' }}>
                {t('guide.demo_references_label')}
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                <button
                  type="button"
                  onClick={() => { setRefInput('TN-OAP-2026-8941029'); handleTrackSubmit('TN-OAP-2026-8941029'); }}
                  style={{
                    background: '#f0fdf4',
                    color: '#15803d',
                    border: '1.5px solid #86efac',
                    padding: '0.4rem 0.85rem',
                    borderRadius: '9999px',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  {t('guide.demo_approved')}
                </button>

                <button
                  type="button"
                  onClick={() => { setRefInput('TN-KMUT-2026-5510293'); handleTrackSubmit('TN-KMUT-2026-5510293'); }}
                  style={{
                    background: '#fefce8',
                    color: '#b45309',
                    border: '1.5px solid #fde68a',
                    padding: '0.4rem 0.85rem',
                    borderRadius: '9999px',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  {t('guide.demo_review')}
                </button>
              </div>
            </div>
          </div>

          {/* Tracker Results */}
          {trackerResult && (
            <div style={{
              background: '#ffffff',
              borderRadius: '16px',
              border: '2px solid #38bdf8',
              padding: '1.75rem',
              boxShadow: '0 4px 12px rgba(2, 132, 199, 0.08)'
            }}>
              {/* Header Info */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
                <div>
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#0284c7', textTransform: 'uppercase' }}>
                    {getLocalized(trackerResult, 'scheme_name')}
                  </span>
                  <h3 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#0f172a', marginTop: '2px' }}>
                    {t('guide.reference_label')} {trackerResult.reference_number}
                  </h3>
                  <p style={{ fontSize: '0.875rem', color: '#64748b', marginTop: '2px' }}>
                    {t('guide.applicant_label')} <strong>{trackerResult.applicant_name}</strong> • {t('guide.submitted_label')} {trackerResult.submission_date}
                  </p>
                </div>

                <div style={{
                  background: trackerResult.current_status === 'approved' ? '#dcfce7' : '#fef3c7',
                  color: trackerResult.current_status === 'approved' ? '#15803d' : '#b45309',
                  padding: '0.4rem 0.85rem',
                  borderRadius: '9999px',
                  fontWeight: 800,
                  fontSize: '0.875rem',
                  border: `1.5px solid ${trackerResult.current_status === 'approved' ? '#86efac' : '#fde68a'}`
                }}>
                  {trackerResult.current_status === 'approved'
                    ? t('guide.status_approved')
                    : t('guide.status_review')}
                </div>
              </div>

              {/* Audio Narration */}
              <div style={{ marginBottom: '1.5rem' }}>
                <AudioPlayer
                  text={getLocalized(trackerResult, 'voice_summary')}
                  autoPlay={true}
                />
              </div>

              {/* Timeline Stages */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1.5rem' }}>
                {trackerResult.stages.map((stg, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      gap: '1rem',
                      background: stg.status === 'completed' ? '#f0fdf4' : stg.status === 'current' ? '#f0f9ff' : '#f8fafc',
                      padding: '1rem 1.25rem',
                      borderRadius: '12px',
                      border: `1.5px solid ${stg.status === 'completed' ? '#bbf7d0' : stg.status === 'current' ? '#bae6fd' : '#e2e8f0'}`
                    }}
                  >
                    <div style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '50%',
                      background: stg.status === 'completed' ? '#16a34a' : stg.status === 'current' ? '#0284c7' : '#94a3b8',
                      color: '#ffffff',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 800,
                      fontSize: '0.9rem',
                      flexShrink: 0
                    }}>
                      {stg.status === 'completed' ? '✓' : stg.stage_number}
                    </div>

                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap' }}>
                        <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#1e293b', margin: 0 }}>
                          {getLocalized(stg, 'title')}
                        </h4>
                        <span style={{ fontSize: '0.775rem', fontWeight: 600, color: '#64748b' }}>
                          📅 {stg.date}
                        </span>
                      </div>

                      <p style={{ fontSize: '0.85rem', color: '#475569', marginTop: '4px', margin: 0 }}>
                        💬 <strong>{t('guide.officer_note_label')}</strong> {getLocalized(stg, 'officer_note')}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Transparent Disclaimer Box */}
              <div style={{ background: '#f8fafc', padding: '0.85rem', borderRadius: '10px', fontSize: '0.8rem', color: '#64748b', textAlign: 'center', border: '1px solid #e2e8f0' }}>
                ℹ️ <strong>{t('guide.disclaimer_title')}</strong> {getLocalized(trackerResult, 'disclaimer')}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Back to Home Button */}
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
          ← {t('guide.back_to_home')}
        </button>
      </div>
    </div>
  );
};

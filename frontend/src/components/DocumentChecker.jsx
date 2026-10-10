import React, { useState } from 'react';
import { Upload, FileCheck, AlertCircle, CheckCircle, Eye, ShieldAlert, Loader2, RotateCcw, Lightbulb, ArrowRight, FileText } from 'lucide-react';
import { useTranslation } from '../i18n';
import { AudioPlayer } from './AudioPlayer';

export const DocumentChecker = ({ onBackToHome, onGoToGuide }) => {
  const { currentLanguage, t } = useTranslation();
  const isTamil = currentLanguage === 'ta';

  const [selectedScheme, setSelectedScheme] = useState('old_age_pension');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [activeSampleId, setActiveSampleId] = useState(null);
  const [report, setReport] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setSelectedFile(file);
    setActiveSampleId(null);
    setReport(null);

    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = () => setPreviewUrl(reader.result);
      reader.readAsDataURL(file);
    } else {
      setPreviewUrl(null);
    }
  };

  const executeCheck = async (fileObj, sampleId) => {
    setIsScanning(true);
    const formData = new FormData();
    
    if (fileObj) {
      formData.append('file', fileObj);
    }
    if (sampleId) {
      formData.append('sample_id', sampleId);
    }
    formData.append('scheme_id', selectedScheme);
    formData.append('language', currentLanguage);

    try {
      const res = await fetch('/api/documents/check', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) throw new Error('Document scan failed');
      const data = await res.json();
      setReport(data);
    } catch (err) {
      console.error('Error checking document readiness:', err);
    } finally {
      setIsScanning(false);
    }
  };

  const handleScanSubmit = (e) => {
    e.preventDefault();
    if (!selectedFile && !activeSampleId) return;
    executeCheck(selectedFile, activeSampleId);
  };

  const handleSampleClick = (sampleId, targetScheme) => {
    setActiveSampleId(sampleId);
    setSelectedFile(null);
    setPreviewUrl(null);
    if (targetScheme) {
      setSelectedScheme(targetScheme);
    }
    executeCheck(null, sampleId);
  };

  return (
    <div className="doc-checker-container" style={{ maxWidth: '850px', margin: '0 auto' }}>
      {/* Header Banner */}
      <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
        <span className="badge-official">
          📄 {t('doc_checker.badge')}
        </span>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#1e3a8a', marginTop: '6px' }}>
          {t('doc_checker.title')}
        </h2>
        <p style={{ color: '#64748b', fontSize: '0.95rem', marginTop: '4px' }}>
          {t('doc_checker.description')}
        </p>
      </div>

      {!report ? (
        /* Upload Form & Sample Testers */
        <form onSubmit={handleScanSubmit} style={{
          background: '#ffffff',
          borderRadius: '16px',
          border: '1.5px solid #cbd5e1',
          padding: '1.75rem',
          boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
        }}>
          {/* 1-Click Sample Test Bar */}
          <div style={{
            background: '#f0f9ff',
            borderRadius: '14px',
            border: '1.5px solid #bae6fd',
            padding: '1.25rem',
            marginBottom: '1.75rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 700, color: '#0369a1', fontSize: '0.95rem', marginBottom: '0.75rem' }}>
              <FileText size={18} />
              <span>{t('doc_checker.samples_label')}</span>
            </div>
            
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              <button
                type="button"
                onClick={() => handleSampleClick('sample_valid_oap', 'old_age_pension')}
                style={{
                  background: activeSampleId === 'sample_valid_oap' ? '#2563eb' : '#ffffff',
                  color: activeSampleId === 'sample_valid_oap' ? '#ffffff' : '#1e40af',
                  border: '1.5px solid #93c5fd',
                  padding: '0.5rem 0.85rem',
                  borderRadius: '9999px',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                {t('doc_checker.sample_valid_oap')}
              </button>

              <button
                type="button"
                onClick={() => handleSampleClick('sample_incomplete', 'old_age_pension')}
                style={{
                  background: activeSampleId === 'sample_incomplete' ? '#d97706' : '#ffffff',
                  color: activeSampleId === 'sample_incomplete' ? '#ffffff' : '#b45309',
                  border: '1.5px solid #fde68a',
                  padding: '0.5rem 0.85rem',
                  borderRadius: '9999px',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                {t('doc_checker.sample_incomplete')}
              </button>

              <button
                type="button"
                onClick={() => handleSampleClick('sample_pm_kisan', 'pm_kisan')}
                style={{
                  background: activeSampleId === 'sample_pm_kisan' ? '#166534' : '#ffffff',
                  color: activeSampleId === 'sample_pm_kisan' ? '#ffffff' : '#15803d',
                  border: '1.5px solid #86efac',
                  padding: '0.5rem 0.85rem',
                  borderRadius: '9999px',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                {t('doc_checker.sample_pm_kisan')}
              </button>

              <button
                type="button"
                onClick={() => handleSampleClick('sample_kmut', 'kalaignar_magalir_urimai')}
                style={{
                  background: activeSampleId === 'sample_kmut' ? '#be185d' : '#ffffff',
                  color: activeSampleId === 'sample_kmut' ? '#ffffff' : '#9d174d',
                  border: '1.5px solid #fbcfe8',
                  padding: '0.5rem 0.85rem',
                  borderRadius: '9999px',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                {t('doc_checker.sample_kmut')}
              </button>
            </div>
          </div>

          {/* Scheme Selection */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
              {t('doc_checker.select_scheme')}
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
                fontWeight: 600,
                color: '#1e293b'
              }}
            >
              <option value="old_age_pension">
                {isTamil ? 'முதியோர் ஓய்வூதியத் திட்டம் (OAP)' : 'Indira Gandhi Old Age Pension Scheme (IGNOAPS)'}
              </option>
              <option value="kalaignar_magalir_urimai">
                {isTamil ? 'கலைஞர் மகளிர் உரிமைத் திட்டம் (KMUT)' : 'Kalaignar Magalir Urimai Thogai Scheme'}
              </option>
              <option value="pm_kisan">
                {isTamil ? 'பிரதம மந்திரி கிசான் சம்மான் நிதி (PM-KISAN)' : 'PM-KISAN Farmer Scheme'}
              </option>
              <option value="cmchis_health">
                {isTamil ? 'முதலமைச்சரின் விரிவான மருத்துவக் காப்பீடு (CMCHIS)' : 'CMCHIS Health Insurance Scheme'}
              </option>
            </select>
          </div>

          {/* Drag & Drop File Upload Box */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontWeight: 700, color: '#1e293b', marginBottom: '0.5rem' }}>
              {t('doc_checker.upload_label')}
            </label>
            
            <div style={{
              border: '2.5px dashed #93c5fd',
              borderRadius: '16px',
              padding: '2rem 1.5rem',
              textAlign: 'center',
              background: selectedFile ? '#f0fdf4' : '#f8fafc',
              cursor: 'pointer',
              position: 'relative'
            }}>
              <input
                type="file"
                accept="image/*,application/pdf"
                onChange={handleFileChange}
                style={{
                  position: 'absolute',
                  inset: 0,
                  opacity: 0,
                  cursor: 'pointer',
                  width: '100%',
                  height: '100%'
                }}
              />

              <div style={{ display: 'inline-flex', padding: '12px', background: '#dcfce7', borderRadius: '50%', color: '#15803d', marginBottom: '0.75rem' }}>
                <Upload size={32} />
              </div>

              {selectedFile ? (
                <div>
                  <p style={{ fontWeight: 700, color: '#166534', fontSize: '1.05rem' }}>
                    📄 {selectedFile.name}
                  </p>
                  <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '2px' }}>
                    {(selectedFile.size / 1024).toFixed(1)} KB • {isTamil ? 'மாற்ற கிளிக் செய்யவும்' : 'Click to change file'}
                  </p>

                  {previewUrl && (
                    <div style={{ marginTop: '1rem' }}>
                      <img
                        src={previewUrl}
                        alt="Document preview"
                        style={{ maxHeight: '140px', borderRadius: '8px', border: '1px solid #cbd5e1', boxShadow: '0 2px 6px rgba(0,0,0,0.1)' }}
                      />
                    </div>
                  )}
                </div>
              ) : (
                <div>
                  <p style={{ fontWeight: 700, color: '#1e3a8a', fontSize: '1.05rem' }}>
                    {t('doc_checker.upload_drop_text')}
                  </p>
                  <p style={{ fontSize: '0.825rem', color: '#64748b', marginTop: '4px' }}>
                    {t('doc_checker.upload_formats')}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Citizen Scanning Guidelines */}
          <div style={{
            background: '#fffbeb',
            borderRadius: '12px',
            border: '1px solid #fde68a',
            padding: '1rem',
            marginBottom: '1.5rem',
            fontSize: '0.85rem',
            color: '#78350f'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 700, marginBottom: '0.4rem' }}>
              <Lightbulb size={18} color="#d97706" />
              <span>{t('doc_checker.tips_title')}</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', margin: 0 }}>
              <li>{t('doc_checker.tip_light')}</li>
              <li>{t('doc_checker.tip_seal')}</li>
              <li>{t('doc_checker.tip_flat')}</li>
            </ul>
          </div>

          {/* Privacy Note */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: '#64748b', marginBottom: '1.5rem', background: '#f8fafc', padding: '0.65rem 0.85rem', borderRadius: '8px' }}>
            <ShieldAlert size={16} color="#0284c7" />
            <span>{t('doc_checker.privacy_note')}</span>
          </div>

          {/* Scan CTA Button */}
          <button
            type="submit"
            disabled={(!selectedFile && !activeSampleId) || isScanning}
            className="speak-cta-btn"
            style={{
              width: '100%',
              padding: '1rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.75rem',
              opacity: (!selectedFile && !activeSampleId) ? 0.6 : 1
            }}
          >
            {isScanning ? <Loader2 style={{ animation: 'spin 1s linear infinite' }} size={22} /> : <FileCheck size={22} />}
            <span>
              {isScanning ? t('doc_checker.scanning_btn') : t('doc_checker.scan_btn')}
            </span>
          </button>
        </form>
      ) : (
        /* Report Results View */
        <div>
          <div style={{
            background: '#ffffff',
            border: `2px solid ${report.is_ready ? '#86efac' : '#fde68a'}`,
            borderRadius: '16px',
            padding: '1.75rem',
            marginBottom: '1.5rem',
            boxShadow: '0 4px 12px rgba(0,0,0,0.06)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.75rem' }}>
              <div>
                <span style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, textTransform: 'uppercase' }}>
                  {t('doc_checker.score_label')}
                </span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '2px' }}>
                  <span style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '56px',
                    height: '56px',
                    borderRadius: '50%',
                    background: report.is_ready ? '#dcfce7' : '#fef3c7',
                    color: report.is_ready ? '#15803d' : '#b45309',
                    fontSize: '1.25rem',
                    fontWeight: 800,
                    border: `3px solid ${report.is_ready ? '#22c55e' : '#f59e0b'}`
                  }}>
                    {report.readiness_score}%
                  </span>
                  <div>
                    <h3 style={{ fontSize: '1.35rem', fontWeight: 800, color: report.is_ready ? '#15803d' : '#b45309' }}>
                      {report.is_ready ? t('doc_checker.status_ready') : t('doc_checker.status_action_needed')}
                    </h3>
                  </div>
                </div>
              </div>

              <button
                type="button"
                onClick={() => { setReport(null); setSelectedFile(null); setActiveSampleId(null); }}
                style={{
                  background: '#f1f5f9',
                  border: '1px solid #cbd5e1',
                  borderRadius: '9999px',
                  padding: '0.5rem 1rem',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  color: '#334155',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  cursor: 'pointer'
                }}
              >
                <RotateCcw size={16} />
                <span>{t('doc_checker.check_another')}</span>
              </button>
            </div>

            {/* Read-Aloud Voice Audio Player */}
            <AudioPlayer text={report.voice_summary} autoPlay={true} />

            {/* Identified Elements Checklist */}
            {report.identified_items && report.identified_items.length > 0 && (
              <div style={{ marginTop: '1.5rem', marginBottom: '1.25rem' }}>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#166534', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.5rem' }}>
                  <CheckCircle size={18} />
                  <span>{t('doc_checker.detected_title')}</span>
                </h4>
                <ul style={{ listStyle: 'none', paddingLeft: '1.25rem', fontSize: '0.925rem', color: '#1e293b' }}>
                  {report.identified_items.map((item, idx) => (
                    <li key={idx} style={{ marginBottom: '6px', position: 'relative' }}>
                      <span style={{ position: 'absolute', left: '-1.1rem', color: '#16a34a', fontWeight: 'bold' }}>✔</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Missing Elements Checklist */}
            {report.missing_items && report.missing_items.length > 0 && (
              <div style={{ marginBottom: '1.25rem' }}>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#b45309', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.5rem' }}>
                  <AlertCircle size={18} />
                  <span>{t('doc_checker.missing_title')}</span>
                </h4>
                <ul style={{ listStyle: 'none', paddingLeft: '1.25rem', fontSize: '0.925rem', color: '#475569' }}>
                  {report.missing_items.map((item, idx) => (
                    <li key={idx} style={{ marginBottom: '6px', position: 'relative' }}>
                      <span style={{ position: 'absolute', left: '-1.1rem', color: '#f59e0b', fontWeight: 'bold' }}>⚠</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Extracted Text Preview */}
            <div style={{ marginTop: '1.25rem', background: '#f8fafc', padding: '1rem', borderRadius: '12px', border: '1px dashed #cbd5e1' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.825rem', fontWeight: 700, color: '#475569', marginBottom: '0.5rem' }}>
                <Eye size={15} />
                <span>{t('doc_checker.ocr_preview_title')}</span>
              </div>
              <p style={{ fontFamily: 'monospace', fontSize: '0.825rem', color: '#334155', whiteSpace: 'pre-wrap', maxHeight: '130px', overflowY: 'auto', margin: 0 }}>
                {report.extracted_text_preview}
              </p>
            </div>

            {/* Recommended Next Step Callout */}
            <div style={{
              marginTop: '1.25rem',
              background: report.is_ready ? '#f0fdf4' : '#fffbeb',
              padding: '1rem',
              borderRadius: '12px',
              border: `1px solid ${report.is_ready ? '#bbf7d0' : '#fef08a'}`
            }}>
              <div style={{ fontWeight: 700, color: report.is_ready ? '#166534' : '#854d0e', marginBottom: '4px', fontSize: '0.9rem' }}>
                📌 {t('doc_checker.next_steps_title')}
              </div>
              <p style={{ fontSize: '0.875rem', color: report.is_ready ? '#14532d' : '#713f12', margin: 0 }}>
                {report.is_ready ? t('doc_checker.next_step_ready') : t('doc_checker.next_step_action')}
              </p>
            </div>

            {/* Advisory Disclaimer */}
            <div style={{ marginTop: '1.25rem', paddingTop: '0.85rem', borderTop: '1px solid #f1f5f9', fontSize: '0.8rem', color: '#64748b', textAlign: 'center' }}>
              <p style={{ margin: 0 }}>
                ℹ️ <strong>{t('doc_checker.disclaimer_title')}</strong> {report.disclaimer}
              </p>
            </div>
          </div>

          {/* Navigation Action Footer */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap', marginTop: '1.5rem' }}>
            <button
              type="button"
              onClick={onBackToHome}
              style={{
                background: '#ffffff',
                border: '1.5px solid #cbd5e1',
                color: '#475569',
                fontWeight: 700,
                padding: '0.75rem 1.25rem',
                borderRadius: '12px',
                cursor: 'pointer',
                fontSize: '0.9rem'
              }}
            >
              ← {t('doc_checker.back_home')}
            </button>

            {onGoToGuide && (
              <button
                type="button"
                onClick={onGoToGuide}
                style={{
                  background: '#2563eb',
                  border: 'none',
                  color: '#ffffff',
                  fontWeight: 700,
                  padding: '0.75rem 1.25rem',
                  borderRadius: '12px',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px'
                }}
              >
                <span>{t('doc_checker.go_to_guide')}</span>
                <ArrowRight size={16} />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

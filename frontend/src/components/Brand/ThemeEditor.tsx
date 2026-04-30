import React, { useState } from 'react';
import { useBranding } from './BrandProvider';

export function ThemeEditor() {
  const { branding } = useBranding();
  const [primaryColor, setPrimaryColor] = useState(branding.primary_color);
  const [secondaryColor, setSecondaryColor] = useState(branding.secondary_color);
  const [platformName, setPlatformName] = useState(branding.platform_name);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/branding/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token,
        },
        body: JSON.stringify({
          primary_color: primaryColor,
          secondary_color: secondaryColor,
          platform_name: platformName,
        }),
      });

      if (response.ok) {
        alert('Theme saved successfully!');
        window.location.reload();
      } else {
        alert('Failed to save theme');
      }
    } catch (error) {
      console.error('Failed to save theme:', error);
      alert('Failed to save theme');
    } finally {
      setSaving(false);
    }
  };

  const handleLogoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/branding/logo', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
        },
        body: formData,
      });

      if (response.ok) {
        alert('Logo uploaded successfully!');
        window.location.reload();
      }
    } catch (error) {
      console.error('Failed to upload logo:', error);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Theme Settings</h2>

      <div style={styles.field}>
        <label style={styles.label}>Platform Name</label>
        <input
          type='text'
          value={platformName}
          onChange={(e) => setPlatformName(e.target.value)}
          style={styles.input}
        />
      </div>

      <div style={styles.field}>
        <label style={styles.label}>Primary Color</label>
        <input
          type='color'
          value={primaryColor}
          onChange={(e) => setPrimaryColor(e.target.value)}
          style={styles.colorInput}
        />
        <span style={styles.colorValue}>{primaryColor}</span>
      </div>

      <div style={styles.field}>
        <label style={styles.label}>Secondary Color</label>
        <input
          type='color'
          value={secondaryColor}
          onChange={(e) => setSecondaryColor(e.target.value)}
          style={styles.colorInput}
        />
        <span style={styles.colorValue}>{secondaryColor}</span>
      </div>

      <div style={styles.field}>
        <label style={styles.label}>Logo</label>
        <input
          type='file'
          accept='image/*'
          onChange={handleLogoUpload}
        />
        {branding.logo_url && (
          <img src={branding.logo_url} alt='Logo' style={styles.preview} />
        )}
      </div>

      <button onClick={handleSave} disabled={saving} style={styles.button}>
        {saving ? 'Saving...' : 'Save Theme'}
      </button>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { padding: '1rem', maxWidth: '500px' },
  field: { marginBottom: '1rem' },
  label: { display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' },
  input: { width: '100%', padding: '0.5rem', fontSize: '1rem' },
  colorInput: { width: '50px', height: '30px', cursor: 'pointer' },
  colorValue: { marginLeft: '0.5rem' },
  preview: { maxWidth: '200px', marginTop: '0.5rem' },
  button: {
    padding: '0.75rem 1.5rem',
    backgroundColor: 'var(--primary-color, #1976d2)',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
};

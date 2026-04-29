/**
 * Accessibility Context Provider
 * Manages accessibility preferences including:
 * - High contrast mode
 * - Reduced motion
 * - Screen reader announcements
 */
import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

interface AccessibilitySettings {
  highContrast: boolean;
  reducedMotion: boolean;
  colorBlindMode: 'none' | 'protanopia' | 'deuteranopia' | 'tritanopia';
  fontSize: 'normal' | 'large' | 'xlarge';
}

interface AccessibilityContextType {
  settings: AccessibilitySettings;
  setHighContrast: (enabled: boolean) => void;
  setReducedMotion: (enabled: boolean) => void;
  setColorBlindMode: (mode: AccessibilitySettings['colorBlindMode']) => void;
  setFontSize: (size: AccessibilitySettings['fontSize']) => void;
  announce: (message: string, priority?: 'polite' | 'assertive') => void;
}

const defaultSettings: AccessibilitySettings = {
  highContrast: false,
  reducedMotion: false,
  colorBlindMode: 'none',
  fontSize: 'normal',
};

const AccessibilityContext = createContext<AccessibilityContextType | null>(null);

export function AccessibilityProvider({ children }: { children: ReactNode }) {
  const { t } = useTranslation();
  const [settings, setSettings] = useState<AccessibilitySettings>(() => {
    const stored = localStorage.getItem('a11y-settings');
    if (stored) {
      try {
        return { ...defaultSettings, ...JSON.parse(stored) };
      } catch {
        return defaultSettings;
      }
    }
    // Check system preferences
    return {
      ...defaultSettings,
      reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      highContrast: window.matchMedia('(prefers-contrast: more)').matches,
    };
  });

  const [announcement, setAnnouncement] = useState<{ message: string; priority: 'polite' | 'assertive' } | null>(null);

  // Apply settings to document
  useEffect(() => {
    const root = document.documentElement;

    // High contrast
    root.classList.toggle('high-contrast', settings.highContrast);

    // Reduced motion
    root.classList.toggle('reduced-motion', settings.reducedMotion);

    // Color blind mode
    root.classList.remove('colorblind-protanopia', 'colorblind-deuteranopia', 'colorblind-tritanopia');
    if (settings.colorBlindMode !== 'none') {
      root.classList.add(`colorblind-${settings.colorBlindMode}`);
    }

    // Font size
    root.classList.remove('font-large', 'font-xlarge');
    if (settings.fontSize === 'large') {
      root.classList.add('font-large');
    } else if (settings.fontSize === 'xlarge') {
      root.classList.add('font-xlarge');
    }

    // Persist settings
    localStorage.setItem('a11y-settings', JSON.stringify(settings));
  }, [settings]);

  // Listen for system preference changes
  useEffect(() => {
    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const contrastQuery = window.matchMedia('(prefers-contrast: more)');

    const handleMotionChange = (e: MediaQueryListEvent) => {
      setSettings(prev => ({ ...prev, reducedMotion: e.matches }));
    };
    const handleContrastChange = (e: MediaQueryListEvent) => {
      setSettings(prev => ({ ...prev, highContrast: e.matches }));
    };

    motionQuery.addEventListener('change', handleMotionChange);
    contrastQuery.addEventListener('change', handleContrastChange);

    return () => {
      motionQuery.removeEventListener('change', handleMotionChange);
      contrastQuery.removeEventListener('change', handleContrastChange);
    };
  }, []);

  const setHighContrast = useCallback((enabled: boolean) => {
    setSettings(prev => ({ ...prev, highContrast: enabled }));
  }, []);

  const setReducedMotion = useCallback((enabled: boolean) => {
    setSettings(prev => ({ ...prev, reducedMotion: enabled }));
  }, []);

  const setColorBlindMode = useCallback((mode: AccessibilitySettings['colorBlindMode']) => {
    setSettings(prev => ({ ...prev, colorBlindMode: mode }));
  }, []);

  const setFontSize = useCallback((size: AccessibilitySettings['fontSize']) => {
    setSettings(prev => ({ ...prev, fontSize: size }));
  }, []);

  const announce = useCallback((message: string, priority: 'polite' | 'assertive' = 'polite') => {
    setAnnouncement({ message, priority });
    // Clear announcement after it's been read
    setTimeout(() => setAnnouncement(null), 1000);
  }, []);

  return (
    <AccessibilityContext.Provider
      value={{
        settings,
        setHighContrast,
        setReducedMotion,
        setColorBlindMode,
        setFontSize,
        announce,
      }}
    >
      {children}
      {/* Live region for screen reader announcements */}
      <div
        role="status"
        aria-live={announcement?.priority || 'polite'}
        aria-atomic="true"
        className="sr-only"
      >
        {announcement?.message}
      </div>
    </AccessibilityContext.Provider>
  );
}

export function useAccessibility() {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within AccessibilityProvider');
  }
  return context;
}

// Export for testing
export { AccessibilityContext };

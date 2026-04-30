/**
 * Accessibility Settings Panel Component
 * Allows users to configure accessibility preferences
 */
import { useTranslation } from 'react-i18next';
import { useAccessibility } from './AccessibilityContext';
import './AccessibilityPanel.css';

interface AccessibilityPanelProps {
  onClose?: () => void;
}

export function AccessibilityPanel({ onClose }: AccessibilityPanelProps) {
  const { t } = useTranslation();
  const { settings, setHighContrast, setReducedMotion, setColorBlindMode, setFontSize } = useAccessibility();

  return (
    <div className="a11y-panel" role="dialog" aria-labelledby="a11y-panel-title">
      <h2 id="a11y-panel-title" className="a11y-panel-title">
        {t('accessibility.settings')}
      </h2>

      {onClose && (
        <button
          className="a11y-panel-close"
          onClick={onClose}
          aria-label={t('accessibility.closeSettings')}
        >
          <span aria-hidden="true">&times;</span>
        </button>
      )}

      <div className="a11y-option">
        <label htmlFor="high-contrast-toggle">
          <span className="a11y-label">{t('accessibility.highContrast')}</span>
          <span className="a11y-description">{t('accessibility.highContrastDesc')}</span>
        </label>
        <button
          id="high-contrast-toggle"
          role="switch"
          aria-checked={settings.highContrast}
          onClick={() => setHighContrast(!settings.highContrast)}
          className="a11y-toggle"
        >
          <span className="a11y-toggle-slider" />
        </button>
      </div>

      <div className="a11y-option">
        <label htmlFor="reduced-motion-toggle">
          <span className="a11y-label">{t('accessibility.reducedMotion')}</span>
          <span className="a11y-description">{t('accessibility.reducedMotionDesc')}</span>
        </label>
        <button
          id="reduced-motion-toggle"
          role="switch"
          aria-checked={settings.reducedMotion}
          onClick={() => setReducedMotion(!settings.reducedMotion)}
          className="a11y-toggle"
        >
          <span className="a11y-toggle-slider" />
        </button>
      </div>

      <div className="a11y-option">
        <label htmlFor="font-size-select">
          <span className="a11y-label">{t('accessibility.fontSize')}</span>
          <span className="a11y-description">{t('accessibility.fontSizeDesc')}</span>
        </label>
        <select
          id="font-size-select"
          value={settings.fontSize}
          onChange={(e) => setFontSize(e.target.value as typeof settings.fontSize)}
          className="a11y-select"
        >
          <option value="normal">{t('accessibility.fontSizeNormal')}</option>
          <option value="large">{t('accessibility.fontSizeLarge')}</option>
          <option value="xlarge">{t('accessibility.fontSizeXLarge')}</option>
        </select>
      </div>

      <div className="a11y-option">
        <label htmlFor="colorblind-select">
          <span className="a11y-label">{t('accessibility.colorBlind')}</span>
          <span className="a11y-description">{t('accessibility.colorBlindDesc')}</span>
        </label>
        <select
          id="colorblind-select"
          value={settings.colorBlindMode}
          onChange={(e) => setColorBlindMode(e.target.value as typeof settings.colorBlindMode)}
          className="a11y-select"
        >
          <option value="none">{t('accessibility.colorBlindNone')}</option>
          <option value="protanopia">{t('accessibility.colorBlindProtanopia')}</option>
          <option value="deuteranopia">{t('accessibility.colorBlindDeuteranopia')}</option>
          <option value="tritanopia">{t('accessibility.colorBlindTritanopia')}</option>
        </select>
      </div>

      <div className="a11y-shortcuts">
        <h3>{t('accessibility.keyboardShortcuts')}</h3>
        <ul>
          <li><kbd>Tab</kbd> {t('accessibility.shortcutTab')}</li>
          <li><kbd>Shift+Tab</kbd> {t('accessibility.shortcutShiftTab')}</li>
          <li><kbd>Enter</kbd> / <kbd>Space</kbd> {t('accessibility.shortcutActivate')}</li>
          <li><kbd>Escape</kbd> {t('accessibility.shortcutEscape')}</li>
        </ul>
      </div>
    </div>
  );
}

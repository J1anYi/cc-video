/**
 * SkipLinks component for keyboard navigation accessibility.
 * Allows users to skip directly to main content areas.
 */
import { useTranslation } from 'react-i18next';
import './SkipLinks.css';

export default function SkipLinks() {
  const { t } = useTranslation();

  return (
    <nav className="skip-links" aria-label={t('accessibility.skipNav')}>
      <a href="#main-content" className="skip-link">
        {t('accessibility.skipToContent')}
      </a>
      <a href="#main-navigation" className="skip-link">
        {t('accessibility.skipToNav')}
      </a>
      <a href="#search-input" className="skip-link">
        {t('accessibility.skipToSearch')}
      </a>
    </nav>
  );
}

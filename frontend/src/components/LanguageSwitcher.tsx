/**
 * Language Switcher Component
 * Allows users to change the UI language
 */
import { useTranslation } from 'react-i18next';
import { SUPPORTED_LANGUAGES } from '../i18n';

export function LanguageSwitcher() {
  const { i18n } = useTranslation();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newLang = e.target.value;
    i18n.changeLanguage(newLang);
    // Store preference
    localStorage.setItem('language', newLang);
    // Update HTML dir attribute for RTL support
    document.documentElement.dir = newLang === 'ar' || newLang === 'he' ? 'rtl' : 'ltr';
    document.documentElement.lang = newLang;
  };

  return (
    <select
      value={i18n.language}
      onChange={handleChange}
      className="language-switcher"
      aria-label="Select language"
    >
      {SUPPORTED_LANGUAGES.map((lang) => (
        <option key={lang.code} value={lang.code}>
          {lang.nativeName}
        </option>
      ))}
    </select>
  );
}

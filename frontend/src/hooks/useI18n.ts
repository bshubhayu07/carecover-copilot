import { useState, useEffect } from 'react';
import type { IndianLanguage, I18nDictionary } from '../types/i18n';

export function useI18n() {
  const [language, setLanguage] = useState<IndianLanguage>("English");
  const [dictionary, setDictionary] = useState<Partial<I18nDictionary>>({});
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch('/static/i18n.json')
      .then(res => res.json())
      .then((data: I18nDictionary) => {
        setDictionary(data);
        setLoading(false);
      })
      .catch(err => console.error("Failed to load i18n data", err));
  }, []);

  const t = (key: string): string => {
    if (!dictionary) return key;
    return dictionary[language]?.[key] || dictionary["English"]?.[key] || key;
  };

  return { language, setLanguage, t, loading };
}

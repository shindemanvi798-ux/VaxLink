import React, { createContext, useState, useContext, useEffect } from 'react';
import { translations } from './translations';

// Create the context
const LanguageContext = createContext();

// Create a custom hook for easy access
export const useLanguage = () => {
  return useContext(LanguageContext);
};

// Provider component that wraps the app
export const LanguageProvider = ({ children }) => {
  // Check local storage for saved language, default to Hindi ('hi') for rural India target
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('saathi_lang') || 'hi';
  });

  // Update local storage whenever language changes
  useEffect(() => {
    localStorage.setItem('saathi_lang', language);
    // Optional: Also update the HTML lang attribute for accessibility
    document.documentElement.lang = language;
  }, [language]);

  // The translation helper function
  const t = (key) => {
    // If the key exists in the current language, return it. 
    // Fallback to English if translation is missing.
    // Fallback to the raw key if it doesn't exist anywhere.
    return translations[language]?.[key] || translations['en']?.[key] || key;
  };

  const changeLanguage = (newLang) => {
    if (translations[newLang]) {
      setLanguage(newLang);
    }
  };

  return (
    <LanguageContext.Provider value={{ language, changeLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';

i18n
  .use(Backend)
  .use(initReactI18next)
  .init({
    // 1. Set the default language when the app loads
    fallbackLng: 'en',
    
    // 2. Add ALL your language folder codes here
    supportedLngs: ['en', 'hi', 'ml', 'mni', 'bn', 'brx', 'as'],

    // 3. Keep your basic page names (namespaces)
    ns: ['common', 'home'], 
    defaultNS: 'common',

    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json', 
    },

    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;

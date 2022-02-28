const de = {
  transport: "Logistik",
  transportDesc: "Biete/Suche Transportmöglichkeiten",
  donations: "Spenden",
  donationsDesc: "Finde Sammelstellen und Spendeninfos",
  legal: "Rechtsfragen",
  legalDesc: "Hilfe zu Rechtsfragen",
  housing: "Unterkünfte",
  housingDesc: "Biete/Suche Unterkünfte",
  translations: "Übersetzungen",
  translationsDesc: "Finde ÜbersetzerInnen",
  visitThisChannel: "Hier entlang bitte!:",
  welcomeMsg:
    "Hey! Wir versuchen, Hilfsangebote und - Anfragen zu koordinieren",
};
const en = {
  transport: "Logistics",
  transportDesc: "offer/search for transport",
  donations: "Donations",
  donationsDesc: "get help with donations",
  legal: "Legal Requests",
  legalDesc: "get help with legal questions",
  housing: "Accomodation",
  housingDesc: "offer/search for housing",
  translations: "Translations",
  translationsDesc: "get help from translators",
  visitThisChannel: "This way please!",
  welcomeMsg:
    "Hey! We are trying to coordinate offers of help and requests. Please choose a topic.",
};
const uk = {
  transport: "транспорт",
  transportDesc: "пропоную/шукаю опції пересування чи логістики",
  donations: "пожертвування",
  donationsDesc: "знайти місця для збору пожертв, чи інформацію про пожертви",
  legal: "правові питання",
  legalDesc: "допомога з правових питань",
  housing: "проживання",
  housingDesc: "пропоную/шукаю житло",
  translations: "переклади",
  translationsDesc: "знайти перекладачів",
  visitThisChannel: "ось сюди, будь ласка!",
  welcomeMsg:
    "привіт! ми намагаємося координувати пропозиції підтримки та запити. Будь ласка, оберіть тему.",
};

// available translations
const translations = {
  de,
  en,
  uk,
};

const getTranslation = (string, language) => {
  if (translations[language]) {
    if (translations[language][string]) {
      return translations[language][string];
    } else {
      console.log(
        `Translation not found for string: ${string} in language ${language}`
      );
    }
  }
  // default to english
  return translations["en"][string];
};

module.exports = {
  getTranslation,
};

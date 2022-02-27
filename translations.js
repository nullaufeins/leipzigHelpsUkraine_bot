const de = {
  transport: "Transport",
  transportDesc: "Biete/Suche Transportmöglichkeiten",
  donations: "Spenden",
  donationsDesc: "Finde Sammelstellen und Spendeninfos",
  legal: "Rechtsfragen",
  legalDesc: "Hilfe zu Rechtsfragen",
  housing: "Unterkünfte",
  housingDesc: "Biete/Suche Unterkünfte",
  translations: "Übersetzungen",
  translationsDesc: "Finde ÜbersetzerInnen",
  visitThisChannel: "Bitte melde dich in diesem Telegram-Channel:",
  welcomeMsg: "Bitte wähle eine Kategorie für dein Anliegen",
};
const en = {
  transport: "Transport",
  transportDesc: "offer/search for transport",
  donations: "Donations",
  donationsDesc: "get help with donations",
  legal: "Legal Requests",
  legalDesc: "get help with legal questions",
  housing: "Housing",
  housingDesc: "offer/search for housing",
  translations: "Translations",
  translationsDesc: "get help from translators",
  visitThisChannel: "Please join the following telegram channel:",
  welcomeMsg: "Please choose a category for your request"
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
  visitThisChannel: "будь-ласка, звертайся до цього телеграм каналу:",
  welcomeMsg: "будь-ласка, вибери категорію, що тебе цікавить"
}

// available translations
const translations = {
  de,
  en,
  uk
};

const getTranslation = (string, language) => {
  if (translations[language]) {
    if (translations[language][string]) {
      return translations[language][string];  
    } else {
      console.log(`Translation not found for string: ${string} in language ${language}`);
    }
  }
  // default to english
  return translations["en"][string];
};

module.exports = {
  getTranslation,
};

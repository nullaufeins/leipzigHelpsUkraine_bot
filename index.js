require("dotenv").config();
process.env.NTBA_FIX_319 = 1;
const TelegramBot = require("node-telegram-bot-api");
const { getTranslation } = require("./translations.js");

const bot = new TelegramBot(process.env.token, { polling: true });

/**
 * Available bot commands
 */
const TRANSPORT_CMD = "/transport";
const HOUSING_CMD = "/housing";
const DONATIONS_CMD = "/donations";
const LEGAL_CMD = "/legal";
const TRANSLATIONS_CMD = "/translations";

/**
 * Supported languages
 */
const SUPPORTED_LANG = ["en", "de", "uk"];

/**
 * Create bot commands array for all languages
 */
const commandsArray = SUPPORTED_LANG.map((lang) => {
  return [
    {
      command: TRANSPORT_CMD,
      description: getTranslation("transportDesc", lang),
    },
    {
      command: HOUSING_CMD,
      description: getTranslation("housingDesc", lang),
    },
    {
      command: DONATIONS_CMD,
      description: getTranslation("donationsDesc", lang),
    },
    {
      command: LEGAL_CMD,
      description: getTranslation("legalDesc", lang),
    },
    {
      command: TRANSLATIONS_CMD,
      description: getTranslation("translationsDesc", lang),
    },
  ];
});

/**
 * Function to set bot commands
 * https://github.com/yagop/node-telegram-bot-api/blob/master/doc/api.md#TelegramBot+setMyCommands
 */
const setBotCommands = async () => {
  await bot.setMyCommands(commandsArray[0], { language_code: "en" });    
  await bot.setMyCommands(commandsArray[1], { language_code: "de" });
  await bot.setMyCommands(commandsArray[2], { language_code: "uk" });
}

/**
 * Function to return inline keyboard categories for the user to select from
 *
 */
const getCategorySelection = (lang) => {
  return [
    [
      {
        text: getTranslation("transport", lang),
        callback_data: "transport",
      },
      {
        text: getTranslation("housing", lang),
        callback_data: "housing",
      },
    ],
    [
      {
        text: getTranslation("donations", lang),
        callback_data: "donations",
      },
      {
        text: getTranslation("legal", lang),
        callback_data: "legal",
      },
      {
        text: getTranslation("translations", lang),
        callback_data: "translations",
      },
    ],
  ];
};

/**
 * Response for transport category
 */
const transportResponse = (chatId, bot, language) => {
  const visitThisChannelText = getTranslation("visitThisChannel", language);
  const responseText = `${visitThisChannelText} @transport_leipzig_ukraine`;

  bot.sendMessage(chatId, responseText);
};

/**
 * Response for housing category
 */
const housingResponse = (chatId, bot, language) => {
  const visitThisChannelText = getTranslation("visitThisChannel", language);
  const responseText = `${visitThisChannelText} @accomodation_leipzig_ukraine`;

  bot.sendMessage(chatId, responseText);
};

/**
 * Response for donations category
 */
const donationsResponse = (chatId, bot, language) => {
  const visitThisChannelText = getTranslation("visitThisChannel", language);
  const responseText = `${visitThisChannelText} @donations_leipzig_ukraine`;

  bot.sendMessage(chatId, responseText);
};

/**
 * Response for legal category
 */
const legalResponse = (chatId, bot, language) => {
  const visitThisChannelText = getTranslation("visitThisChannel", language);
  const responseText = `${visitThisChannelText} @legal_leipzig_ukraine`;

  bot.sendMessage(chatId, responseText);
};

/**
 * Response for translations category
 */
const translationsResponse = (chatId, bot, language) => {
  const visitThisChannelText = getTranslation("visitThisChannel", language);
  const responseText = `${visitThisChannelText} @interpreter_leipzig_ukraine`;

  bot.sendMessage(chatId, responseText);
};

/**
 * Inline keyboard handler
 */
bot.on("callback_query", (msg) => {
  // chatId: unique identifier for the target chat or username of the target channel (in the format @channelusername)
  const chatId = msg.message.chat.id;
  const lang = msg.from.language_code;

  if (msg.data === "transport") {
    transportResponse(chatId, bot, lang);
  }
  if (msg.data === "housing") {
    housingResponse(chatId, bot, lang);
  }
  if (msg.data === "donations") {
    donationsResponse(chatId, bot, lang);
  }
  if (msg.data === "legal") {
    legalResponse(chatId, bot, lang);
  }
  if (msg.data === "translations") {
    translationsResponse(chatId, bot, lang);
  }
});

/**
 * Message handler
 */
bot.on("message", async function (msg, args) {
  const chatId = msg.chat.id;
  const lang = msg.from.language_code;
  

  if (msg.new_chat_members != undefined) {
    bot.sendMessage(chatId, getTranslation("welcomeMsg", lang), {
      reply_markup: {
        inline_keyboard: getCategorySelection(lang),
      },
    });
  }

  if (msg.text == "/start") {
    bot.sendMessage(chatId, getTranslation("welcomeMsg", lang), {
      reply_markup: {
        inline_keyboard: getCategorySelection(lang),
      },
    });
  }

  if (msg.text == "/help") {
    bot.sendMessage(chatId, getTranslation("welcomeMsg", lang), {
      reply_markup: {
        inline_keyboard: getCategorySelection(lang),
      },
    });
  }


  if (msg.text == TRANSPORT_CMD) {
    transportResponse(chatId, bot, lang);
  }

  if (msg.text == HOUSING_CMD) {
    housingResponse(chatId, bot);
  }

  if (msg.text == DONATIONS_CMD) {
    donationsResponse(chatId, bot);
  }

  if (msg.text == LEGAL_CMD) {
    legalResponse(chatId, bot);
  }

  if (msg.text == TRANSLATIONS_CMD) {
    translationsResponse(chatId, bot);
  }
});

/**
 * On server initialization
 */
setBotCommands();
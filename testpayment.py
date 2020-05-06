
"""
Basic example for a bot that can receive payment from user.
"""

import logging

from telegram import (LabeledPrice, ShippingOption,
                      InlineKeyboardButton as inlinebutt,
                      InlineKeyboardMarkup as inlinemark)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
Filters, PreCheckoutQueryHandler, ShippingQueryHandler, RegexHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start_callback(bot, update):
    print(update)
    msg = "Use /shipping to get an invoice for shipping-payment, "
    msg += "or /noshipping for an invoice without shipping."
    update.message.reply_text(msg)


def start_with_shipping_callback(bot, update):
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = "381764678:TEST:16004"
    start_parameter = "test-payment"
    currency = "rub"
    # price in dollars
    price = 100
    # price * 100 so as to include 2 decimal points
    # check https://core.telegram.org/bots/payments#supported-currencies for more details
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    bot.send_invoice(chat_id, title, description, payload,
                             provider_token, start_parameter, currency, prices,
                             need_name=True, need_phone_number=True,
                             need_email=True, need_shipping_address=True, is_flexible=True)


def start_without_shipping_callback(bot, update):
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = "381764678:TEST:16004"
    start_parameter = "test-payment"
    currency = "rub"
    # price in dollars
    price = 100
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    bot.send_invoice(chat_id, title, description, payload,
                             provider_token, start_parameter, currency, prices)


def shipping_callback(bot, update):
    print(update)
    query = update.shipping_query
    print(query)
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        bot.answerShippingQuery(update.shipping_query.id, ok=False, error_message="Something went wrong...")
        return
    else:
        options = list()
        # a single LabeledPrice
        options.append(ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)]))
        # an array of LabeledPrice objects
        price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
        options.append(ShippingOption('2', 'Shipping Option B', price_list))
        bot.answerShippingQuery(update.shipping_query.id, ok=True, shipping_options=options)


# after (optional) shipping, it's the pre-checkout
def precheckout_callback(bot, update):
    query = update.pre_checkout_query
    print(query)
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        bot.answerPreCheckoutQuery(update.pre_checkout_query.id, ok=False, error_message="Something went wrong...")
    else:
        bot.answerPreCheckoutQuery(update.pre_checkout_query.id, ok=True)


# finally, after contacting the payment provider...
def successful_payment_callback(bot,update):
    print(update)
    # do something after successfully receiving payment?
    update.message.reply_text("Thank you for your payment!")


def add_handlers(updater):
    dp = updater.dispatcher

    # simple start function
    dp.add_handler(CommandHandler('start', start_callback))
    dp.add_handler(RegexHandler("start", start_callback))
    dp.add_handler(CallbackQueryHandler(start_callback, pattern='start'))

    # Add command handler to start the payment invoice
    dp.add_handler(CommandHandler("shipping", start_with_shipping_callback))
    dp.add_handler(CommandHandler("noshipping", start_without_shipping_callback))

    # Optional handler if your product requires shipping
    dp.add_handler(ShippingQueryHandler(shipping_callback))

    # Pre-checkout handler to final check
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dp.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1233132022:AAH6wrRy9_Yp4TfrXsBosye9pVSB_4zc1lM")

    # Get the dispatcher to register handlers


    add_handlers(updater)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


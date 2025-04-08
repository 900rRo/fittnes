from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, PreCheckoutQueryHandler
import nest_asyncio
import asyncio
import aiohttp
from aiohttp import web

nest_asyncio.apply()

job_prices = {
    "копирайтер": 20000,
    "дизайнер": 30000,
    "видеомонтаж": 40000,
    "программист": 50000,
    "маркетолог": 45000,
    "smm-менеджер": 50000,
    "seo-специалист": 55000,
    "таргетолог": 50000,
    "менеджер по продажам": 60000,
    "аналитик данных": 55000
}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Используйте /add_vacancy для подачи вакансии.')

async def add_vacancy(update: Update, context: CallbackContext):
    await update.message.reply_text('Введите название вакансии:')
    context.user_data['step'] = 'title'

async def handle_message(update: Update, context: CallbackContext):
    step = context.user_data.get('step')

    if step == 'title':
        title = update.message.text
        if len(title) < 3:
            await update.message.reply_text('Название вакансии должно быть больше 3 символов. Введите ещё раз:')
        else:
            context.user_data['title'] = title
            await update.message.reply_text('Введите описание вакансии:')
            context.user_data['step'] = 'description'

    elif step == 'description':
        description = update.message.text
        if len(description) < 10:
            await update.message.reply_text('Описание должно быть больше 10 символов. Введите ещё раз:')
        else:
            context.user_data['description'] = description
            await update.message.reply_text('Введите условия работы:')
            context.user_data['step'] = 'conditions'

    elif step == 'conditions':
        conditions = update.message.text
        if len(conditions) < 5:
            await update.message.reply_text('Условия работы должны быть чёткими. Введите ещё раз:')
        else:
            context.user_data['conditions'] = conditions
            await update.message.reply_text('Введите профессию (например: копирайтер, дизайнер...):')
            context.user_data['step'] = 'salary'

    elif step == 'salary':
        job_title = update.message.text.lower()
        if job_title not in job_prices:
            await update.message.reply_text('Неверная профессия. Попробуйте снова.')
        else:
            context.user_data['salary'] = job_prices[job_title]
            await update.message.reply_text(f"""Ваша вакансия:
Название: {context.user_data['title']}
Описание: {context.user_data['description']}
Условия: {context.user_data['conditions']}
Цена за публикацию: {context.user_data['salary'] // 100:.2f} рублей
Подтверждаете? (Да/Нет)""")
            context.user_data['step'] = 'confirm'

async def confirm_vacancy(update: Update, context: CallbackContext):
    if update.message.text.lower() == 'да':
        await send_invoice(update, context)
    else:
        await update.message.reply_text('Вакансия не была опубликована.')

async def send_invoice(update: Update, context: CallbackContext):
    title = "Оплата за публикацию вакансии"
    description = f"Размещение вакансии '{context.user_data['title']}'"
    payload = "custom-payload"
    currency = "RUB"
    price = context.user_data['salary']
    prices = [LabeledPrice("Публикация вакансии", price)]

    await context.bot.send_invoice(
        chat_id=update.message.chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="YOUR_PROVIDER_TOKEN",  # ← Замени на свой
        currency=currency,
        prices=prices,
        start_parameter="payment",
        is_flexible=False
    )

async def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    if query.invoice_payload != 'custom-payload':
        await query.answer(ok=False, error_message="Ошибка в заказе.")
    else:
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: CallbackContext):
    await update.message.reply_text('Оплата прошла успешно! Вакансия опубликована.')

# Веб-сервер для /ping
async def handle_ping(request):
    return web.Response(text="OK")

async def run_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/ping", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=8080)
    await site.start()

# Пинг самого себя каждые 15 минут
async def ping_self():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                await session.get("https://your-render-url.onrender.com/ping")  # ← замени на свой URL
        except Exception as e:
            print(f"Ошибка пинга: {e}")
        await asyncio.sleep(900)

async def main():
    application = Application.builder().token("YOUR_TOKEN").build()  # ← Замени на свой токен

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_vacancy", add_vacancy))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Regex('^(Да|Нет)$'), confirm_vacancy))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    asyncio.create_task(run_web_server())
    asyncio.create_task(ping_self())

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.idle()

if __name__ == '__main__':
    asyncio.run(main())

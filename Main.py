from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
import buttons
import prices

API_TOKEN = '7460845141:AAENwy152IfB0F5MdPmg27Xp-O-shO6_dB4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

WELCOME_MESSAGE = "Здравствуйте! Добро пожаловать в нашу компанию. Мы рады предложить вам качественные услуги!"
ABOUT_US_MESSAGE = (
    "Наша компания предоставляет разнообразные услуги, включая профессиональные консультации и техническую помощь.\n"
    "Мы работаем на рынке уже несколько лет и заслужили доверие наших клиентов.\n"
    "Выберите интересующую вас услугу из меню ниже."
)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(WELCOME_MESSAGE, reply_markup=buttons.main_menu)


@dp.message_handler(commands=['about'])
async def about_command(message: types.Message):
    await about_text_command(message)


@dp.message_handler(lambda message: message.text == "Купить")
async def buy_command(message: types.Message):
    await get_buying_list(message)


@dp.message_handler(lambda message: message.text == "О компании")
async def about_text_command(message: types.Message):
    await message.answer(ABOUT_US_MESSAGE, reply_markup=buttons.back_button_menu)


@dp.message_handler(lambda message: message.text == "Помощь")
async def help_command(message: types.Message):
    help_text = "Если у вас есть вопросы, пожалуйста, свяжитесь с нами через раздел 'Контакты'."
    await message.answer(help_text, reply_markup=buttons.back_button_menu)


async def get_buying_list(message: types.Message):
    for i in range(1, 5):
        product = prices.services[i]
        product_info = (
            f"**Название:** {product['name']}\n"
            f"**Описание:** {product['description']}\n"
            f"**Цена:** {product['price']} рублей"
        )
        await message.answer(product_info, parse_mode=ParseMode.MARKDOWN)
        await message.answer_photo(photo=product["image_url"])

    await message.answer("Выберите продукт для покупки:", reply_markup=buttons.inline_product_menu)


@dp.callback_query_handler(lambda call: call.data in ["buy", "about"])
async def main_menu_callback_handler(call: types.CallbackQuery):
    if call.data == "buy":
        await get_buying_list(call.message)
    elif call.data == "about":
        await call.message.answer(ABOUT_US_MESSAGE, reply_markup=buttons.back_button_menu)
    await call.answer()


@dp.callback_query_handler(lambda call: call.data.startswith("product_buying"))
async def callback_buying_handler(call: types.CallbackQuery):
    await send_confirm_message(call)
    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "go_back")
async def callback_back_handler(call: types.CallbackQuery):
    await call.message.answer("Вы вернулись в главное меню.", reply_markup=buttons.main_menu)
    await call.answer()


async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

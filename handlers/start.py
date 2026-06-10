from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from data.texts import *
from data.keyboards import *
from database.models import get_user, create_user, is_banned

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    
    if is_banned(message.from_user.id):
        await message.answer("🚫 Вы заблокированы.")
        return
    
    await message.answer(
        START_TEXT,
        reply_markup=main_menu()
    )

# Обработчики кнопок Reply-меню
@router.message(F.text == "🛰️ Активировать симку")
async def activate_btn(message: Message):
    await message.answer("📱 Выберите способ:", reply_markup=type_keyboard())

@router.message(F.text == "🏛️ Купить Госуслуги")
async def gos_btn(message: Message):
    await message.answer(f"🏛️ Аккаунт Госуслуг\n💰 {PRICE_GOS}₽", reply_markup=payment_keyboard(PRICE_GOS, "gos"))

@router.message(F.text == "📋 Мои активации")
async def activations_btn(message: Message):
    from database.models import get_user_activations
    acts = get_user_activations(message.from_user.id)
    if not acts:
        await message.answer("📋 Нет активаций.", reply_markup=main_menu()); return
    text = "📋 <b>ВАШИ АКТИВАЦИИ:</b>\n\n"
    for a in acts[:10]:
        text += f"#{a['id']} | {a['type']} | {a['amount']}₽\n"
    await message.answer(text, reply_markup=main_menu())

@router.message(F.text == "💰 Тарифы")
async def prices_btn(message: Message):
    await message.answer(PRICES_TEXT, reply_markup=main_menu())

@router.callback_query(F.data == "start")
async def back_start(call: CallbackQuery):
    await call.message.answer(START_TEXT, reply_markup=main_menu())
    await call.message.delete()
    await call.answer()

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
        reply_markup=start_keyboard()
    )

@router.callback_query(F.data == "start")
async def back_start(call: CallbackQuery):
    if is_banned(call.from_user.id):
        await call.answer("🚫 Заблокированы!"); return
    await call.message.edit_text(START_TEXT, reply_markup=start_keyboard())
    await call.answer()

@router.callback_query(F.data == "prices")
async def prices(call: CallbackQuery):
    await call.message.edit_text(
        PRICES_TEXT,
        reply_markup=InlineKeyboardBuilder().button(text="❌ НАЗАД", callback_data="start").as_markup()
    )
    await call.answer()

@router.callback_query(F.data == "my_activations")
async def my_activations(call: CallbackQuery):
    from database.models import get_user_activations
    acts = get_user_activations(call.from_user.id)
    if not acts:
        await call.message.edit_text("📋 Нет активаций.", reply_markup=InlineKeyboardBuilder().button(text="❌ НАЗАД", callback_data="start").as_markup()); return
    text = "📋 <b>ВАШИ АКТИВАЦИИ:</b>\n\n"
    for a in acts[:10]:
        text += f"#{a['id']} | {a['type']} | {a['amount']}₽\n"
    await call.message.edit_text(text, reply_markup=InlineKeyboardBuilder().button(text="❌ НАЗАД", callback_data="start").as_markup())
    await call.answer()

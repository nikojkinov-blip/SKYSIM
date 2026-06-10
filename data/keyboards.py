from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# Твои кастомные эмодзи (как СТРОКИ!)
E_SKYSIM = "5283175099703268554"
E_CHECK = "5343909794149310690"
E_CROSS = "5210952531676504517"
E_DOLLAR = "5337049146534665824"

def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="АКТИВИРОВАТЬ СИМКУ", callback_data="activate", icon_custom_emoji_id=E_SKYSIM))
    builder.add(InlineKeyboardButton(text="КУПИТЬ ГОСУСЛУГИ", callback_data="buy_gos"))
    builder.add(InlineKeyboardButton(text="МОИ АКТИВАЦИИ", callback_data="my_activations"))
    builder.add(InlineKeyboardButton(text="ТАРИФЫ", callback_data="prices"))
    builder.adjust(1)
    return builder.as_markup()

def type_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="ЗАГРУЗИТЬ ФОТО", callback_data="type_photo"))
    builder.add(InlineKeyboardButton(text="ВВЕСТИ ВРУЧНУЮ", callback_data="type_manual"))
    builder.add(InlineKeyboardButton(text="НАЗАД", callback_data="start", icon_custom_emoji_id=E_CROSS))
    builder.adjust(1)
    return builder.as_markup()

def count_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="3 симки", callback_data="count_3", icon_custom_emoji_id=E_CHECK))
    builder.add(InlineKeyboardButton(text="5 симок", callback_data="count_5", icon_custom_emoji_id=E_CHECK))
    builder.add(InlineKeyboardButton(text="10 симок", callback_data="count_10", icon_custom_emoji_id=E_CHECK))
    builder.add(InlineKeyboardButton(text="НАЗАД", callback_data="activate", icon_custom_emoji_id=E_CROSS))
    builder.adjust(1)
    return builder.as_markup()

def payment_keyboard(amount: int, order_type: str):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="ОПЛАТИТЬ CRYPTO", callback_data=f"pay_crypto_{amount}_{order_type}", icon_custom_emoji_id=E_DOLLAR))
    builder.add(InlineKeyboardButton(text="ОПЛАТИТЬ КАРТОЙ", callback_data=f"pay_card_{amount}_{order_type}"))
    builder.add(InlineKeyboardButton(text="НАЗАД", callback_data="activate", icon_custom_emoji_id=E_CROSS))
    builder.adjust(1)
    return builder.as_markup()

def admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="СТАТИСТИКА", callback_data="admin_stats"))
    builder.add(InlineKeyboardButton(text="ЮЗЕРЫ", callback_data="admin_users"))
    builder.add(InlineKeyboardButton(text="АКТИВАЦИИ", callback_data="admin_activations"))
    builder.add(InlineKeyboardButton(text="РАССЫЛКА", callback_data="admin_broadcast"))
    builder.add(InlineKeyboardButton(text="БАН", callback_data="admin_ban_menu"))
    builder.add(InlineKeyboardButton(text="ЗАКРЫТЬ", callback_data="close", icon_custom_emoji_id=E_CROSS))
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()

def back_admin():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="НАЗАД", callback_data="admin", icon_custom_emoji_id=E_CROSS))
    return builder.as_markup()

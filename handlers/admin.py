from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from data.texts import *
from data.keyboards import *
from database.models import *
import os

router = Router()
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "6593438966").split(",")]

def is_admin(uid): return uid in ADMIN_IDS

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id): return
    s = get_stats()
    await message.answer(ADMIN_TEXT.format(users=s['users'], activations=s['activations'], revenue=s['revenue']), reply_markup=admin_keyboard())

@router.callback_query(F.data == "admin")
async def admin_back(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    s = get_stats()
    await call.message.edit_text(ADMIN_TEXT.format(users=s['users'], activations=s['activations'], revenue=s['revenue']), reply_markup=admin_keyboard())
    await call.answer()

@router.callback_query(F.data == "admin_stats")
async def admin_stats(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    s = get_stats()
    sim = db.fetchone("SELECT COUNT(*) as c FROM activations WHERE type='sim'")
    gos = db.fetchone("SELECT COUNT(*) as c FROM activations WHERE type='gos'")
    await call.message.edit_text(f"📊 <b>СТАТИСТИКА:</b>\n\n👥 Юзеров: {s['users']}\n📱 SIM: {sim['c'] if sim else 0}\n🏛️ Госуслуг: {gos['c'] if gos else 0}\n💰 Доход: {s['revenue']}₽", reply_markup=back_admin())
    await call.answer()

@router.callback_query(F.data == "admin_users")
async def admin_users(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    users = get_users_list(30)
    text = "👥 <b>ЮЗЕРЫ:</b>\n\n"
    for u in users:
        ban = "🚫" if u.get('banned') else "✅"
        text += f"{ban} <code>{u['user_id']}</code> | 💰{u.get('total_spent',0)}₽\n"
    await call.message.edit_text(text, reply_markup=back_admin())
    await call.answer()

@router.callback_query(F.data == "admin_activations")
async def admin_activations(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    acts = get_all_activations(30)
    if not acts: await call.message.edit_text("Нет.", reply_markup=back_admin()); return
    text = "📱 <b>АКТИВАЦИИ:</b>\n\n"
    for a in acts:
        text += f"#{a['id']} | <code>{a['user_id']}</code> | {a['type']} | {a['amount']}₽\n"
    await call.message.edit_text(text, reply_markup=back_admin())
    await call.answer()

@router.callback_query(F.data == "admin_ban_menu")
async def admin_ban_menu(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    await call.message.edit_text("🚫 <b>БАН/РАЗБАН:</b>\n<code>/ban ID</code>\n<code>/unban ID</code>\n<code>/find ID</code>", reply_markup=back_admin())
    await call.answer()

@router.message(Command("ban"))
async def ban_cmd(message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2: return
    uid = int(args[1])
    ban_user(uid, "Ручной бан")
    await message.answer(f"🚫 {uid} забанен!")

@router.message(Command("unban"))
async def unban_cmd(message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2: return
    uid = int(args[1])
    unban_user(uid)
    await message.answer(f"✅ {uid} разбанен!")

@router.message(Command("find"))
async def find_cmd(message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2: return
    q = args[1]
    if q.startswith("@"):
        u = db.fetchone("SELECT * FROM users WHERE username=?", (q[1:],))
    else:
        u = db.fetchone("SELECT * FROM users WHERE user_id=?", (int(q),))
    if not u: await message.answer("❌ Не найден."); return
    await message.answer(f"👤 ID: <code>{u['user_id']}</code>\n👤 @{u.get('username','?')}\n💰 Потратил: {u.get('total_spent',0)}₽\n🚫 Бан: {'Да' if u.get('banned') else 'Нет'}")

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(call: CallbackQuery):
    if not is_admin(call.from_user.id): return
    await call.message.edit_text("📢 <code>/bc ТЕКСТ</code>", reply_markup=back_admin())
    await call.answer()

@router.message(Command("bc"))
async def broadcast(message: Message):
    if not is_admin(message.from_user.id): return
    text = message.text.replace("/bc ", "", 1)
    if text == "/bc": return
    users = db.fetchall("SELECT user_id FROM users WHERE banned=0")
    sent = 0
    for u in users:
        try: await message.bot.send_message(u['user_id'], f"📢 {text}"); sent += 1
        except: pass
    await message.answer(f"✅ {sent}/{len(users)}")

@router.callback_query(F.data == "close")
async def close(call: CallbackQuery): await call.message.delete(); await call.answer()
import os

PRICE = int(os.getenv("PRICE_PER_SIM", "75"))
PRICE_GOS = int(os.getenv("PRICE_GOS", "375"))
CARD = os.getenv("CARD", "2200702171069789")
BANK = os.getenv("BANK", "Т-Банк")
USDT = os.getenv("USDT_WALLET", "TDBbi3P3tqmsRDrGfkyzJR5x9Z5Lpzjv6L")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "6593438966").split(",")]

START_TEXT = f"""🛰️ <b>SKY-SIM 2.0</b>

Активация сим-карт Билайн.
Доверенное лицо • Госуслуги.

💎 <b>Сим-карта:</b> от {PRICE}₽
🏛️ <b>Госуслуги (аккаунт):</b> {PRICE_GOS}₽
📦 <b>Минимум:</b> 3 симки

⚡ Активация за 15 минут
🔐 Конфиденциально"""

PRICES_TEXT = f"""📦 <b>ТАРИФЫ:</b>

<b>📱 СИМ-КАРТЫ:</b>
❌ 1 симка — закончились
✅ 3 симки — {PRICE*3}₽
✅ 5 симок — {PRICE*5}₽
✅ 10 симок — {PRICE*10}₽

<b>🏛️ ГОСУСЛУГИ:</b>
✅ Аккаунт — {PRICE_GOS}₽

💎 Цена за симку: {PRICE}₽"""

ADMIN_TEXT = """👑 <b>SKY-SIM 2.0 ADMIN</b>

👥 Юзеров: {users}
📱 Активаций: {activations}
💰 Доход: {revenue}₽"""
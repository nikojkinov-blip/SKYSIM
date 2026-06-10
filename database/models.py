import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "skysim.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

class Database:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cls._instance.conn.row_factory = sqlite3.Row
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance
    def execute(self, q, p=()):
        try: self.cursor.execute(q, p); self.conn.commit()
        except: self.conn.rollback()
    def fetchone(self, q, p=()): self.cursor.execute(q, p); r = self.cursor.fetchone(); return dict(r) if r else None
    def fetchall(self, q, p=()): self.cursor.execute(q, p); return [dict(r) for r in self.cursor.fetchall()]
    def insert(self, t, d):
        c = ', '.join(d.keys()); pl = ', '.join(['?' for _ in d])
        self.execute(f"INSERT INTO {t} ({c}) VALUES ({pl})", tuple(d.values()))
        return self.cursor.lastrowid
    def update(self, t, d, w, p):
        s = ', '.join([f"{k}=?" for k in d])
        self.execute(f"UPDATE {t} SET {s} WHERE {w}", tuple(d.values()) + p)

db = Database()

def init_db():
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT,
        joined_date TEXT, banned INTEGER DEFAULT 0, ban_reason TEXT,
        total_activations INTEGER DEFAULT 0, total_spent INTEGER DEFAULT 0
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS activations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
        iccid TEXT, type TEXT, sims_count INTEGER, amount INTEGER,
        status TEXT DEFAULT 'pending', created_at TEXT
    )''')
    print("✅ База готова!")

init_db()

def get_user(uid): return db.fetchone("SELECT * FROM users WHERE user_id=?", (uid,))
def create_user(uid, uname, fname):
    if not get_user(uid):
        db.insert('users', {'user_id': uid, 'username': uname or '', 'first_name': fname or '', 'joined_date': datetime.now().isoformat()})
def ban_user(uid, reason=""): db.update('users', {'banned': 1, 'ban_reason': reason}, 'user_id=?', (uid,))
def unban_user(uid): db.update('users', {'banned': 0, 'ban_reason': ''}, 'user_id=?', (uid,))
def is_banned(uid):
    u = get_user(uid)
    return u and u.get('banned')
def add_activation(uid, iccid, atype, count, amount):
    db.insert('activations', {'user_id': uid, 'iccid': iccid, 'type': atype, 'sims_count': count, 'amount': amount, 'created_at': datetime.now().isoformat()})
    db.update('users', {'total_activations': get_user(uid)['total_activations']+count, 'total_spent': get_user(uid)['total_spent']+amount}, 'user_id=?', (uid,))
def get_user_activations(uid):
    return db.fetchall("SELECT * FROM activations WHERE user_id=? ORDER BY created_at DESC LIMIT 20", (uid,))
def get_all_activations(limit=50):
    return db.fetchall("SELECT * FROM activations ORDER BY created_at DESC LIMIT ?", (limit,))
def get_users_list(limit=50):
    return db.fetchall("SELECT * FROM users ORDER BY joined_date DESC LIMIT ?", (limit,))
def get_stats():
    u = db.fetchone("SELECT COUNT(*) as c FROM users")
    a = db.fetchone("SELECT COUNT(*) as c FROM activations")
    r = db.fetchone("SELECT SUM(amount) as c FROM activations")
    return {'users': u['c'] if u else 0, 'activations': a['c'] if a else 0, 'revenue': r['c'] or 0 if r else 0}
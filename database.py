import sqlite3
from datetime import date

DB_NAME = "gyulekezet.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Presbiterek tábla (kibővítve a lakcím oszlopokkal)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presbiterek (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vezeteknev TEXT,
            keresztnev TEXT,
            szuletesi_datum TEXT,
            szuletesi_hely TEXT,
            telepules TEXT,
            utca TEXT,
            hazszam TEXT,
            neme TEXT,
            tagsag_kezdete TEXT,
            megjegyzes TEXT
        )
    ''')

    # 2. Tagok tábla (kibővítve a lakcím oszlopokkal)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tagok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vezeteknev TEXT,
            keresztnev TEXT,
            szuletesi_datum TEXT,
            szuletesi_hely TEXT,
            telepules TEXT,
            utca TEXT,
            hazszam TEXT,
            neme TEXT,
            tagsag_kezdete TEXT,
            presbiter_id INTEGER,
            megjegyzes TEXT,
            FOREIGN KEY (presbiter_id) REFERENCES presbiterek (id)
        )
    ''')

    # 3. Befizetések tábla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS befizetesek (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id INTEGER,
            ev INTEGER,
            honap INTEGER,
            FOREIGN KEY (tag_id) REFERENCES tagok (id)
        )
    ''')

    conn.commit()
    conn.close()

def szamol_eletkor(szuletesi_datum_str):
    try:
        szul_ev, szul_ho, szul_nap = map(int, szuletesi_datum_str.split('-'))
        ma = date.today()
        eletkor = ma.year - szul_ev - ((ma.month, ma.day) < (szul_ho, szul_nap))
        return str(eletkor)
    except:
        return "?"
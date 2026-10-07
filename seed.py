import sqlite3

# Csatlakozás az adatbázishoz
conn = sqlite3.connect("gyulekezet.db")
cursor = conn.cursor()

# --- 10 PRESBITER HOZZÁADÁSA ---
presbiterek_sql = """
INSERT INTO presbiterek (vezeteknev, keresztnev, szuletesi_datum, szuletesi_hely, telepules, utca, hazszam, neme, tagsag_kezdete, megjegyzes) VALUES 
('Tóth', 'Péter', '1965-03-12', 'Debrecen', 'Debrecen', 'Kossuth', '12', 'Férfi', '1995-01-10', 'Főpresbiter'),
('Szabó', 'Lajos', '1970-08-22', 'Nyíregyháza', 'Debrecen', 'Piac', '4', 'Férfi', '1998-05-11', 'Pénztáros'),
('Kovács', 'János', '1958-11-05', 'Budapest', 'Debrecen', 'Csapó', '23', 'Férfi', '1990-12-01', ''),
('Nagy', 'Mária', '1962-02-15', 'Debrecen', 'Debrecen', 'Böszörményi', '88', 'Nő', '1992-04-14', ''),
('Varga', 'István', '1975-09-30', 'Miskolc', 'Debrecen', 'Füredi', '5', 'Férfi', '2001-08-20', ''),
('Horváth', 'Zoltán', '1980-01-25', 'Debrecen', 'Debrecen', 'Hajnal', '11', 'Férfi', '2005-03-12', ''),
('Kiss', 'László', '1968-07-19', 'Eger', 'Debrecen', 'Mester', '34', 'Férfi', '1996-09-09', ''),
('Molnár', 'Gábor', '1972-12-04', 'Debrecen', 'Debrecen', 'Károlyi', '2', 'Férfi', '1999-11-11', ''),
('Németh', 'Katalin', '1978-06-14', 'Szeged', 'Debrecen', 'Cegléd', '19', 'Nő', '2003-02-28', ''),
('Farkas', 'József', '1955-04-08', 'Debrecen', 'Debrecen', 'Bem tér', '7', 'Férfi', '1985-07-15', 'Tiszteletbeli');
"""

# --- 20 TAG HOZZÁADÁSA ---
# A presbiter_id 1 és 10 közötti szám, amely a fenti presbiterekre hivatkozik
tagok_sql = """
INSERT INTO tagok (vezeteknev, keresztnev, szuletesi_datum, szuletesi_hely, telepules, utca, hazszam, neme, tagsag_kezdete, presbiter_id, megjegyzes) VALUES 
('Balogh', 'Anna', '1990-05-14', 'Debrecen', 'Debrecen', 'Darabos', '1', 'Nő', '2015-06-01', 1, 'Aktív'),
('Takács', 'Bence', '1995-10-21', 'Budapest', 'Debrecen', 'Homok', '42', 'Férfi', '2018-09-15', 2, ''),
('Juhász', 'Eszter', '1988-03-09', 'Debrecen', 'Debrecen', 'Böszörményi', '12', 'Nő', '2010-04-20', 3, ''),
('Mészáros', 'Dávid', '2000-12-12', 'Nyíregyháza', 'Debrecen', 'Kassai', '8', 'Férfi', '2022-01-10', 4, ''),
('Simon', 'Gergő', '1985-07-30', 'Debrecen', 'Debrecen', 'Nyíl', '55', 'Férfi', '2008-11-05', 5, ''),
('Rácz', 'Zsófia', '1992-01-18', 'Szolnok', 'Debrecen', 'Faraktár', '3', 'Nő', '2016-03-14', 6, ''),
('Fodor', 'Tamás', '1979-09-02', 'Debrecen', 'Debrecen', 'Vágóhíd', '9', 'Férfi', '2001-10-10', 7, ''),
('Gál', 'Nikolett', '1998-04-25', 'Miskolc', 'Debrecen', 'Kossuth', '45', 'Nő', '2019-12-01', 8, ''),
('Papp', 'Máté', '1993-08-11', 'Debrecen', 'Debrecen', 'Füredi', '21', 'Férfi', '2014-07-22', 9, ''),
('Lukács', 'Lilla', '1982-11-06', 'Eger', 'Debrecen', 'Péterfia', '11', 'Nő', '2005-05-05', 10, ''),
('Kerekes', 'Imre', '1960-02-14', 'Debrecen', 'Debrecen', 'Hadházi', '67', 'Férfi', '1990-08-15', 1, ''),
('Vincze', 'Dóra', '1996-06-19', 'Győr', 'Debrecen', 'Erzsébet', '4', 'Nő', '2020-02-28', 2, ''),
('Somogyi', 'Péter', '1981-12-30', 'Debrecen', 'Debrecen', 'Szabó Kálmán', '10', 'Férfi', '2003-09-09', 3, ''),
('Sándor', 'Klaudia', '1999-03-27', 'Debrecen', 'Debrecen', 'Derék', '99', 'Nő', '2021-11-11', 4, ''),
('Vörös', 'Ádám', '1994-05-08', 'Budapest', 'Debrecen', 'István', '22', 'Férfi', '2017-06-30', 5, ''),
('Hegedűs', 'Boglárka', '1987-10-15', 'Debrecen', 'Debrecen', 'Mikszáth', '7', 'Nő', '2012-10-12', 6, ''),
('Kocsis', 'Zsolt', '1976-01-04', 'Debrecen', 'Debrecen', 'Csapó', '89', 'Férfi', '1998-04-04', 7, ''),
('Bognár', 'Tímea', '1991-08-29', 'Nyíregyháza', 'Debrecen', 'Hatvan', '14', 'Nő', '2015-05-20', 8, ''),
('Kozma', 'Attila', '1984-07-07', 'Debrecen', 'Debrecen', 'Bethlen', '33', 'Férfi', '2007-08-08', 9, ''),
('Váradi', 'Noémi', '2002-09-16', 'Debrecen', 'Debrecen', 'Egyetem', '1', 'Nő', '2023-01-05', 10, 'Új tag');
"""

try:
    cursor.executescript(presbiterek_sql)
    cursor.executescript(tagok_sql)
    conn.commit()
    print("Sikeresen feltöltve az adatbázis 10 presbiterrel és 20 taggal!")
except Exception as e:
    print(f"Hiba történt: {e}")
finally:
    conn.close()
import sqlite3

DB_PATH = "/home/pi/inky-pi/inkypi_config.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS wifi_config 
                          (id INTEGER PRIMARY KEY, ssid TEXT, password TEXT)''')
        # Ensure a row exists to update
        cursor.execute("INSERT OR IGNORE INTO wifi_config (id) VALUES (1)")
        conn.commit()

def update_wifi_creds(ssid, password):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE wifi_config SET ssid = ?, password = ? WHERE id = 1", (ssid, password))
        conn.commit()
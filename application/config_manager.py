import sqlite3

class ConfigurationManager:
    def __init__(self, db_path="/home/pi/inky-pi/inkypi_config.db"):
        self.db_path = db_path
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, layout_mode TEXT, active_widget TEXT)")
            conn.execute("INSERT OR IGNORE INTO settings (id, layout_mode, active_widget) VALUES (1, 'grid', 'NamePlate')")

    def get_settings(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT layout_mode, active_widget FROM settings WHERE id = 1").fetchone()

    def update(self, mode, widget):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE settings SET layout_mode = ?, active_widget = ? WHERE id = 1", (mode, widget))
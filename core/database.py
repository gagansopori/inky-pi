import sqlite3
from pathlib import Path
from datetime import datetime
from core.logger import CustomLogger

# Anchor to project root/data
BASE_DIR = Path(__file__).resolve().parent.parent
# Ensure the data directory exists
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "inky_pi.db"

log = CustomLogger("database", log_to_file=False)


class DatabaseManager:
    """Handles all communication with the SQLite source of truth."""

    # SQL Constants for Prepared Statements
    GET_STATE_SQL = "SELECT * FROM system_state WHERE id = 1"
    UPDATE_MODE_SQL = "UPDATE system_state SET active_mode = ? WHERE id = 1"
    LOG_REFRESH_SQL = "UPDATE system_state SET last_refresh = ?, last_error = NULL WHERE id = 1"
    LOG_ERROR_SQL = "UPDATE system_state SET last_error = ? WHERE id = 1"

    GET_WIDGET_SQL = "SELECT * FROM widget_configs WHERE widget_id = ?"

    # --- NEW: WiFi Config SQL ---
    UPDATE_WIFI_SQL = "UPDATE wifi_config SET ssid = ?, password = ? WHERE id = 1"
    GET_WIFI_SQL = "SELECT * FROM wifi_config WHERE id = 1"

    UPSERT_WIDGET_SQL = """
        INSERT INTO widget_configs (widget_id, layout_slot, config_json)
        VALUES (?, ?, ?)
        ON CONFLICT(widget_id) DO UPDATE SET
            layout_slot=excluded.layout_slot,
            config_json=excluded.config_json
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _execute_query(self, query, params=(), fetch=False, commit=False):
        """Helper to manage the connection lifecycle and dictionary mapping."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)

                if commit:
                    conn.commit()
                if fetch:
                    return cursor.fetchall()
                return None
        except sqlite3.Error as e:
            log.error(f"Database Error: {e} | Query: {query}")
            return None

    # --- System State ---

    def get_system_state(self):
        results = self._execute_query(self.GET_STATE_SQL, fetch=True)
        return dict(results[0]) if results else None

    def update_active_mode(self, new_mode):
        log.info(f"Switching system mode to: {new_mode}")
        self._execute_query(self.UPDATE_MODE_SQL, (new_mode,), commit=True)

    def log_refresh(self, error_message=None):
        if error_message:
            self._execute_query(self.LOG_ERROR_SQL, (error_message,), commit=True)
        else:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._execute_query(self.LOG_REFRESH_SQL, (now,), commit=True)

    # --- WiFi Configuration (Merged from db_manager.py) ---

    def update_wifi_creds(self, ssid, password):
        """Saves Wi-Fi credentials from the setup portal."""
        log.info(f"Saving new Wi-Fi credentials for SSID: {ssid}")
        return self._execute_query(self.UPDATE_WIFI_SQL, (ssid, password), commit=True)

    def get_wifi_creds(self):
        """Retrieves stored Wi-Fi credentials."""
        results = self._execute_query(self.GET_WIFI_SQL, fetch=True)
        return dict(results[0]) if results else None

    # --- Widget Configs ---

    def get_widget_config(self, widget_id):
        results = self._execute_query(self.GET_WIDGET_SQL, (widget_id,), fetch=True)
        return dict(results[0]) if results else None

    def save_widget_config(self, widget_id, layout_slot, config_json):
        self._execute_query(self.UPSERT_WIDGET_SQL, (widget_id, layout_slot, config_json), commit=True)
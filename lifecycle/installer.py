import sqlite3
import shutil
import logging
import sys
from pathlib import Path

# =================================================================
# InkyPi Application Installer
# Purpose: Initialize database schema, directories, and assets.
# =================================================================

# 1. Path Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "inky_pi.db"
ASSETS_DIR = BASE_DIR / "assets"


# 2. Simple Console Logger for Lifecycle
def get_installer_logger():
    logger = logging.getLogger("installer")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


log = get_installer_logger()


def setup_directories():
    """Ensure the data directory exists."""
    if not DATA_DIR.exists():
        log.info(f"Creating data directory at {DATA_DIR}")
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    else:
        log.debug("Data directory already exists.")


def init_database():
    """Create the SQLite schema and seed default state."""
    log.info("Provisioning database schema...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            active_mode TEXT NOT NULL,
            is_enabled INTEGER DEFAULT 1,
            last_refresh TIMESTAMP,
            last_error TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS widget_configs (
            widget_id TEXT PRIMARY KEY,
            layout_slot TEXT DEFAULT 'full',
            config_json TEXT
        )
    ''')

    # 2. Seed System State Singleton
    cursor.execute("SELECT COUNT(*) FROM system_state")
    if cursor.fetchone()[0] == 0:
        log.info("First-run detected: Seeding default system state (name_plate).")
        cursor.execute('''
            INSERT INTO system_state (id, active_mode, is_enabled)
            VALUES (1, 'name_plate', 1)
        ''')

    # 3. Seed Widget Configs (Independent of System State)
    default_widgets = [
        ('clock', 'full', '{"show_seconds": false, "military_time": false}'),
        ('name_plate', 'full', '{}'),
        ('sports', 'full', '{"preferred_league": "NBA"}')
    ]

    for w_id, slot, cfg in default_widgets:
        cursor.execute("SELECT COUNT(*) FROM widget_configs WHERE widget_id = ?", (w_id,))
        if cursor.fetchone()[0] == 0:
            log.info(f"Seeding default config for {w_id}...")
            cursor.execute("INSERT INTO widget_configs (widget_id, layout_slot, config_json) VALUES (?, ?, ?)",
                           (w_id, slot, cfg))

    conn.commit()
    conn.close()


def sync_assets():
    """Ensure working .md files exist; fallback to examples."""
    required_files = ["identity.md", "sports_config.md"]

    for filename in required_files:
        target_file = ASSETS_DIR / filename
        # We look for files named 'identity_example.md' etc.
        example_file = ASSETS_DIR / f"{target_file.stem}_example.md"

        if not target_file.exists():
            if example_file.exists():
                log.warning(f"{filename} missing. Initializing from template...")
                shutil.copy(example_file, target_file)
            else:
                log.error(f"Critical Asset Missing: {filename} and no example found!")


def run():
    log.info("=== Starting InkyPi Application Setup ===")
    try:
        setup_directories()
        init_database()
        sync_assets()
        log.info("=== Application Setup Successfully Completed ===")
    except Exception as e:
        log.critical(f"Installation failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    run()
import sqlite3
import shutil
from pathlib import Path

# =================================================================
# InkyPi Application Installer
# Purpose: Initialize database schema, directories, and assets.
# =================================================================

# 1. Anchor Paths relative to this file (inky-pi/lifecycle/installer.py)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "inky_pi.db"
ASSETS_DIR = BASE_DIR / "assets"


def setup_directories():
    """Ensure the data directory exists."""
    if not DATA_DIR.exists():
        print(f"Creating data directory at {DATA_DIR}...")
        DATA_DIR.mkdir(parents=True, exist_ok=True)


def init_database():
    """Create the SQLite schema and seed default state."""
    print(f"Initializing database at {DB_PATH}...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create System State Table (Singleton)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            active_mode TEXT NOT NULL,
            is_enabled INTEGER DEFAULT 1,
            last_refresh TIMESTAMP,
            last_error TEXT
        )
    ''')

    # Create Widget Configs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS widget_configs (
            widget_id TEXT PRIMARY KEY,
            layout_slot TEXT DEFAULT 'full',
            config_json TEXT
        )
    ''')

    # Seed Factory Reset / Default Data
    cursor.execute("SELECT COUNT(*) FROM system_state")
    if cursor.fetchone()[0] == 0:
        print("Seeding default system state...")
        cursor.execute('''
            INSERT INTO system_state (id, active_mode, is_enabled)
            VALUES (1, 'name_plate', 1)
        ''')

    conn.commit()
    conn.close()


def sync_assets():
    """Check for required .md files; if missing, use examples."""
    required_files = ["identity.md", "sports_config.md"]

    for filename in required_files:
        target_file = ASSETS_DIR / filename
        example_file = ASSETS_DIR / f"{filename.split('.')[0]}_example.md"

        if not target_file.exists():
            if example_file.exists():
                print(f"Missing {filename}. Copying from {example_file.name}...")
                shutil.copy(example_file, target_file)
            else:
                print(f"Warning: Neither {filename} nor an example was found in assets.")


def run():
    print("--- Starting Application Layer Setup ---")
    setup_directories()
    init_database()
    sync_assets()
    print("--- Application Layer Setup Complete ---")


if __name__ == "__main__":
    run()
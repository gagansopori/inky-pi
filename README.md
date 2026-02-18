# inky-pi
Inky-Pi provides a service that allows you to customize your e-ink display with without going through the hassle of 
coding & then deploying user-friendly way to access and control your pimoroni-inky displays. 
This service allows you to convert your inky e-paper display into an information dashboard. For now its only going to 
fetch cartoons from the new yorker website and render it on your inky display, but more features are in the works.

Portals Design 

There are a couple of things we need to understand about this portal.

There are three main things that we need to achieve from this portal

There are 3 types of users for this - 
1. Superuser / Admin - Can alter permissions and Data. Has Root access to the service.
2. Profile Based User - Can customize all that he can see on his display. 
   1. Can save the state of his display/system/.
   2. Can customize the shape/size/build of the widgets through webservice.
3. Guest - Can only detect the system & do template widgets on the screen

## User Types
 - Superuser/ Admin
   - Can alter permissions and Data.
   - Has Root access to the service.
   - 
 - Registered User
   - Can save the state of his display/system/.
   - Can customize the shape/size/build of the widgets through webservice.
   - 
 - Guest/ One Time User
   - Can only do template widgets
   - Cant Save the state of his system.


### Project Structure
```markdown
inky-pi/
├── assets/                     # STATIC RESOURCES (Source of Truth)
│   ├── fonts/                  # Custom .ttf/.otf files (installed during setup)
│   ├── identity.md             # Name, Title, Company data
│   └── sports_config.md        # ESPN API URLs and preferences
│
├── core/                       # THE SERVER (Data & Hardware Orchestration)
│   ├── hardware/               # THE ADAPTERS (Hardware Abstraction Layer)
│   │   ├── __init__.py
│   │   ├── base.py             # Abstract Base Class for any e-paper
│   │   ├── inky_adapter.py     # Implementation for Pimoroni Inky
│   │   └── mock_adapter.py     # Implementation for local dev (saves to .png)
│   ├── widgets/                # THE STRATEGIES (Individual Logic Units)
│   │   ├── __init__.py
│   │   ├── base.py             # Widget & State base classes
│   │   ├── clock.py            # Time/Date logic
│   │   ├── name_plate.py       # MD parser for identity.md
│   │   └── sports.py           # API logic for sports_config.md
│   ├── __init__.py
│   ├── database.py             # SQLite interface (Bridge between Web and Core)
│   ├── orchestrator.py         # Main Loop: Poll DB -> Fetch -> Render -> Display
│   └── renderer.py             # PIL logic: Composes widgets into a single image
│
├── lifecycle/                  # THE SUPERVISOR (System State Management)
│   ├── __init__.py
│   ├── supervisor.py           # Traffic Cop: Decides Config vs. Run mode
│   ├── installer.py            # One-time setup (DB init, Font installation)
│   └── wifi_manager.py         # Hotspot/Access Point logic
│
├── scripts/                    # AUTOMATION
│   ├── install.sh              # Entry point for first-time installation
│   ├── start.sh                # Executed by Systemd on boot
│   └── update.sh               # OTA Update logic (Git pull + Restart)
│
├── tests/                      # Unit testing for widgets/logic
│
├── web/                        # THE CLIENT (Remote Control Interface)
│   ├── static/                 # CSS, JS, and UI Icons
│   ├── templates/
│   │   ├── dashboard.html      # Run Mode interface (Layout toggles)
│   │   └── config.html         # Config Mode interface (Wi-Fi setup)
│   ├── __init__.py
│   └── app.py                  # Flask server (Writes to DB, reads system status)
│
├── requirements.txt            # Python dependencies
├── inkypi.service              # Systemd configuration file
└── README.md                   # Project documentation
```



import threading, time
from flask import Flask, render_template, jsonify, request
from web.system import SystemManager
from zapplication.config_manager import ConfigurationManager
from core.renderer import InkyRenderer
from core.widgets import NamePlateWidget, NamePlateMini, NamePlateMaxi
from core.widgets import ClockWidget, ClockMini, ClockMaxi
from core.widgets import SportsWidget, SportsMini, SportsMaxi

app = Flask(__name__)
db = ConfigurationManager()


def worker():
    renderer = InkyRenderer()
    w_map = {"NamePlate": NamePlateWidget(), "Clock": ClockWidget(), "Sports": SportsWidget()}

    while True:
        mode, active = db.get_settings()
        if mode == 'grid':
            active_list = [w_map["NamePlate"], w_map["Clock"], w_map["Sports"]]
            w_map["NamePlate"].set_state(NamePlateMini())
            w_map["Clock"].set_state(ClockMini())
            w_map["Sports"].set_state(SportsMini())
        else:
            target = w_map.get(active, w_map["NamePlate"])
            state_cls = globals()[f"{active}Maxi"]
            target.set_state(state_cls())
            active_list = [target]

        for w in active_list: w.fetch_data()
        renderer.draw(active_list, mode)
        time.sleep(180)


@app.route('/')
def index(): return render_template('index.html')


@app.route('/api/system/shutdown', methods=['POST'])
def shutdown():
    SystemManager.shutdown()
    return jsonify({"status": "ok"})


@app.route('/api/settings/layout', methods=['POST'])
def set_layout():
    data = request.json
    db.update(data['mode'], data['active_widget'])
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    app.run(host='0.0.0.0', port=80)
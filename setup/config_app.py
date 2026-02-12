from flask import Flask, request, render_template_string
import subprocess
import db_manager

app = Flask(__name__)

# Modern, minimalist UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; padding: 40px 20px; background: #fafafa; color: #333; }
        .card { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h2 { margin-top: 0; color: #d63031; }
        label { font-size: 14px; font-weight: 600; display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 14px; background: #2d3436; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
        button:active { background: #000; }
    </style>
</head>
<body>
    <div class="card">
        <h2>InkyPi Setup</h2>
        <p>Enter the details for the new Wi-Fi network.</p>
        <form method="POST">
            <label>Wi-Fi Name (SSID)</label>
            <input type="text" name="ssid" placeholder="e.g. Home_Network" required>
            <label>Password</label>
            <input type="password" name="password" placeholder="••••••••" required>
            <button type="submit">Update & Reboot</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ssid = request.form.get('ssid')
        pwd = request.form.get('password')

        # Store in DB
        db_manager.update_wifi_creds(ssid, pwd)

        # The "Hand-off": Switch network and reboot
        # We use nmcli connect. If it fails, the boot_manager will bring us back here anyway.
        cmd = f"sleep 2 && nmcli device wifi connect '{ssid}' password '{pwd}' && sudo reboot"
        subprocess.Popen(cmd, shell=True)

        return """
            <body style="font-family:sans-serif; text-align:center; padding-top:50px;">
                <h2>Configuring...</h2>
                <p>The Pi is connecting to <b>{}</b>.</p>
                <p>This hotspot will close. If the screen doesn't update in 2 minutes, check your password and try again.</p>
            </body>
        """.format(ssid)

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
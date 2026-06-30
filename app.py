from flask import Flask, render_template, request, redirect, make_response
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Security logging function
def log_security_event(event_type, ip_address, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{event_type}] IP: {ip_address} | {details}\n"
    with open("security.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_line)

@app.route("/")
def home():
    return render_template("login.html")

from flask import Flask, render_template, request, redirect, make_response # תוסיפי את make_response

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "Customer")
    resp = make_response(redirect(f"/secure-zone/bank?user={username}"))
    resp.set_cookie('session_token', 'secure_user_session_12345') 
    return resp


@app.route("/secure-zone/bank")
def bank_dashboard():
    # Optional: You can get the user here if you need to do something in Python
    username = request.args.get("user", "Customer")
    return render_template("bank.html")

@app.route("/log", methods=['GET', 'POST'])
def log_data():
    # This captures the stolen cookies from the bot simulation
    if request.args:
        print(f"\n--- [!] New data received (GET) ---")
        for key, value in request.args.items():
            print(f"{key}: {value}")
            # Optional: Log this to security.log as well
            log_security_event("EXFILTRATION", request.remote_addr, f"{key}: {value}")
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)

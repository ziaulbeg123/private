from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os

app = Flask(__name__)

# ══════════════════════════════════════════════════
#  NOTIFICATION CONFIGURATION
#  Fill in your details below
# ══════════════════════════════════════════════════

# 📧 EMAIL NOTIFICATION SETTINGS
EMAIL_ENABLED = True
EMAIL_SENDER = "flyedu58@gmail.com"
EMAIL_PASSWORD = "aoqa qwmw cdcl cmbj"
EMAIL_RECEIVER = "flyedu58@gmail.com"

# 📱 WHATSAPP NOTIFICATION via CallMeBot (FREE)
WHATSAPP_ENABLED = False  # OFF - sirf email use ho raha hai
WHATSAPP_PHONE = "918191876059"
WHATSAPP_API_KEY = ""


# ══════════════════════════════════════════════════
#  GOOGLE SHEETS SETUP
# ══════════════════════════════════════════════════
def save_to_google_sheet(data):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Contact Information (Responses)").sheet1
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("first_name"),
            data.get("last_name"),
            data.get("phone"),
            data.get("email"),
            data.get("interest"),
            data.get("country"),
            data.get("message")
        ])
        print("✅ Saved to Google Sheets")
    except Exception as e:
        print(f"❌ Google Sheets Error: {e}")


# ══════════════════════════════════════════════════
#  📧 EMAIL NOTIFICATION
# ══════════════════════════════════════════════════
def send_email_notification(data):
    if not EMAIL_ENABLED:
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚀 New Lead: {data.get('first_name')} {data.get('last_name')} - FlyEdu Abroad"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        html = f"""
        <html>
        <body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
            <div style="max-width:600px;margin:auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
                <div style="background:linear-gradient(135deg,#040d21,#0f2040);padding:30px;text-align:center;">
                    <h1 style="color:#f5c518;font-size:28px;margin:0;">🎓 New Student Lead!</h1>
                    <p style="color:rgba(255,255,255,0.7);margin:8px 0 0;">FlyEdu Abroad – Contact Form</p>
                </div>
                <div style="padding:30px;">
                    <table style="width:100%;border-collapse:collapse;">
                        <tr style="border-bottom:1px solid #eee;">
                            <td style="padding:12px 8px;color:#666;font-weight:bold;width:35%;">👤 Full Name</td>
                            <td style="padding:12px 8px;color:#111;font-size:16px;">{data.get('first_name')} {data.get('last_name')}</td>
                        </tr>
                        <tr style="border-bottom:1px solid #eee;background:#fafafa;">
                            <td style="padding:12px 8px;color:#666;font-weight:bold;">📱 Phone</td>
                            <td style="padding:12px 8px;color:#111;font-size:16px;"><a href="tel:{data.get('phone')}" style="color:#0d6efd;">{data.get('phone')}</a></td>
                        </tr>
                        <tr style="border-bottom:1px solid #eee;">
                            <td style="padding:12px 8px;color:#666;font-weight:bold;">📧 Email</td>
                            <td style="padding:12px 8px;color:#111;font-size:16px;"><a href="mailto:{data.get('email')}" style="color:#0d6efd;">{data.get('email')}</a></td>
                        </tr>
                        <tr style="border-bottom:1px solid #eee;background:#fafafa;">
                            <td style="padding:12px 8px;color:#666;font-weight:bold;">🎯 Interest</td>
                            <td style="padding:12px 8px;color:#111;font-size:16px;">{data.get('interest', 'N/A')}</td>
                        </tr>
                        <tr style="border-bottom:1px solid #eee;">
                            <td style="padding:12px 8px;color:#666;font-weight:bold;">🌍 Country</td>
                            <td style="padding:12px 8px;color:#111;font-size:16px;">{data.get('country', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding:12px 8px;color:#666;font-weight:bold;">💬 Message</td>
                            <td style="padding:12px 8px;color:#111;">{data.get('message', 'No message')}</td>
                        </tr>
                    </table>
                    <div style="margin-top:24px;text-align:center;">
                        <a href="https://wa.me/{data.get('phone','')}" 
                           style="background:#25d366;color:white;padding:12px 28px;border-radius:50px;text-decoration:none;font-weight:bold;font-size:15px;display:inline-block;">
                            📱 WhatsApp This Lead
                        </a>
                    </div>
                </div>
                <div style="background:#f8f9fa;padding:16px;text-align:center;color:#999;font-size:13px;">
                    Received at {datetime.now().strftime('%d %b %Y, %I:%M %p')} | FlyEdu Abroad CRM
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("✅ Email notification sent!")
    except Exception as e:
        print(f"❌ Email Error: {e}")


# ══════════════════════════════════════════════════
#  📱 WHATSAPP NOTIFICATION via CallMeBot (FREE)
# ══════════════════════════════════════════════════
def send_whatsapp_notification(data):
    if not WHATSAPP_ENABLED:
        return
    try:
        name = f"{data.get('first_name','')} {data.get('last_name','')}"
        phone = data.get('phone', 'N/A')
        interest = data.get('interest', 'N/A')
        country = data.get('country', 'N/A')

        message = (
            f"🚀 *NEW LEAD - FlyEdu Abroad*\n\n"
            f"👤 *Name:* {name}\n"
            f"📱 *Phone:* {phone}\n"
            f"📧 *Email:* {data.get('email','N/A')}\n"
            f"🎯 *Interest:* {interest}\n"
            f"🌍 *Country:* {country}\n"
            f"💬 *Message:* {data.get('message','None')}\n\n"
            f"⏰ {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
            f"_Call back within 5 minutes!_ ⚡"
        )

        url = f"https://api.callmebot.com/whatsapp.php"
        params = {
            "phone": WHATSAPP_PHONE,
            "text": message,
            "apikey": WHATSAPP_API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("✅ WhatsApp notification sent!")
        else:
            print(f"⚠️ WhatsApp response: {response.status_code}")
    except Exception as e:
        print(f"❌ WhatsApp Error: {e}")


# ══════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        form_data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "interest": request.form.get("interest"),
            "country": request.form.get("country"),
            "message": request.form.get("message"),
        }
        print("📥 FORM SUBMITTED:", form_data)

        # Save to Google Sheets
        save_to_google_sheet(form_data)

        # Send notifications (runs async-ish – won't block page load)
        send_email_notification(form_data)
        send_whatsapp_notification(form_data)

        # Redirect with success flag
        return redirect(url_for('contact', submitted=1))

    submitted = request.args.get('submitted')
    return render_template('contact.html', submitted=submitted)


if __name__ == '__main__':
    app.run(debug=True)
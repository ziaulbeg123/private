import os
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)

# ══════════════════════════════════════════════════
#  📧 EMAIL CONFIGURATION
# ══════════════════════════════════════════════════
EMAIL_SENDER   = "flyedu58@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "aoqa qwmw cdcl cmbj")
EMAIL_RECEIVER = "flyedu58@gmail.com"


# ══════════════════════════════════════════════════
#  📧 EMAIL FUNCTION — Port 587 TLS (Render compatible)
# ══════════════════════════════════════════════════
def send_email_notification(data):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"New Lead: {data.get('first_name')} {data.get('last_name')} - FlyEdu Abroad"
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = EMAIL_RECEIVER

        html = f"""
        <html>
        <body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px;">
            <div style="max-width:600px;margin:auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1);">

                <div style="background:linear-gradient(135deg,#040d21,#0f2040);padding:30px;text-align:center;">
                    <h1 style="color:#f5c518;font-size:26px;margin:0;">New Student Lead!</h1>
                    <p style="color:rgba(255,255,255,0.6);margin:8px 0 0;font-size:14px;">FlyEdu Abroad — Contact Form</p>
                </div>

                <div style="padding:30px;">
                    <table style="width:100%;border-collapse:collapse;">
                        <tr style="border-bottom:1px solid #eee;">
                            <td style="padding:14px 8px;color:#888;font-weight:700;width:35%;font-size:13px;">Full Name</td>
                            <td style="padding:14px 8px;color:#111;font-size:15px;font-weight:600;">{data.get('first_name')} {data.get('last_name')}</td>
                        </tr>
                        <tr style="border-bottom:1px solid #eee;background:#fafafa;">
                            <td style="padding:14px 8px;color:#888;font-weight:700;font-size:13px;">Phone</td>
                            <td style="padding:14px 8px;font-size:15px;font-weight:600;">
                                <a href="tel:{data.get('phone')}" style="color:#0d6efd;text-decoration:none;">{data.get('phone')}</a>
                            </td>
                        </tr>
                        <tr style="border-bottom:1px solid #eee;">
                            <td style="padding:14px 8px;color:#888;font-weight:700;font-size:13px;">Email</td>
                            <td style="padding:14px 8px;font-size:15px;">
                                <a href="mailto:{data.get('email')}" style="color:#0d6efd;text-decoration:none;">{data.get('email')}</a>
                            </td>
                        </tr>
                        <tr style="border-bottom:1px solid #eee;background:#fafafa;">
                            <td style="padding:14px 8px;color:#888;font-weight:700;font-size:13px;">Interest</td>
                            <td style="padding:14px 8px;color:#111;font-size:15px;">{data.get('interest') or 'N/A'}</td>
                        </tr>
                        <tr style="border-bottom:1px solid #eee;">
                            <td style="padding:14px 8px;color:#888;font-weight:700;font-size:13px;">Country</td>
                            <td style="padding:14px 8px;color:#111;font-size:15px;">{data.get('country') or 'N/A'}</td>
                        </tr>
                        <tr>
                            <td style="padding:14px 8px;color:#888;font-weight:700;font-size:13px;">Message</td>
                            <td style="padding:14px 8px;color:#555;font-size:14px;">{data.get('message') or '—'}</td>
                        </tr>
                    </table>

                    <div style="margin-top:28px;text-align:center;">
                        <a href="https://wa.me/{data.get('phone','').replace('+','').replace(' ','')}"
                           style="background:#25d366;color:white;padding:14px 32px;border-radius:50px;text-decoration:none;font-weight:700;font-size:15px;display:inline-block;">
                            WhatsApp This Lead Now
                        </a>
                    </div>
                </div>

                <div style="background:#f8f9fa;padding:16px;text-align:center;color:#aaa;font-size:12px;">
                    Received at {datetime.now().strftime('%d %b %Y, %I:%M %p')} | FlyEdu Abroad
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        # ✅ Port 587 + STARTTLS — Render pe kaam karta hai
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("✅ Email sent successfully!")
        return True

    except Exception as e:
        print(f"❌ Email Error: {e}")
        return False


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
            "last_name":  request.form.get("last_name"),
            "phone":      request.form.get("phone"),
            "email":      request.form.get("email"),
            "interest":   request.form.get("interest"),
            "country":    request.form.get("country"),
            "message":    request.form.get("message"),
        }
        print("FORM SUBMITTED:", form_data)
        send_email_notification(form_data)
        return redirect(url_for('contact', submitted=1))

    submitted = request.args.get('submitted')
    return render_template('contact.html', submitted=submitted)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
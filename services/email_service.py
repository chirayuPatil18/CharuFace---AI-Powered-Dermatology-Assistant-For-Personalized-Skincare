import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# SEND OTP EMAIL
def send_otp_email(to_email, otp):

    subject = "CharuFace OTP Verification"
    body = f"""
Your OTP is: {otp}

This OTP is valid for a short time.
Do not share it with anyone.
"""

    send_email(to_email, subject, body)


# SEND REPORT EMAIL
def send_report_email(to_email, result):

    issue = result.get("issue", "").upper()
    severity = result.get("severity", "")
    confidence = result.get("confidence", "")
    rec = result.get("recommendation", {})

    ingredients = "".join([f"<li>{i}</li>" for i in rec.get("ingredients", [])])
    avoid = "".join([f"<li>{i}</li>" for i in rec.get("avoid", [])])

    morning = "".join([f"<li>{i}</li>" for i in rec.get("routine", {}).get("morning", [])])
    night = "".join([f"<li>{i}</li>" for i in rec.get("routine", {}).get("night", [])])

    diet_eat = "".join([f"<li>{i}</li>" for i in rec.get("diet", {}).get("foods_to_eat", [])])
    diet_avoid = "".join([f"<li>{i}</li>" for i in rec.get("diet", {}).get("foods_to_avoid", [])])

    products_html = ""
    for p in rec.get("products", []):
        link = f"https://www.amazon.in/s?k={p.get('name','').replace(' ','+')}"
        products_html += f"""
        <div style="margin-bottom:10px;">
            <b>{p.get('name')}</b><br>
            <span style="color:#555;">{p.get('reason')}</span><br>
            <a href="{link}" style="color:#ff4d6d;">View Product</a>
        </div>
        """

    html = f"""
    <html>
    <body style="margin:0;padding:0;font-family:Segoe UI;background:#f4f6f8;">

    <div style="max-width:600px;margin:auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.1);">

        <!-- HEADER -->
        <div style="background:linear-gradient(135deg,#ff4d6d,#ff758f);padding:20px;color:white;text-align:center;">
            <h2>CharuFace AI Skin Report</h2>
            <p>Your personalized skincare insights</p>
        </div>

        <!-- CONTENT -->
        <div style="padding:20px;color:#333;">

            <h3>{issue} ({severity})</h3>
            <p><b>Confidence:</b> {confidence}%</p>
            <p>{rec.get("explanation","")}</p>

            <hr>

            <h3>✨ Ingredients</h3>
            <ul>{ingredients}</ul>

            <h3>⚠️ Avoid</h3>
            <ul>{avoid}</ul>

            <h3>🧴 Routine</h3>
            <b>Morning</b>
            <ul>{morning}</ul>

            <b>Night</b>
            <ul>{night}</ul>

            <h3>🥗 Diet</h3>
            <b>Eat</b>
            <ul>{diet_eat}</ul>

            <b>Avoid</b>
            <ul>{diet_avoid}</ul>

            <h3>🛍 Recommended Products</h3>
            {products_html}

        </div>

        <!-- FOOTER -->
        <div style="background:#f1f5f9;padding:15px;text-align:center;font-size:12px;color:#666;">
            Powered by CharuFace AI • Personalized Skincare Assistant
        </div>

    </div>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your CharuFace Skin Report"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email error:", e)

# CORE MAIL FUNCTION
def send_email(to_email, subject, body):

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)

    server.send_message(msg)
    server.quit()
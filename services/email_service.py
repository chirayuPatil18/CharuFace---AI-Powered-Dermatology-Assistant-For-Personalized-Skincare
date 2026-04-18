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

    # ✅ NEW: HOME REMEDIES
    home_remedies = "".join([f"<li>{i}</li>" for i in rec.get("home_remedies", [])])

    # PRODUCTS
    products_html = ""
    for p in rec.get("products", []):
        link = p.get("link") or f"https://www.amazon.in/s?k={p.get('name','').replace(' ','+')}"
        products_html += f"""
        <div style="background:#f9fafb;padding:12px;border-radius:10px;margin-bottom:10px;border:1px solid #eee;">
            <b style="color:#111;">{p.get('name')}</b><br>
            <span style="color:#555;">{p.get('reason')}</span><br>
            <a href="{link}" style="color:#ff4d6d;font-weight:500;text-decoration:none;">View Product →</a>
        </div>
        """

    # 🔥 IMPROVED PREMIUM UI
    html = f"""
    <html>
    <body style="margin:0;padding:0;font-family:Segoe UI;background:#0f172a;">

    <div style="max-width:650px;margin:auto;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,0.3);">

        <!-- HEADER -->
        <div style="background:linear-gradient(135deg,#ff4d6d,#fb7185);padding:25px;color:white;text-align:center;">
            <h2 style="margin:0;">✨ CharuFace AI Skin Report</h2>
            <p style="margin:5px 0 0;">Personalized Dermatology Insights</p>
        </div>

        <!-- CONTENT -->
        <div style="padding:25px;color:#1e293b;">

            <h2 style="margin-bottom:5px;">{issue} ({severity})</h2>
            <p><b>Confidence:</b> {confidence}%</p>
            <p style="line-height:1.6;">{rec.get("explanation","")}</p>

            <hr style="margin:20px 0;">

            <h3 style="color:#ff4d6d;">✨ Key Ingredients</h3>
            <ul>{ingredients}</ul>

            <h3 style="color:#ef4444;">⚠️ What to Avoid</h3>
            <ul>{avoid}</ul>

            <h3 style="color:#6366f1;">🧴 Skincare Routine</h3>
            <b>Morning</b>
            <ul>{morning}</ul>

            <b>Night</b>
            <ul>{night}</ul>

            <!-- ✅ NEW HOME REMEDIES SECTION -->
            <h3 style="color:#10b981;">🏠 Home Remedies</h3>
            <ul>{home_remedies}</ul>

            <h3 style="color:#f59e0b;">🥗 Diet Recommendations</h3>
            <b>Eat</b>
            <ul>{diet_eat}</ul>

            <b>Avoid</b>
            <ul>{diet_avoid}</ul>

            <h3 style="color:#ec4899;">🛍 Recommended Products</h3>
            {products_html}

        </div>

        <!-- FOOTER -->
        <div style="background:#f1f5f9;padding:15px;text-align:center;font-size:12px;color:#64748b;">
            Powered by CharuFace AI • Smart Skincare Assistant
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

        print("Email sent successfully")

    except Exception as e:
        print("Email error:", e)


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
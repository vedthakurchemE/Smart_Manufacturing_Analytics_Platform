# 📦 Module 8: Notification Bot | SensorGuardAI Suite
# 📧 Sends alerts via Gmail (secure) and Telegram
# 📦 Author: Ved Thakur | IPS Academy Indore | BTech ChemEng

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import requests
import os

# === Gmail Configuration ===
# 🔐 Use Gmail App Password (not your real password)
EMAIL_ADDRESS = os.environ.get("EMAIL_USER", "vedthakursa@gmail.com")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS", "duvw iefq qgwc qeiu")  # Replace or use env vars

def send_email_alert(subject, body, receiver="receiver@example.com"):
    """
    Send alert email using secure Gmail SMTP with app password.

    Args:
        subject (str): Email subject
        body (str): Email body (text only)
        receiver (str): Recipient email address
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        st.success(f"📧 Email sent successfully to {receiver}!")

    except Exception as e:
        st.error(f"❌ Email Send Error: {e}")

def run():
    """
    Streamlit test page for Notification Bot (Email + Telegram).
    """
    st.header("📢 Notification Bot Tester")
    st.markdown("Send alert via **Gmail (SMTP)** or **Telegram Bot API**")

    subject = st.text_input("✉️ Email Subject", value="SensorGuardAI Alert")
    body = st.text_area("📝 Email / Telegram Body", value="⚠️ Fault detected in Reactor-2. Please investigate.")
    receiver = st.text_input("📨 Send To Email", value="receiver@example.com")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📧 Send Email"):
            send_email_alert(subject, body, receiver)

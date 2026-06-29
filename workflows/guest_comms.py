"""
Guest communication workflows.
Sends booking confirmations, check-in instructions, and departure reminders.
Triggered by Guesty webhook events.
"""

import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logger = logging.getLogger(__name__)


class GuestComms:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.sendgrid.net")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "apikey")
        self.smtp_pass = os.getenv("SMTP_PASS", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@christianopm.com")

    def _send(self, to: str, subject: str, body: str):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = to
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.sendmail(self.from_email, to, msg.as_string())
        logger.info(f"Email sent to {to}: {subject}")

    async def send_confirmation(self, reservation: dict):
        guest = reservation.get("guest", {})
        to_email = guest.get("email", "")
        if not to_email:
            logger.warning("No guest email found, skipping confirmation")
            return

        checkin  = reservation.get("checkIn",  "N/A")
        checkout = reservation.get("checkOut", "N/A")
        name     = guest.get("fullName", "Guest")

        subject = f"Booking Confirmed — {reservation.get('listingName', 'Your Stay')}"
        body = f"""
        <h2>Hi {name},</h2>
        <p>Your booking is confirmed.</p>
        <ul>
          <li><strong>Check-in:</strong> {checkin}</li>
          <li><strong>Check-out:</strong> {checkout}</li>
          <li><strong>Property:</strong> {reservation.get('listingName', '')}</li>
        </ul>
        <p>Your access code will be sent 24 hours before arrival.</p>
        <p>Christiano Vincenti Property Management</p>
        """
        self._send(to_email, subject, body)

    async def send_checkin_instructions(self, reservation: dict, access_code: str):
        guest    = reservation.get("guest", {})
        to_email = guest.get("email", "")
        name     = guest.get("fullName", "Guest")
        subject  = "Your check-in instructions & access code"
        body = f"""
        <h2>Hi {name},</h2>
        <p>Your check-in is tomorrow. Here are your details:</p>
        <p><strong>Access code: {access_code}</strong></p>
        <p>Enter this code at the gate panel. Valid for the duration of your stay.</p>
        <p>Christiano Vincenti Property Management</p>
        """
        self._send(to_email, subject, body)

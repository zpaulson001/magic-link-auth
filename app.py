import os
import smtplib
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, Form

app = FastAPI()

load_dotenv()


def send_email(sender: str, recipient: str, message: str | None):

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
    SMTP_URL = os.getenv("SMTP_URL")

    MESSAGE = f"""From: {sender} {EMAIL}
To: {recipient} {RECIPIENT_EMAIL}
Subject: hello there

{message}
"""

    print(MESSAGE)

    server = smtplib.SMTP(SMTP_URL, 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, RECIPIENT_EMAIL, MESSAGE)


@app.get("/")
async def root():
    return {"message": "look out world 👀"}


@app.post("/send")
async def send_away(
    recipient: Annotated[str, Form()],
    sender: Annotated[str, Form()],
    message: Annotated[str | None, Form()] = None,
):
    send_email(sender=sender, recipient=recipient, message=message)
    return "✉️"

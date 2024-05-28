import os
import jwt
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = FastAPI()

load_dotenv()


def send_magic_link(user_id: int):

    encoded_jwt = jwt.encode({"user_id": user_id}, "secret")

    FROM_EMAIL = os.getenv("FROM_EMAIL")
    TO_EMAIL = os.getenv("TO_EMAIL")

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject="Login Link",
        html_content=f"<strong>Here's your token: {encoded_jwt}</strong>",
    )

    try:
        sg = SendGridAPIClient(os.getenv("SG_API_KEY"))
        response = sg.send(message)
    except Exception as e:
        print(e.message)

    return "success"


@app.get("/")
async def root():
    return {"message": "look out world 👀"}


@app.post("/send")
async def send_away(user_id: Annotated[int, Form()]):
    result = send_magic_link(user_id)
    return result

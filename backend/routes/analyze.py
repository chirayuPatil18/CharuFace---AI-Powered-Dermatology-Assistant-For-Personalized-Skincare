from fastapi import APIRouter
from pydantic import BaseModel
import base64
import os
import uuid
import requests

from inference.pipeline import predict_from_images
from rag.rag_pipeline import run_rag
from services.product_service import enrich_products
from services.email_service import send_report_email 

# MEMORY IMPORT
from chatbot.chat_pipeline import save_memory, load_memory

router = APIRouter()

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class AnalyzeRequest(BaseModel):
    images: dict
    user_profile: dict

# SAVE IMAGE
def save_base64_image(base64_str, name):
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]

    image_data = base64.b64decode(base64_str)

    filename = f"{name}_{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(image_data)

    return filepath

# WEATHER API
def get_environment(user):
    try:
        API_KEY = os.getenv("OPENWEATHER_API_KEY")

        location = user.get("location")

        if location:
            lat = location.get("lat")
            lon = location.get("lon")
        else:
            return "normal (location not provided)"

        weather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        ).json()

        temp = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        condition = weather["weather"][0]["main"]

        if humidity > 70:
            env = "humid"
        elif temp > 32:
            env = "hot"
        elif humidity < 30:
            env = "dry"
        else:
            env = "normal"

        return f"{env} ({condition}, {temp}°C, humidity={humidity}%)"

    except Exception as e:
        print("Weather API error:", e)
        return "normal"

# MAIN API
@router.post("/analyze")
async def analyze(request: AnalyzeRequest):

    print("\n REQUEST RECEIVED")

    try:
        image_paths = []

        # SAVE IMAGES
        for key in ["left", "center", "right"]:
            path = save_base64_image(request.images[key], key)
            image_paths.append(path)

        user = request.user_profile
        concern = user.get("concern", "acne")

        # ENVIRONMENT
        user["environment"] = get_environment(user)
        print("Environment:", user["environment"])

        # AI PIPELINE
        issue, severity, confidence = predict_from_images(image_paths, concern)

        # RAG
        rag_response = run_rag(
            user_query=f"Skincare advice for {issue}",
            skin_issue=issue,
            severity=severity,
            user_profile=user
        )

        # PRODUCT ENRICHMENT
        if isinstance(rag_response, dict) and "products" in rag_response:
            rag_response["products"] = enrich_products(rag_response["products"])

        # FINAL RESPONSE
        result_data = {
            "issue": issue,
            "severity": severity,
            "confidence": round(confidence * 100, 2),
            "environment": user["environment"],
            "recommendation": rag_response
        }

        # SEND EMAIL REPORT
        try:
            user_email = user.get("email")

            print("Email received from frontend:", user_email)

            if user_email:
                send_report_email(user_email, result_data)
                print("Email sent successfully to:", user_email)
            else:
                print("No email found in user_profile")

        except Exception as e:
            print("Email sending failed:", str(e))

        # SAVE MEMORY
        email = user.get("email")  # get email from frontend

        if email:
            memory = load_memory(email)
        else:
            memory = {}

        memory["profile"] = user
        memory["recommendation"] = rag_response

        if email:
            save_memory(email, memory)

        return result_data

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
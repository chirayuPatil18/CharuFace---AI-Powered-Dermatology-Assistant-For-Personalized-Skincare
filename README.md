# 🧠 CharuFace – AI Dermatology System

> An intelligent, end-to-end AI system that analyzes facial skin conditions and generates **personalized skincare recommendations** using Computer Vision + RAG + LLMs.

---

## 🚀 Overview

CharuFace is an **AI-powered dermatology assistant** that:

* 📸 Captures facial images (left, center, right)
* 🤖 Detects skin conditions using deep learning
* 🧠 Uses Retrieval-Augmented Generation (RAG) for medical reasoning
* 🌍 Adapts recommendations based on **severity + environment**
* 🛍️ Suggests **real-world skincare products** (Amazon / Flipkart)

---

## 🏗️ System Architecture

```text
User (Camera Input)
        ↓
Face Detection (Haarcascade)
        ↓
YOLO + CNN Models
        ↓
Skin Issue + Severity
        ↓
RAG Pipeline (Knowledge Base)
        ↓
LLM (Qwen via OpenRouter)
        ↓
Personalized Recommendations
        ↓
Product Enrichment (SerpAPI)
        ↓
Frontend UI (Results Page)
```

---

## 🧠 Key Features

### 🔬 AI Skin Analysis

* Multi-angle face capture (Left, Center, Right)
* YOLO-based detection + CNN classification
* Severity estimation (Mild / Moderate / Severe)

---

### 📚 RAG-Based Medical Reasoning

* Uses structured dermatology knowledge base
* Context-aware recommendations
* No hallucination (strict prompt control)

---

### 🎯 Personalized Skincare Engine

Recommendations adapt based on:

* Skin issue
* Severity level
* Skin type
* Allergies
* 🌍 Environment (climate-aware logic)

---

### 🧴 Clinical-Level Recommendations

* Ingredients with purpose (e.g. Salicylic Acid → unclogs pores)
* Step-by-step skincare routine (morning/night)
* Diet + lifestyle guidance
* Home remedies with usage instructions

---

### 🛍️ Smart Product System

* AI suggests relevant products
* Filters only skincare categories
* Fetches:

  * Product image
  * Amazon / Flipkart link
* Removes noise (food, devices, irrelevant items)

---

### ⚡ Real-Time UI Experience

* Beautiful frontend (HTML, CSS, JS)
* Camera integration
* Loading animation + AI processing screen
* Wishlist + previous recommendations

---

## 🧩 Tech Stack

### 🧠 AI / ML

* YOLOv8 (object detection)
* CNN (skin classification)
* Haarcascade (face detection)

### 📚 NLP / LLM

* OpenRouter API
* Qwen 2.5 Instruct
* RAG (FAISS + Sentence Transformers)

### 🛠 Backend

* FastAPI
* Python

### 🌐 Frontend

* HTML, CSS, JavaScript

### 🔗 External Tools

* SerpAPI (product enrichment)
* FAISS (vector search)

---

## 📂 Project Structure

```bash
AI_Dermatology/
│
├── backend/           # FastAPI routes
├── inference/         # ML pipelines (YOLO + CNN)
├── rag/               # RAG pipeline
├── services/          # Product + external APIs
├── chatbot/           # Chat assistant
├── models/            # ML models (ignored in Git)
├── templates/         # HTML pages
├── static/            # CSS, JS, images
├── memory/            # Cached results (ignored)
├── uploads/           # User images (ignored)
│
├── knowledge_base.json
├── requirements.txt
├── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repo

```bash
git clone https://github.com/your-username/charuface.git
cd charuface
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create `.env` file:

```env
OPENROUTER_API_KEY=your_key_here
SERPAPI_KEY=your_key_here
```

---

### 5️⃣ Run Server

```bash
uvicorn backend.main:app --reload
```

---

### 6️⃣ Open App

```
http://127.0.0.1:8000
```

---

## 📸 Workflow

1. Enter user details (age, skin type, concern)
2. Capture 3 face angles
3. AI analyzes skin condition
4. Generates:

   * Explanation
   * Ingredients
   * Routine
   * Diet
   * Products
5. View results with real product links

---

## 🎯 What Makes This Special

* 🔥 Combines **Computer Vision + LLM + RAG**
* 🔥 Real-world product integration (not just text)
* 🔥 Personalized + adaptive recommendations
* 🔥 Clean UI + full-stack system
* 🔥 Near **startup-level AI product**

---

## ⚠️ Disclaimer

This system provides **informational skincare guidance only** and does **not replace professional medical advice**.

---

## 🚀 Future Improvements

* 📊 Rating-based product ranking
* 🧪 Ingredient compatibility engine
* 🧠 Multi-step treatment timeline
* 🤖 Agent-based workflows (LangGraph)

---

## 👨‍💻 Author

**Chirayu Patil**
AI Engineer | Generative AI | Computer Vision

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!

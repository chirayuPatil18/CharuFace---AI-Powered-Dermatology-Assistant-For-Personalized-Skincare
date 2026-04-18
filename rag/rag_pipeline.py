import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from dotenv import load_dotenv

# LOAD ENV
load_dotenv()

# CONFIG
EMBED_MODEL = "models/all-MiniLM-L6-v2"
TOP_K = 5

PRIORITY_SECTIONS = ["ingredients", "environment", "rules", "causes"]

# OPENROUTER CLIENT
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# LOAD KB
with open("knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

texts = [item["text"] for item in knowledge_base]

# EMBEDDINGS
embedder = SentenceTransformer(EMBED_MODEL)
embeddings = embedder.encode(texts, convert_to_numpy=True)

# RETRIEVE
def retrieve(query, skin_issue=None, severity=None):
    query_embedding = embedder.encode([query])

    filtered_indices = []
    filtered_embeddings = []

    for i, item in enumerate(knowledge_base):

        if skin_issue and item["metadata"].get("skin_issue") != skin_issue:
            continue

        item_severity = item["metadata"].get("severity", "all")

        if severity:
            if item_severity not in [severity, "all"]:
                if "severity" in item["metadata"]:
                    continue

        filtered_indices.append(i)
        filtered_embeddings.append(embeddings[i])

    if len(filtered_embeddings) == 0:
        return []

    filtered_embeddings = np.array(filtered_embeddings)

    index = faiss.IndexFlatL2(filtered_embeddings.shape[1])
    index.add(filtered_embeddings)

    D, I = index.search(query_embedding, TOP_K)

    results = []
    for idx in I[0]:
        real_idx = filtered_indices[idx]
        results.append(knowledge_base[real_idx])

    results.sort(
        key=lambda x: PRIORITY_SECTIONS.index(x["metadata"]["section"])
        if x["metadata"]["section"] in PRIORITY_SECTIONS else 999
    )

    return results

# CONTEXT BUILDER
def build_context(chunks):
    context = ""
    used_sections = set()

    for chunk in chunks:
        section = chunk["metadata"]["section"]

        if section in used_sections:
            continue

        used_sections.add(section)
        context += f"\n[{section.upper()}]\n{chunk['text']}\n"

    return context


# ADVANCED PROMPT
def build_prompt(context, skin_issue, severity, user_profile, user_query):

    return f"""
You are an advanced AI skincare assistant trained on dermatology knowledge.

IMPORTANT:
- You provide HIGH-QUALITY, evidence-based skincare guidance
- You are NOT a doctor and must NOT claim to replace medical professionals
- You behave like a clinical skincare advisor (not generic AI)

STRICT RULES:
- Use ONLY provided context
- NO hallucination
- ONLY OTC products 
- All recommendations MUST be relevant to {skin_issue} and severity level ({severity})

👤 USER PROFILE:
Skin Issue: {skin_issue}
Severity: {severity}
Skin Type: {user_profile.get("skin_type")}
Allergies: {user_profile.get("allergies")}
Environment: {user_profile.get("environment")}

📚 CONTEXT:
{context}

-----------------------------------
🧠 CORE INTELLIGENCE RULES
-----------------------------------

🔥 SEVERITY ADAPTATION:
- Mild → gentle care, barrier repair
- Moderate → introduce actives
- Severe → strong targeted treatment

🌍 CLIMATE ADAPTATION (VERY IMPORTANT):
- Humid → lightweight, oil control, non-comedogenic
- Dry → hydration, ceramides, barrier repair
- Polluted → deep cleansing + antioxidants

⚠️ ALL outputs MUST adapt based on BOTH:
→ severity
→ environment

-----------------------------------
📊 OUTPUT REQUIREMENTS
-----------------------------------

1. explanation:
- Explain biological cause of {skin_issue}
- Connect with severity level

2. ingredients:
- 4–8 ingredients
- MUST change based on severity
- Include purpose
- Example: "Salicylic Acid (penetrates pores and removes excess oil)"

3. avoid:
- Specific triggers (ingredients / habits / products) or environmental factors to avoid that can worsen {skin_issue}
- Must consider skin type + severity

4. routine (CRITICAL):

- MUST change based on severity
- MUST adapt to environment
- Step-by-step clinical logic

FORMAT:
- Each step must include:
  → WHAT
  → WHY

Example:
"Use salicylic acid cleanser to unclog pores and reduce oil buildup"

RULES:
- NO generic steps
- NO objects → ONLY strings
- Mild → simple routine
- Severe → advanced treatment routine

5. diet:
- Nutrient-based (NOT generic)
- Must support skin healing
- Example: "Omega-3 fatty acids (reduce inflammation and redness)"

6. home_remedies:
- Practical + safe
- Include usage method

🛍️ PRODUCTS:
- 8–12 highly relevant skincare OTC products which can be applyed to the skin for treating {skin_issue}
- Must directly solve {skin_issue}

-----------------------------------
RETURN JSON ONLY:
-----------------------------------

{{
  "explanation": "",
  "ingredients": [],
  "avoid": [],
  "product_types": [],
  "routine": {{
    "morning": [],
    "night": []
  }},
  "home_remedies": [],
  "diet": {{
    "foods_to_eat": [],
    "foods_to_avoid": []
  }},
  "products": [
    {{
      "name": "",
      "search_query": "",
      "reason": ""
    }}
  ],
  "precautions": ""
}}

QUESTION:
{user_query}
"""

# LLM
def generate_response(prompt):
    response = client.chat.completions.create(
        model="qwen/qwen-2.5-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content

# SAFE PARSE
def safe_parse(response):
    try:
        import re
        clean = re.sub(r"```json|```", "", response).strip()
        data = json.loads(clean)

        # FIX ROUTINE FORMAT
        if "routine" in data:
            routine = data["routine"]

            if isinstance(routine, dict):
                for key in ["morning", "night"]:
                    if key in routine:
                        routine[key] = [
                            item["step"] if isinstance(item, dict) else item
                            for item in routine[key]
                        ]

            elif isinstance(routine, list):
                new_routine = {"morning": [], "night": []}

                for item in routine:
                    time = item.get("time", "").lower()
                    steps = item.get("steps", [])

                    new_routine[time] = [
                        s["step"] if isinstance(s, dict) else s
                        for s in steps
                    ]

                data["routine"] = new_routine

        return data

    except Exception as e:
        print("JSON parse error:", e)
        return {
            "error": "Invalid JSON",
            "raw": response
        }

# MAIN
def run_rag(user_query, skin_issue, severity, user_profile):
    chunks = retrieve(user_query, skin_issue, severity)
    context = build_context(chunks)

    prompt = build_prompt(
        context,
        skin_issue,
        severity,
        user_profile,
        user_query
    )

    response = generate_response(prompt)

    return safe_parse(response)
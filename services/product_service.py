import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# PRODUCT VALIDATION
VALID_KEYWORDS = [
    "cleanser", "face wash", "moisturizer",
    "cream", "lotion", "serum", "sunscreen",
    "gel", "toner", "spf"
]

INVALID_KEYWORDS = [
    "food", "potato", "diet", "juice",
    "humidifier", "machine", "device",
    "supplement", "capsule"
]


def is_valid_product(name):
    name = name.lower()

    if any(bad in name for bad in INVALID_KEYWORDS):
        return False

    return any(good in name for good in VALID_KEYWORDS)

# FETCH PRODUCT DATA
def fetch_product_data(query):
    try:
        search = GoogleSearch({
            "q": query + " buy India Amazon Flipkart",
            "tbm": "shop",
            "api_key": SERPAPI_KEY,
            "num": 5
        })

        results = search.get_dict()

        if "shopping_results" in results:

            # PRIORITY: AMAZON / FLIPKART
            for item in results["shopping_results"]:
                link = item.get("link", "").lower()

                if "amazon" in link or "flipkart" in link:
                    return {
                        "image": item.get("thumbnail"),
                        "link": item.get("link")
                    }

            # fallback to first result
            first = results["shopping_results"][0]

            return {
                "image": first.get("thumbnail"),
                "link": first.get("link")
            }

    except Exception as e:
        print("SerpAPI Error:", e)

    return {"image": None, "link": None}

# ENRICH PRODUCTS
def enrich_products(products):

    enriched = []

    for product in products:

        name = product.get("name", "")

        # FILTER INVALID PRODUCTS
        if not is_valid_product(name):
            continue

        # CLEAN QUERY
        query = f"{name} skincare India"

        data = fetch_product_data(query)

        image = data["image"] or f"https://via.placeholder.com/200?text={name}"
        link = data["link"] or f"https://www.amazon.in/s?k={name}"

        enriched.append({
            "name": name,
            "reason": product.get("reason"),
            "search_query": query,
            "image": image,
            "link": link
        })

    return enriched
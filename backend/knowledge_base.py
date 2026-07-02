import re
import pandas as pd


KNOWLEDGE_BASE_PATH = "data/processed/property_knowledge_base.csv"


def load_knowledge_base():
    return pd.read_csv(KNOWLEDGE_BASE_PATH)


def extract_listing_features(listing_text: str) -> dict:
    text = listing_text.lower()

    features = {
        "has_price": bool(re.search(r"\$|price|priced|asking", text)),
        "has_bedrooms": bool(re.search(r"\b\d+\s*(bed|beds|bedroom|bedrooms)\b", text)),
        "has_bathrooms": bool(re.search(r"\b\d+(\.\d+)?\s*(bath|baths|bathroom|bathrooms)\b", text)),
        "has_area": bool(re.search(r"\b\d+\s*(sqft|sq ft|square feet)\b", text)),
        "has_location": bool(re.search(r"\bin\b|\bnear\b|\bneighborhood\b|\bdowntown\b", text)),
        "has_garage": "garage" in text,
        "has_basement": "basement" in text,
        "has_air": "central air" in text or "air conditioning" in text or "ac" in text,
        "has_fireplace": "fireplace" in text,
        "has_deck_or_porch": "deck" in text or "porch" in text,
        "description_length": len(listing_text.split())
    }

    return features


def calculate_completeness_score(features: dict) -> int:
    score = 0

    weights = {
        "has_price": 15,
        "has_bedrooms": 15,
        "has_bathrooms": 15,
        "has_area": 15,
        "has_location": 15,
        "has_garage": 10,
        "has_basement": 5,
        "has_air": 5,
        "has_fireplace": 3,
        "has_deck_or_porch": 2
    }

    for key, weight in weights.items():
        if features.get(key):
            score += weight

    if features["description_length"] >= 40:
        score += 10
    elif features["description_length"] >= 20:
        score += 5

    return min(score, 100)


def detect_missing_fields(features: dict) -> list:
    missing = []

    required_fields = {
        "has_price": "price",
        "has_bedrooms": "bedrooms",
        "has_bathrooms": "bathrooms",
        "has_area": "square footage",
        "has_location": "location/neighborhood",
        "has_garage": "garage information",
        "has_air": "heating/cooling details",
    }

    for key, label in required_fields.items():
        if not features.get(key):
            missing.append(label)

    return missing


def get_knowledge_base_summary(kb: pd.DataFrame) -> dict:
    summary = {
        "average_price": round(kb["sale_price"].mean(), 2),
        "average_living_area_sqft": round(kb["living_area_sqft"].mean(), 2),
        "average_bedrooms": round(kb["bedrooms"].mean(), 2),
        "average_bathrooms": round(kb["bathrooms"].mean(), 2),
        "average_amenity_count": round(kb["amenity_count"].mean(), 2),
        "common_keywords": get_common_keywords(kb)
    }

    return summary


def get_common_keywords(kb: pd.DataFrame) -> list:
    keywords = []

    for item in kb["recommended_keywords"].dropna().head(100):
        keywords.extend([word.strip() for word in item.split(",") if word.strip()])

    common = pd.Series(keywords).value_counts().head(10).index.tolist()

    return common


def analyze_against_knowledge_base(listing_text: str) -> dict:
    kb = load_knowledge_base()

    extracted_features = extract_listing_features(listing_text)
    completeness_score = calculate_completeness_score(extracted_features)
    missing_fields = detect_missing_fields(extracted_features)
    kb_summary = get_knowledge_base_summary(kb)

    return {
        "extracted_features": extracted_features,
        "completeness_score": completeness_score,
        "missing_fields": missing_fields,
        "knowledge_base_summary": kb_summary
    }

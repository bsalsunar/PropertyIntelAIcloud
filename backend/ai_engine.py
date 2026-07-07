import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from knowledge_base import analyze_against_knowledge_base

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_listing_with_ai(listing_text: str) -> dict:
    kb_analysis = analyze_against_knowledge_base(listing_text)

    prompt = f"""
You are an AI real estate listing quality and SEO analyst.

Analyze the user listing using the structured knowledge base analysis.

User Listing:
{listing_text}

Knowledge Base Analysis:
{json.dumps(kb_analysis, indent=2)}

Your job:
1. Give a final quality_score from 0 to 100.
2. Give an seo_score from 0 to 100.
3. Explain the score clearly.
4. Recommend SEO keywords based on the knowledge base.
5. Suggest missing improvements.
6. Rewrite the listing into a better SEO-friendly version.

Important:
- Do not only rewrite text.
- Use the missing fields and extracted features from the knowledge base analysis.
- Return STRICT JSON only.

JSON format:
{{
  "quality_score": 0,
  "seo_score": 0,
  "completeness_score": 0,
  "missing_fields": [],
  "explanation": [],
  "seo_keywords": [],
  "improvement_suggestions": [],
  "improved_listing": ""
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    ai_result = response.choices[0].message.content

    try:
        return json.loads(ai_result)
    except json.JSONDecodeError:
        return {
            "error": "AI response was not valid JSON",
            "raw_response": ai_result,
            "knowledge_base_analysis": kb_analysis
        }

# 🏠 PropertyIntelAI

> **AI-Powered Property Listing Quality & SEO Analyzer using a Structured Real Estate Knowledge Base**

PropertyIntelAI is an end-to-end AI application that evaluates the quality and SEO readiness of real estate listings. The application combines **data engineering**, a **structured real estate knowledge base**, and **Large Language Models (LLMs)** to provide explainable insights and actionable recommendations for property listings.

Unlike applications that rely solely on text generation, PropertyIntelAI first compares a user-submitted listing against a structured knowledge base built from historical real estate data. The AI then reasons over this analysis to generate quality scores, SEO recommendations, and an optimized listing.

Live Demo

https://propertyintelaicloud-2pvbzpgjrawb9phtyk4ewn.streamlit.app/

---

<img width="1184" height="588" alt="Screenshot 2026-07-02 at 9 38 55 PM" src="https://github.com/user-attachments/assets/51af1402-20e1-42f3-8fa1-d0293ef53597" />

<img width="598" height="418" alt="Screenshot 2026-07-02 at 9 40 07 PM" src="https://github.com/user-attachments/assets/4d330e19-aef3-4252-86d5-23a18163fc9c" />

<img width="1430" height="797" alt="Screenshot 2026-07-03 at 2 16 34 PM" src="https://github.com/user-attachments/assets/56ce60f0-4d8b-4eff-bea1-c9a5c8f7ec72" />


# 📌 Problem Statement

A large number of real estate listings fail to attract potential buyers because they are incomplete, poorly structured, or not optimized for search engines.

Common issues include:

* Missing property details
* Incomplete descriptions
* Weak SEO optimization
* Lack of important amenities
* Poor readability
* Missing buyer-focused information

PropertyIntelAI helps solve these problems by automatically evaluating listings and providing intelligent recommendations before they are published.

---

# 🎯 Project Objectives

* Build a structured real estate knowledge base from historical housing data.
* Clean and transform raw housing data into meaningful engineered features.
* Compare new property listings against the knowledge base.
* Evaluate listing completeness and quality.
* Generate explainable Quality and SEO scores.
* Recommend improvements using AI.
* Provide an interactive web application for users.

---

# 🚀 Features

## 📊 Data Collection

The application uses the **Ames Housing Dataset**, which contains detailed residential property information.

Ames Housing Dataset link:
https://www.kaggle.com/datasets/sifikhaoula/ames-housing-dataset?select=AmesHousing.csv

It includes:

* Property characteristics
* Neighborhood
* House style
* Living area
* Lot size
* Bedrooms
* Bathrooms
* Garage information
* Basement information
* Property quality
* Amenities
* Sale price
* others features
---

## ⚙️ Data Engineering

The raw dataset is cleaned and transformed into a structured knowledge base.

### Data Cleaning

* Standardize column names
* Handle missing values
* Normalize categorical values
* Transform property attributes
* Remove inconsistencies

### Feature Engineering

The preprocessing pipeline generates features including:

* Property Type
* Living Area
* Bedroom Count
* Bathroom Count
* Garage Capacity
* Amenity Count
* Property Quality Label
* Completeness Score
* Recommended SEO Keywords

The processed knowledge base is stored as:

```text
data/processed/property_knowledge_base.csv
```

---

# 🧠 Knowledge Base

Instead of sending raw listings directly to an LLM, PropertyIntelAI first compares the listing with a structured knowledge base.

The knowledge base contains information about:

* Property characteristics
* Amenities
* Property quality
* Neighborhood information
* Listing completeness
* Common SEO keywords

This enables explainable and consistent evaluations.

---

# 🤖 AI Workflow

### Step 1 — User Input

The user submits a property listing.

↓

### Step 2 — Feature Extraction

The application extracts:

* Price
* Bedrooms
* Bathrooms
* Square footage
* Location
* Garage
* Basement
* Amenities

↓

### Step 3 — Knowledge Base Comparison

The listing is evaluated against the processed knowledge base.

The application determines:

* Completeness Score
* Missing Information
* Property characteristics
* Relevant SEO features

↓

### Step 4 — AI Analysis

The knowledge base analysis is passed to an LLM.

The LLM generates:

* Listing Quality Score
* SEO Score
* Missing Information
* Explanation of Scores
* SEO Keyword Suggestions
* Improvement Recommendations
* Optimized Listing Description

---

# 🏗️ System Architecture

```text
                  Raw Housing Dataset
                          │
                          ▼
          Data Cleaning & Feature Engineering
                          │
                          ▼
         Property Knowledge Base (CSV + SQLite)
                          │
                          ▼
            Knowledge Base Feature Analyzer
                          │
                          ▼
               OpenAI Large Language Model
                          │
                          ▼
                    FastAPI Backend
                          │
                          ▼
                Streamlit Web Application
```

---

# 💻 Technology Stack

### Programming

* Python

### Data Engineering

* Pandas
* NumPy

### Database

* SQLite

### Backend

* FastAPI

### Frontend

* Streamlit

### AI

* OpenAI API

### Version Control

* Git
* GitHub

---

# 📁 Project Structure

```text
PropertyIntelAI/

backend/
│── ai_engine.py
│── config.py
│── data_preprocessing.py
│── database.py
│── knowledge_base.py
│── main.py

frontend/
│── app.py

data/
│── raw/
│     └── properties.csv
│
│── processed/
│     └── property_knowledge_base.csv
│
└── realestate.db

docs/
notebooks/
tests/
screenshots/

README.md
requirements.txt
.env.example
```

---

# 🌐 API Endpoints

## GET /

Returns the API status.

---

## GET /health

Health check endpoint.

---

## POST /analyze

Analyzes a property listing.

### Example Request

```json
{
  "listing_text": "Beautiful 4-bedroom home in Ames with updated kitchen and attached garage."
}
```

### Example Response

```json
{
  "quality_score": 87,
  "seo_score": 84,
  "completeness_score": 78,
  "missing_fields": [
    "Price",
    "Square Footage"
  ],
  "seo_keywords": [
    "family home",
    "updated kitchen",
    "attached garage"
  ],
  "improvement_suggestions": [
    "Include asking price",
    "Mention total living area"
  ],
  "improved_listing": "..."
}
```

---

# 🖥️ User Interface

The Streamlit application allows users to:

* Paste a property listing
* Analyze listing quality
* View Quality Score
* View SEO Score
* View Completeness Score
* Identify missing information
* Read AI explanations
* View suggested SEO keywords
* Generate an optimized property listing

---

# ▶️ Installation

## Clone the Repository

```bash
git clone https://github.com/<your-github-username>/PropertyIntelAI.git
cd PropertyIntelAI
```

## Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configure Environment Variables

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
```

---

# ▶️ Run the Project

### Step 1 — Build the Knowledge Base

```bash
python backend/data_preprocessing.py
```

### Step 2 — Start FastAPI

```bash
uvicorn backend.main:app --reload
```

### Step 3 — Launch Streamlit

```bash
streamlit run frontend/app.py
```

---

# 📈 Future Enhancements

* Retrieval-Augmented Generation (RAG)
* Vector database integration
* Similar property recommendations
* Duplicate listing detection
* Property price estimation
* Image quality analysis
* PDF report generation
* User authentication
* Cloud deployment
* Interactive analytics dashboard

---

# 🎓 Skills Demonstrated

* Data Collection
* Data Cleaning
* Feature Engineering
* Knowledge Base Construction
* AI Prompt Engineering
* LLM Integration
* FastAPI Development
* Streamlit Development
* SQLite Database Design
* Git & GitHub
* End-to-End AI Application Development

---

# 📜 License

This project was developed for educational, research, and portfolio purposes.

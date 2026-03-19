# 🏛️ Precondition Extraction of Public Services from Greek Legislation using LLMs

### MSc Data Science Project — Legal Information Extraction Pipeline for e-Government  
📍 Author: **Vasileios Stergiopoulos**  
🎓 MSc in Data Science — School of Science & Technology  
📅 2024  

---

## 📌 Overview

Public service provision is still largely based on unstructured legal documents. Even in modern digital systems, regulations are distributed as PDF files containing eligibility criteria (preconditions) written in natural language.

This project presents an **end-to-end LLM-based pipeline** that automatically:

- Extracts legal documents from government sources  
- Processes unstructured Greek legal text  
- Identifies eligibility preconditions for public services  
- Converts them into **structured, machine-readable JSON**

The goal is to support the transition from a **document-based paradigm** to a **data-driven public service ecosystem**, enabling automation, interoperability, and advanced analytics.

---

## 🏗️ System Architecture

The pipeline consists of the following stages:

```text
Public Service IDs (CSV)
        │
        ▼
Mitos API (Metadata Retrieval)
        │
        ▼
Legal Rule PDFs
        │
        ▼
PDF Text Extraction
        │
        ▼
LLM-based Information Extraction
        │
        ▼
Structured JSON Output (Preconditions)
```

---

## 📂 Data Sources

### 🔗 Mitos Platform
- https://mitos.gov.gr/

Provides structured metadata for public services, including:
- Process IDs
- Legal references
- Associated rule documents (PDFs)

---

### 📜 Greek Government Gazette (ΦΕΚ)
- https://www.et.gr/

Contains official legal documents describing:
- Eligibility conditions
- Legal requirements
- Administrative rules

---

## ⚙️ Pipeline Components

### 1. Metadata Retrieval
- Fetches service data via Mitos API
- Extracts:
  - Legal rule URLs
  - Existing conditions (if available)

---

### 2. PDF Processing
- Downloads legal documents
- Extracts raw Greek text using PDF parsers
- Handles noisy and unstructured content

---

## 3. LLM-based Extraction

A carefully designed prompt enables the model to:

- Identify **eligibility preconditions**
- Filter out irrelevant procedural text
- Extract structured fields:
  - `text`
  - `category`
  - `applicant_type`
  - `legal_reference`
  - `confidence`

Example output:

```json
{
  "process_id": "439993",
  "preconditions": [
    {
      "text": "Ο αιτών πρέπει να είναι άνω των 18 ετών",
      "category": "age",
      "applicant_type": "αιτών",
      "legal_reference": null,
      "confidence": 0.95
    }
  ]
}
```

---

## 🧠 Prompt Engineering Strategy

The extraction process relies on a **structured prompt design** with:

- Clear definition of "precondition"
- Strict JSON output enforcement
- Category constraints
- Legal text preservation (no paraphrasing)
- Atomic condition splitting
- Hallucination prevention rules

This transforms the LLM into a **controlled Information Extraction system** rather than a generative model.

---

## 🧱 Tech Stack

- Python  
- OpenAI API (LLMs)  
- Requests (API calls)  
- PyPDF2 (PDF parsing)  
- dotenv (environment management)  

---

## 🚀 How to Run

### 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/your-repo.git
cd your-repo
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set API key 
```env
OPENAI_API_KEY=your_key_here
```

### 4. Run pipeline 
```bash
python -m app.main --limit 1
```

---

## 📊 Challenges

This project addresses several real-world challenges:

- Highly unstructured legal language
- Long and noisy PDF documents
- Multiple conditions per sentence
- Ambiguous legal phrasing
- Inconsistent document formatting

---

## 📈 Results & Observations

- LLMs can effectively extract structured legal conditions from Greek legislation
- Prompt design is critical for:
  - Accuracy
  - Consistency
  - Hallucination control
- Category classification improves downstream usability

---

## 🔬 Future Work

Several improvements can enhance this system:

### 📄 Document Chunking

Process long legal texts in segments (articles/paragraphs) to improve coverage.

### 🧪 Evaluation Framework

Create a labeled dataset and compute:

- Precision
- Recall
- F1-score

### 🧠 Few-shot Prompting

Add examples to improve extraction accuracy.

### 🌐 Web Interface

Provide a UI for uploading documents and viewing results.

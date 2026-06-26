# Resume Parser using Grok (Transformer Model)

## Overview

This project implements a Resume Parser that extracts structured information from resumes using the **Grok Large Language Model (LLM)**. The parser processes resumes in multiple formats, extracts relevant candidate information, and generates structured JSON output suitable for recruitment platforms.

The application supports **batch processing**, allowing multiple resumes to be parsed in a single execution.

---

# Requirement

Develop a robust Resume Parser capable of:

* Reading resumes in **PDF**, **DOCX**, and **DOC** formats.
* Leveraging a **Transformer Model** for information extraction.
* Returning the extracted information in **JSON** format.

---

# Supported File Formats

* `.pdf`
* `.docx`
* `.doc`

---

# Information Extracted

The parser extracts the following information whenever available:

### Contact Information

* Name
* Email
* Phone Number
* Location
* LinkedIn
* GitHub
* Website / Portfolio

### Summary

* Professional Summary

### Education

* Institution
* Degree
* Field of Study
* Graduation Year
* GPA

### Work Experience

* Company
* Position
* Start Date
* End Date
* Duration
* Description

### Skills

* Programming Languages
* Frameworks
* Tools
* Databases
* Cloud Technologies
* Technical Skills
* Soft Skills

### Certifications

* Certification Name
* Issuer
* Year

### Projects

* Project Name
* Description
* Technologies Used

### Additional Sections

* Awards
* Publications

---

# Project Structure

```text
resume_parser/
│
├── main.py
├── config.yaml
├── requirements.txt
├── README.md
│
├── modules/
│   ├── sanity_check.py
│   ├── text_extractor.py
│   └── llm_call.py
│
├── prompts/
│   ├── system_prompt.txt
│   └── user_prompt.txt
│
├── resumes/
│
└── output/
```

---

# File Description

## main.py

Application entry point.

Responsibilities:

* Load configuration
* Discover resume files
* Coordinate the parsing workflow
* Save the final JSON output

---

## config.yaml

Stores all configurable settings.

Includes:

* API Key
* Base URL
* Model Name
* Resume Folder Path
* Output Folder Path
* Processing Parameters

---

## modules/sanity_check.py

Validates resume files before processing.

Checks include:

* File existence
* Supported extension
* Maximum file size
* Read permissions

---

## modules/text_extractor.py

Extracts text from supported resume formats.

Supports:

* PDF
* DOCX
* DOC

---

## modules/llm_call.py

Handles communication with the Grok API.

Responsibilities:

* Load prompts
* Construct the final prompt
* Send requests to the LLM
* Retry failed requests
* Validate JSON responses
* Return structured data

---

## prompts/system_prompt.txt

Defines the behavior of the LLM.

Examples:

* Resume parsing instructions
* ATS extraction behavior
* Anti-hallucination rules
* JSON response requirements

---

## prompts/user_prompt.txt

Defines:

* Fields to extract
* Output JSON schema
* Parsing rules

---

## resumes/

Place all resume files inside this folder.

Example:

```text
resumes/
├── resume1.pdf
├── resume2.docx
└── resume3.doc
```

---

## output/

Stores the generated JSON results.

---

# Processing Workflow

```text
Resume Files
      │
      ▼
Sanity Check
      │
      ▼
Text Extraction
      │
      ▼
Prompt Construction
      │
      ▼
Grok LLM
      │
      ▼
JSON Validation
      │
      ▼
Save Results
```

---

# Configuration

Update the values in `config.yaml`.

Example:

```yaml
provider: grok

providers:
  grok:
    api_key: YOUR_API_KEY
    base_url: https://api.x.ai/v1
    model: llama-3.1-8b-instant
```

---

# Running the Parser

### Step 1

Place all resume files inside the `resumes/` folder.

### Step 2

Install dependencies.

```bash
pip install -r requirements.txt
```

### Step 3

Run the parser.

```bash
python main.py
```

---

# Output

After successful execution, the parser generates a JSON file inside the `output/` directory.

Example:

```json
[
  {
    "_file": "resume1.pdf",
    "_status": "success",
    "contact": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
]
```

Each JSON object represents one processed resume and follows the predefined schema.

---

# Future Improvements

* OCR support for scanned resumes
* Resume ranking
* Skill normalization
* Candidate matching
* REST API
* Web interface
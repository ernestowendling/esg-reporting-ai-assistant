# ESG Reporting AI Assistant

A grounded AI assistant for ESG reporting, regulatory analysis and controlled source-based research.

The project explores how large language models can support sustainability and financial-services professionals without relying on unsupported or untraceable answers.

## Business problem

ESG reporting teams work with complex regulatory texts, internal policies, data definitions and disclosure requirements.

Relevant information is often distributed across multiple documents, making research and interpretation time-consuming.

A general-purpose chatbot may provide a plausible response, but that response may:

* omit important context;
* rely on outdated knowledge;
* confuse similar regulatory concepts;
* provide unsupported statements;
* fail to show which source informed the answer.

This project addresses that problem through controlled document retrieval and grounded response generation.

## What the assistant does

The assistant is designed to:

1. receive an ESG or regulatory question;
2. search an approved document collection;
3. retrieve the most relevant source passages;
4. use those passages as context for the language model;
5. generate a business-oriented response;
6. retain citations or source references;
7. present the answer for human review.

## Example use cases

The assistant may support questions relating to:

* SFDR disclosures;
* principal adverse impacts;
* sustainability indicators;
* ESG data definitions;
* fund-documentation requirements;
* internal ESG policies;
* reporting methodologies;
* regulatory source comparison;
* data-quality investigations.

## Design principles

### Grounding

Responses should be based on retrieved source material rather than on unrestricted model knowledge.

### Traceability

The user should be able to identify the documents or passages supporting the response.

### Controlled scope

The assistant should answer from an approved knowledge base and state when the available material is insufficient.

### Human review

The system supports professional analysis. It does not replace legal, regulatory, compliance or investment judgement.

### Auditability

Important workflow events should be recordable, including:

* the user query;
* retrieved sources;
* model response;
* citations;
* validation results;
* processing errors.

## Workflow

```text
User question
    ↓
Document retrieval
    ↓
Relevant source passages
    ↓
Grounded LLM prompt
    ↓
Response generation
    ↓
Citation and output checks
    ↓
Human review
```

## Technology stack

* Python
* Streamlit
* Large language model APIs
* Retrieval-augmented generation
* Document parsing
* Vector or semantic retrieval
* Prompt templates
* Source citation
* Audit-trail controls

## Project structure

```text
esg-reporting-ai-assistant/
│
├── app.py
├── requirements.txt
├── README.md
│
├── ingestion/
│   └── document processing
│
├── retrieval/
│   └── search and ranking logic
│
├── generation/
│   └── prompt and response logic
│
├── validation/
│   └── output and citation checks
│
├── data/
│   └── approved sample documents
│
└── tests/
    └── retrieval and validation tests
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/esg-reporting-ai-assistant.git
cd esg-reporting-ai-assistant
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file based on `.env.example`.

```text
LLM_API_KEY=your_api_key
```

Do not commit API keys or other credentials to GitHub.

## Run the application

```bash
streamlit run app.py
```

## Testing

```bash
pytest
```

Testing should cover:

* document ingestion;
* retrieval relevance;
* empty search results;
* unsupported questions;
* citation generation;
* missing environment variables;
* malformed source documents;
* response-validation rules.

## Current limitations

This project is a prototype.

It does not provide legal, compliance or investment advice.

Its output depends on:

* the quality of the source documents;
* the accuracy of document parsing;
* the relevance of retrieved passages;
* the model and prompt configuration;
* human review of the final answer.

The assistant should state clearly when the available documents do not support a reliable response.

## Potential development

* stronger citation validation;
* source-version controls;
* regulatory-document metadata;
* document effective-date checks;
* multilingual retrieval;
* comparison of regulatory versions;
* user access controls;
* persistent query history;
* evaluation datasets;
* answer-quality scoring;
* structured ESG data integration;
* board and oversight reporting outputs.

## Why this project matters

In regulated financial services, a fluent answer is not enough.

An AI system should also demonstrate:

* where the information came from;
* whether the source was relevant;
* what the system could not establish;
* where professional review remains necessary.

This project applies that principle to ESG and regulatory reporting.

## Author

**Ernesto Wendling**

Financial-services governance and ESG professional building grounded AI and automation solutions for regulated business environments.

[LinkedIn](YOUR-LINKEDIN-URL)

---

# Python Control Lab

Applied Python exercises and business workflows focused on validation, exception handling, control evidence and operational automation.

This repository documents the development of practical Python capabilities through examples connected to real business-control problems.

It is not intended to be a collection of disconnected beginner exercises. Each component is designed to demonstrate how Python can be used to make a process more reliable, traceable or efficient.

## Objectives

The repository focuses on five areas:

* data validation;
* reusable business rules;
* exception handling;
* audit-trail generation;
* automated testing.

## Business context

Operational teams frequently rely on spreadsheets, manual checks and repeated copy-and-paste activities.

Typical control weaknesses include:

* inconsistent validation;
* undocumented decisions;
* missing exception records;
* manual calculation errors;
* unclear ownership;
* limited reproducibility.

The exercises in this repository convert selected checks into explicit and testable Python logic.

## Example modules

Depending on the current repository content, the lab may include:

### Data-quality validation

Checks for missing, duplicated, incorrectly formatted or inconsistent records.

### Business-rule validation

Applies defined rules to determine whether a record passes, fails or requires review.

### Exception management

Separates valid records from exceptions and provides an explanation for each result.

### Audit trails

Records what check was performed, when it occurred and what outcome was produced.

### File processing

Reads, transforms and exports structured data from formats such as CSV, Excel or JSON.

### API interaction

Retrieves or submits data through controlled API requests.

### Automated testing

Uses test cases to confirm that validation logic behaves as expected.

## Example workflow

```text
Input data
    ↓
Format checks
    ↓
Business-rule validation
    ↓
Pass / fail / review decision
    ↓
Exception report
    ↓
Audit evidence
```

## Repository structure

```text
diamond-python-control-lab/
│
├── README.md
├── requirements.txt
│
├── exercises/
│   └── focused Python exercises
│
├── controls/
│   └── reusable validation functions
│
├── workflows/
│   └── end-to-end business examples
│
├── data/
│   └── fictional sample data
│
├── outputs/
│   └── example reports
│
└── tests/
    └── automated test cases
```

## Technology

* Python
* Pandas
* OpenPyXL
* Requests
* Pytest
* JSON
* CSV and Excel processing
* Git and GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/diamond-python-control-lab.git
cd diamond-python-control-lab
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running an exercise

Run the relevant Python file from the repository root:

```bash
python path/to/example.py
```

Run the automated tests:

```bash
pytest
```

## Development approach

Each workflow should ideally include:

1. a clearly defined business problem;
2. fictional sample input;
3. explicit validation rules;
4. readable output;
5. exception handling;
6. automated tests;
7. a short explanation of the control benefit.

## Sample data policy

All published data should be fictional, anonymised or generated specifically for the repository.

No confidential business information, personal data, production credentials or proprietary documents should be included.

## Current limitations

The repository contains portfolio and learning implementations rather than production systems.

Some examples may use simplified datasets or local files to make the underlying logic easy to understand.

## Planned development

* additional test coverage;
* stronger type validation;
* structured logging;
* reusable configuration files;
* more complete exception reports;
* API-based workflows;
* Streamlit interfaces;
* integration with AI-assisted processes;
* SAP-oriented validation examples.

## Why this repository matters

The objective is not simply to demonstrate Python syntax.

It is to show how technical skills can be applied to business processes that require reliability, evidence and control.

That approach reflects my wider professional focus: using AI and automation to improve regulated operations without removing accountability or human oversight.

## Author

**Ernesto Wendling**

Financial-services governance and transformation professional applying Python, AI and automation to controlled business workflows.

[LinkedIn](YOUR-LINKEDIN-URL)

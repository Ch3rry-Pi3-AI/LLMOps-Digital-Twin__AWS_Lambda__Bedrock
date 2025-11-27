# 🚀 **Enhance the Digital Twin — Branch Overview**

This branch enriches the **llmops-digital-twin** backend and frontend by adding a **personal data layer**, a **dynamic contextual system prompt**, **AWS-ready memory persistence**, and optional **Markdown rendering** for more natural, expressive responses.

It also prepares the backend for **AWS Lambda deployment** in the next stage.

A full demo is shown below:

<p align="center">
  <img src="../img/demo/twin_demo.gif" width="100%" />
</p>



## Part 1: Add Personal Data for the Twin

### Step 1: Create the Data Directory

Inside the **backend** folder:

```bash
cd backend
mkdir data
```

Your directory now includes a dedicated space for structured personal information used to enrich the Digital Twin’s context.

### Step 2: Add Personal Data Files

Inside `backend/data/`, create:

**1. `facts.json`** — structured persona information
**2. `summary.txt`** — your professional summary
**3. `style.txt`** — communication guidelines
**4. `linkedin.pdf`** — exported or printed PDF of your LinkedIn profile

These files are consumed by the backend to build a natural and accurate representation of your identity.

Example (truncated):

```json
{
  "full_name": "Roger J. Campbell",
  "name": "Roger",
  "current_role": "AI / ML Consultant",
  "location": "Birmingham, UK",
  "specialties": ["Machine Learning", "LLMOps", "..."]
}
```

Summary and style files contain short descriptive text blocks defining your tone and background.



## Part 2: Create the `resources.py` Module

This module loads all persona-related data files and makes them available to the rest of the backend.

Truncated example:

```python
reader = PdfReader("./data/linkedin.pdf")
linkedin = ...
summary = open("./data/summary.txt").read()
style = open("./data/style.txt").read()
facts = json.load(open("./data/facts.json"))
```

This provides a clean, centralised data ingestion layer.



## Part 3: Build the Dynamic Context System

Create `backend/context.py`.

This file constructs the **system prompt** sent to the LLM each time the Digital Twin responds.

It uses:

* `facts.json`
* `summary.txt`
* `style.txt`
* extracted `linkedin.pdf` text
* current time
* safety and behavioural rules
* Markdown-friendly formatting

Truncated:

```python
def prompt():
    return f"""
# Your Role

You are a digital twin of {full_name}, also known as {name}.
...
Here are notes about communication style:
{style}
"""
```

This enables rich, natural, personalised responses.



## Part 4: Update Dependencies

Append to `backend/requirements.txt`:

```
boto3
pypdf
mangum
```

These support:

* S3-based memory persistence
* PDF text extraction
* AWS Lambda execution

Update your environment:

```bash
cd backend
uv add -r requirements.txt
```



## Part 5: Upgrade the Backend to Support Memory + AWS

Replace `server.py` with the AWS-ready version.

Enhancements include:

* local or S3 memory storage
* improved conversation trimming
* context-aware system prompt injection
* structured request/response models
* AWS-compatible CORS
* safe error handling

Truncated:

```python
USE_S3 = os.getenv("USE_S3") == "true"
messages = [{"role": "system", "content": prompt()}]
...
save_conversation(session_id, conversation)
```



## Part 6: Add the AWS Lambda Handler

Create `backend/lambda_handler.py`:

```python
from mangum import Mangum
from server import app
handler = Mangum(app)
```

This enables seamless deployment to AWS Lambda + API Gateway.



## Part 7: Enable Markdown Rendering in the Frontend

To allow the twin to use **bold**, **lists**, **headings**, etc., the frontend was upgraded with:

```bash
npm install react-markdown remark-gfm remark-breaks
```

### Twin component update (`components/twin.tsx`)

Assistant messages now render Markdown safely:

```tsx
<Markdown
  className="markdown-content prose prose-slate max-w-none"
  remarkPlugins={[remarkGfm, remarkBreaks]}
>
  {message.content}
</Markdown>
```

User messages still render as plain text.

### Global CSS update (`app/globals.css`)

Clean Markdown styling via Tailwind Typography:

```css
@import "tailwindcss";
@import "@tailwindcss/typography";

.markdown-content {
  @apply prose prose-slate max-w-none;
}
```

This ensures professional, readable formatting.



## Part 8: Test Locally

### Backend:

```bash
cd backend
uv run uvicorn server:app --reload
```

### Frontend:

```bash
cd frontend
npm run dev
```

Visit:

```
http://localhost:3000
```

Your Digital Twin now:

* remembers conversation history
* uses rich persona context
* renders Markdown beautifully
* is AWS Lambda ready
* is S3-compatible for production memory

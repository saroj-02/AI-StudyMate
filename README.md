
# AI StudyMate — AI-Powered Student Utility Application

AI StudyMate is a beginner-friendly AI application that helps students
understand concepts, summarize notes, improve written answers, and
practice for examinations using a Large Language Model (LLM).

The application is built with Python, Streamlit, and Google's Gemini API.

## 1. Problem Statement

Students often work with lengthy lecture notes, difficult technical
concepts, and written answers that need improvement. Preparing revision
material manually can take time, and students may need help understanding
the same concept at different levels of difficulty.

AI StudyMate provides a simple interface through which students can
submit study material and receive task-specific AI-generated assistance.

The application is designed as a focused student utility rather than
a general-purpose chatbot.

## 2. Objectives

- Integrate a real LLM API into a usable application.
- Design clear, task-specific prompts.
- Generate structured and readable educational content.
- Validate inputs before making API calls.
- Handle API errors and empty model responses.
- Keep API credentials outside the source code.
- Demonstrate a complete AI-assisted user workflow.

## 3. Features

### 3.1 Summarize Notes

Converts supplied study notes into a structured summary containing:
- Topic overview
- Key points
- Important terms
- Quick revision checklist

### 3.2 Generate Quiz

Creates multiple-choice questions from supplied study material.

Each question includes:
- Four answer options
- Correct answer
- Short explanation

Students can select between 3 and 10 questions.

### 3.3 Improve My Answer

Helps students improve their written answers by:
- Improving clarity and organization
- Correcting grammar
- Identifying missing concepts
- Highlighting possible factual issues

### 3.4 Explain Concept

Explains a topic through:
- A simple explanation
- Step-by-step working
- A practical example
- Key takeaways
- A practice question

### 3.5 Additional Usability Features

- Difficulty selection
- Input validation
- Loading indicator
- Readable Markdown output
- Download generated results
- Recent activity within the current session
- User-friendly API error messages

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| Google Gemini API | AI content generation |
| google-genai | Official Google Gen AI Python SDK |
| python-dotenv | Local environment configuration |
| Markdown | Structured output presentation |
| Git and GitHub | Version control and source hosting |

## 5. Project Structure

AI-StudyMate/
- app.py
- ai_service.py
- prompt_templates.py
- validators.py
- requirements.txt
- .env.example
- .gitignore
- README.md
- .streamlit/config.toml

## 6. Installation

### Prerequisites

- Python 3.11 or a compatible supported Python version
- pip
- Internet access
- A Gemini API key

### Step 1: Clone or create the project

If the repository already exists:

    git clone YOUR_REPOSITORY_URL
    cd AI-StudyMate

Alternatively, create the folder manually and add the supplied files.

### Step 2: Create a virtual environment

On macOS or Linux:

    python3 -m venv .venv
    source .venv/bin/activate

On Windows:

    python -m venv .venv
    .venv\Scripts\activate

### Step 3: Install dependencies

    python -m pip install --upgrade pip
    pip install -r requirements.txt

### Step 4: Obtain an API key

Visit:

https://aistudio.google.com/apikey

Create an API key according to the provider's current account,
region, and usage requirements.

### Step 5: Configure the environment

On macOS or Linux:

    cp .env.example .env

On Windows, copy `.env.example` to `.env` manually.

Edit `.env`:

    GEMINI_API_KEY=your_actual_api_key
    GEMINI_MODEL=gemini-3.8-flash

Replace the placeholder with your actual key.

Never commit `.env` to a public repository.

### Step 6: Run the application

    streamlit run app.py

Open the local URL printed by Streamlit, normally:

http://localhost:8501

## 7. Application Workflow

1. The student opens AI StudyMate.
2. The student selects a utility.
3. The student chooses a difficulty level.
4. The student enters notes, an answer, or a question.
5. The application validates the input.
6. The prompt builder creates a task-specific prompt.
7. The AI service sends the prompt to Gemini.
8. The application processes the response.
9. The result is displayed as Markdown.
10. The student can download the result.

## 8. Architecture

The project separates responsibilities into four main modules.

### app.py

Responsible for the interface, form handling, loading state, output
display, download functionality, and user-facing errors.

### validators.py

Checks input type, empty values, minimum and maximum input length,
and quiz question count.

### prompt_templates.py

Creates the instructions required for each utility and defines the
expected output format.

### ai_service.py

Initializes the API client, sends generation requests, configures
the model, and converts provider errors into understandable messages.

### Architecture flow

    Student
       |
       v
    Streamlit UI (app.py)
       |
       v
    Input Validation (validators.py)
       |
       v
    Prompt Builder (prompt_templates.py)
       |
       v
    AI Service (ai_service.py)
       |
       v
    Gemini API
       |
       v
    Response Handling
       |
       v
    Markdown Output and Download

## 9. Prompt Engineering Approach

The project uses a structured prompting strategy.

### Role

The model is instructed to act as an educational assistant.

### Task

The selected utility defines the exact operation, such as summarization,
quiz generation, answer improvement, or concept explanation.

### Context

The student's supplied content is included as data to analyze.

### Constraints

The prompt defines rules for factual accuracy, clarity, and uncertainty.

### Output Format

Each utility has a different requested structure so that the result
is readable and aligned with the student's objective.

### Example

Task: Explain Concept

Input:

Explain normalization in DBMS with a simple example.

Expected sections:

- Simple Explanation
- How It Works
- Example
- Key Takeaways
- Practice Question

The model's actual wording and correctness can vary.

## 10. Input Validation

The application checks:

- Whether the supplied content is a string
- Whether the content is empty or whitespace-only
- Whether at least three characters are supplied
- Whether the input exceeds 20,000 characters
- Whether the quiz count is between 3 and 10

Invalid inputs are rejected before an API request is made.

Input length limits reduce unnecessarily large requests, but they do
not guarantee that every request will fit the model's context window.

## 11. Error Handling

The AI service handles several failure categories.

### Missing API key

The application explains that the environment configuration is missing.

### Invalid request

The application asks the student to check the input and configuration.

### Authentication or permission failure

The application advises checking the API key and model permissions.

### Rate limits or quota exhaustion

The application advises waiting and checking the available API quota.

### Provider server errors

The application reports temporary unavailability.

### Empty model output

The application asks the student to try again with a more specific input.

### Unexpected exceptions

The application displays a generic message rather than exposing raw
provider internals to the user.

API error handling improves usability but does not replace monitoring,
logging, retries, or production observability.

## 12. Security Considerations

- API credentials are loaded from environment variables.
- The .env file is excluded from Git.
- The example environment file contains only a placeholder.
- Raw provider errors are not displayed directly.
- Student content is treated as untrusted input in prompt instructions.
- The model is not trusted to guarantee factual correctness.

The project does not implement authentication, database persistence,
formal privacy controls, or production-grade abuse prevention.

## 13. Testing Plan

Test the following scenarios manually.

| Test | Expected Result |
|---|---|
| Submit empty input | Validation warning |
| Submit spaces only | Validation warning |
| Submit one or two characters | Minimum-length warning |
| Submit valid notes | AI-generated result |
| Generate a quiz | Requested number of questions |
| Select Beginner difficulty | Beginner-oriented prompt |
| Use an invalid API key | Authentication error message |
| Exceed API quota | Quota or rate-limit message |
| Receive an empty response | Clear retry guidance |
| Download the result | Markdown file downloads |
| Submit content at the character limit | Validation accepts the length |
| Submit content beyond the limit | Input is rejected |

Actual results should be recorded during testing. Do not report tests
as passed unless you have executed them.

## 14. Limitations

- Model responses can contain factual errors.
- Quiz answer keys can occasionally be incorrect.
- Output formatting is not perfectly deterministic.
- API availability and quotas depend on the provider and account.
- The current history exists only within the Streamlit session.
- There is no permanent database or user account system.
- The application processes text input rather than uploading files.
- The basic error handler does not implement automatic retries.

## 15. Future Enhancements

- PDF and DOCX note upload
- Persistent study history using MongoDB
- User authentication
- Flashcards and spaced repetition
- Interactive quizzes with score calculation
- Retrieval-Augmented Generation (RAG)
- Source-grounded answers
- Automated unit tests
- API usage monitoring and rate limiting
- Deployment with securely configured environment variables

## 16. Conclusion

AI StudyMate demonstrates the fundamentals of beginner-level AI
application engineering. It combines a usable interface, structured
prompts, LLM API integration, input validation, error handling, and
readable output into a practical educational workflow.

The primary objective is to demonstrate a working AI feature that
addresses a real student need, rather than making isolated API calls.

## 17. Acknowledgments

- Google Gemini API
- Google Gen AI Python SDK
- Streamlit
- Python

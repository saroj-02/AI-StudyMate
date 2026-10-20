
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from prompt_templates import build_prompt

load_dotenv()

DEFAULT_MODEL = "gemini-3.8-flash"


def get_client() -> genai.Client:
    """Create the Gemini client using a secret API key."""

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "Gemini API key is missing. Add GEMINI_API_KEY "
            "to your .env file and restart the application."
        )

    return genai.Client(api_key=api_key)


def generate_study_output(
    task: str,
    content: str,
    level: str = "Beginner",
    question_count: int = 5,
) -> str:
    """Generate a result for one of the student utilities."""

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip()

    if not model:
        model = DEFAULT_MODEL

    prompt = build_prompt(
        task=task,
        content=content,
        level=level,
        question_count=question_count,
    )

    client = get_client()

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=4096,
                system_instruction=(
                    "You are AI StudyMate, an educational assistant. "
                    "Follow the task instructions and return clear, "
                    "accurate, student-friendly Markdown."
                ),
            ),
        )

        result = response.text

        if not result or not result.strip():
            raise RuntimeError(
                "The model returned an empty response. "
                "Try again with a more specific input."
            )

        return result.strip()

    except errors.APIError as exc:
        status = getattr(exc, "code", None)

        if status == 400:
            raise RuntimeError(
                "The request was rejected. Check your input and "
                "the selected model configuration."
            ) from exc

        if status == 401 or status == 403:
            raise RuntimeError(
                "The API key may be invalid or may not have "
                "permission to use this model."
            ) from exc

        if status == 404:
            raise RuntimeError(
                f"The Gemini model '{model}' is unavailable for this API key. "
                "Set GEMINI_MODEL to a model that supports generateContent; "
                "the Gemini API recommended gemini-3.8-flash for this key."
            ) from exc

        if status == 429:
            raise RuntimeError(
                "The API rate limit or quota was reached. "
                "Wait before trying again, and check your API quota."
            ) from exc

        if status is not None and status >= 500:
            raise RuntimeError(
                "The AI provider is temporarily unavailable. "
                "Please try again later."
            ) from exc

        if isinstance(status, int):
            message = (
                f"The Gemini API request failed with HTTP {status}. "
                "Check your model and API configuration, then try again."
            )
        else:
            message = (
                "The Gemini API request failed. Check your model and API "
                "configuration, then try again."
            )

        raise RuntimeError(message) from exc

    except TimeoutError as exc:
        raise RuntimeError(
            "The request timed out. Try again with shorter content."
        ) from exc

    except ValueError:
        # Preserve the useful configuration error from get_client().
        raise

    except RuntimeError:
        raise

    except Exception as exc:
        # Do not expose raw provider internals to the user.
        raise RuntimeError(
            "An unexpected error occurred while generating the "
            "study output. Please try again."
        ) from exc

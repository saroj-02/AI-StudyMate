
MAX_INPUT_CHARS = 20000
MIN_INPUT_CHARS = 3


def validate_text(text: str) -> tuple[bool, str]:
    """Validate text supplied by the student."""

    if not isinstance(text, str):
        return False, "Input must be text."

    cleaned_text = text.strip()

    if not cleaned_text:
        return False, "Please enter some text before generating."

    if len(cleaned_text) < MIN_INPUT_CHARS:
        return False, "Please enter at least 3 characters."

    if len(cleaned_text) > MAX_INPUT_CHARS:
        return (
            False,
            f"Input is too long. Maximum allowed is "
            f"{MAX_INPUT_CHARS:,} characters."
        )

    return True, cleaned_text


def validate_quiz_count(count: int) -> tuple[bool, str]:
    """Validate the requested number of quiz questions."""

    if not isinstance(count, int) or isinstance(count, bool):
        return False, "Question count must be an integer."

    if not 3 <= count <= 10:
        return False, "Choose between 3 and 10 questions."

    return True, ""

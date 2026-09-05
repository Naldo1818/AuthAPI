import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    LLM_MODEL,
    LLM_TIMEOUT,
    LLM_STUB,
)

router = APIRouter(prefix="/ai", tags=["AI"])


class TriageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class TriageResponse(BaseModel):
    category: Literal["billing", "bug", "feature", "other"]
    urgency: Literal["low", "normal", "high"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str


PROMPT_PATH = Path(__file__).parent / "prompts" / "triage-v1.md"


def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def parse_json_output(raw_output: str) -> dict:
    """
    Parse JSON returned by the LLM.

    Handles:
    - normal JSON
    - JSON inside markdown code fences
    - extra text surrounding JSON
    """

    raw_output = raw_output.strip()

    # Remove markdown code fences
    if raw_output.startswith("```"):
        lines = raw_output.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        raw_output = "\n".join(lines).strip()

    # Try normal JSON first
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON object from surrounding text
    start = raw_output.find("{")
    end = raw_output.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output.")

    extracted = raw_output[start:end + 1]

    return json.loads(extracted)


def quarantine_failure(
    input_text: str,
    raw_output: str,
    error: str,
):
    """
    Save failed model output for debugging.
    """

    log_path = Path("logs/quarantine.jsonl")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "input": input_text,
        "raw_output": raw_output,
        "error": error,
        "prompt_version": "triage-v1",
        "model": LLM_MODEL,
    }

    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def call_gemini(client, system_prompt: str, user_message: str):
    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            response_mime_type="application/json",
        ),
    )

    return response.text


@router.post("/triage", response_model=TriageResponse)
def triage_message(request: TriageRequest):

    # Development stub
    if LLM_STUB == "1":
        return TriageResponse(
            category="other",
            urgency="normal",
            confidence=0.50,
            reason="Stub response used while the AI integration is being built."
        )

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    system_prompt = load_prompt()

    user_message = json.dumps(
        {
            "customer_message": request.text
        },
        ensure_ascii=False
    )

    # -----------------------------
    # First model attempt
    # -----------------------------

    try:
        raw_output = call_gemini(
            client,
            system_prompt,
            user_message
        )

        parsed = parse_json_output(raw_output)

        result = TriageResponse.model_validate(parsed)

        return result

    except Exception as first_error:

        # -----------------------------
        # One repair attempt
        # -----------------------------

        repair_prompt = f"""
The previous model response was invalid.

Validation/parsing error:
{str(first_error)}

Return ONLY valid JSON matching this exact schema:

{{
  "category": "billing | bug | feature | other",
  "urgency": "low | normal | high",
  "confidence": 0.0,
  "reason": "one short sentence"
}}

Rules:
- category must be billing, bug, feature, or other
- urgency must be low, normal, or high
- confidence must be between 0 and 1
- reason must be one short sentence
- do not add extra fields
- do not use markdown
"""

        try:
            repaired_output = call_gemini(
                client,
                repair_prompt,
                user_message
            )

            repaired_parsed = parse_json_output(
                repaired_output
            )

            repaired_result = TriageResponse.model_validate(
                repaired_parsed
            )

            return repaired_result

        except Exception as second_error:

            quarantine_failure(
                input_text=request.text,
                raw_output=raw_output,
                error=str(second_error),
            )

            raise HTTPException(
                status_code=422,
                detail="The AI response could not be validated."
            )
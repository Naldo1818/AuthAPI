import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

router = APIRouter(prefix="/ai", tags=["AI"])

class TriageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

class TriageResponse(BaseModel):
    category: Literal["billing", "bug", "feature", "other"]
    urgency: Literal["low", "normal", "high"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str

@router.post("/triage", response_model=TriageResponse)
async def triage_message(request: TriageRequest):
    llm_stub = os.getenv("LLM_STUB", "1")

    if llm_stub == "1":
        return TriageResponse(
            category="other",
            urgency="normal",
            confidence=0.50,
            reason="Stub response used while the AI integration is being built."
        )

    # Real LLM integration
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("LLM_MODEL", "openrouter/free")
    timeout = int(os.getenv("LLM_TIMEOUT", "30"))

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenRouter API key not configured."
        )

    prompt = f"""Triage this support message:
"{request.text}"

Respond in JSON only:
{{
    "category": "billing|bug|feature|other",
    "urgency": "low|normal|high",
    "confidence": 0.0-1.0,
    "reason": "brief explanation"
}}"""

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Parse LLM response (you'll need to add JSON extraction)
            # For now, return a basic response
            return TriageResponse(
                category="other",
                urgency="normal",
                confidence=0.75,
                reason="Processed by OpenRouter"
            )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LLM service timeout")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")
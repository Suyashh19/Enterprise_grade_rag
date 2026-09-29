import logfire
from portkey_ai import Portkey, createHeaders, PORTKEY_GATEWAY_URL
from langchain_openai import ChatOpenAI

from app.config import settings


# Production gateway config is saved in the Portkey dashboard
# and attached as the DEFAULT config of PORTKEY_API_KEY.
#
# Dashboard config:
#   - Fallback: @rag/<GROQ_MODEL> -> @brag/<GROQ_FAST_MODEL>
#   - Cache: simple mode
#   - Retry: 2 attempts on 429 / 503
#
# Do NOT send an inline config from code because the workspace
# blocks inline configs and the API key uses its dashboard config.

portkey_client = Portkey(
    api_key=settings.PORTKEY_API_KEY,
    virtual_key=settings.GROQ_SLUG
)


def get_langchain_llm(feature: str = "rag") -> ChatOpenAI:
    """
    Returns a Portkey-backed ChatOpenAI.

    Portkey exposes an OpenAI-compatible gateway.
    The model uses the Portkey provider slug:

        @rag/openai/gpt-oss-120b

    The provider header tells Portkey which provider integration
    should handle the request.
    """

    return ChatOpenAI(
        api_key=settings.PORTKEY_API_KEY,
        base_url=PORTKEY_GATEWAY_URL,

        # Primary Portkey model
        model=settings.GROQ_MODEL,

        temperature=0,

        default_headers=createHeaders(
            api_key=settings.PORTKEY_API_KEY,

            # REQUIRED:
            # Send virtual_key to trigger Saved Integration fallback
            virtual_key=settings.GROQ_SLUG,

            metadata={
                "feature": feature,
                "_user": "rag-system",
                "environment": "production"
            }
        )
    )


def extract_cache_status(response) -> str:
    """
    Pull x-portkey-cache-status from the Portkey native client response.
    Tries multiple attribute paths defensively.
    Returns 'MISS' if not found.
    """

    for attr in ("_raw_response", "_response", "_http_response"):
        raw = getattr(response, attr, None)

        if raw is not None:
            status = getattr(raw, "headers", {}).get(
                "x-portkey-cache-status",
                ""
            )

            if status:
                return status.upper()

    return "MISS"
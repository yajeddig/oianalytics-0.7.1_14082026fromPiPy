from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .. import _credentials
from .. import endpoints

__all__ = [
    "LlmMessage",
    "LlmContentBlock",
    "LlmUsage",
    "LlmResponse",
    "create_llm_message",
]

MessageRole = Literal["user", "assistant"]


class LlmContentBlock(BaseModel):
    type: Literal["text"] = "text"
    text: str


class LlmMessage(BaseModel):
    role: MessageRole
    content: List[LlmContentBlock]


class LlmUsage(BaseModel):
    model_config = {"populate_by_name": True}

    input_tokens: int = Field(alias="inputTokens")
    output_tokens: int = Field(alias="outputTokens")


class LlmResponse(BaseModel):
    model_config = {"populate_by_name": True}

    created: datetime
    model: str
    output: List[LlmContentBlock]
    stop_reason: str = Field(alias="stopReason")
    usage: LlmUsage

    @property
    def text(self) -> str:
        return self.output[0].text


def create_llm_message(
    prompt: str,
    instructions: Optional[str] = None,
    history: Optional[List[LlmMessage]] = None,
    max_tokens: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> LlmResponse:
    """
    Send a user prompt and receive the LLM reply.

    Parameters
    ----------
    prompt : str
        The user message to send.
    instructions : str, optional
        System-level instructions for the model.
    history : list of LlmMessage, optional
        Prior turns to include for multi-turn conversations.
    max_tokens : int, optional
        Maximum number of tokens to generate.
    api_credentials : OIAnalyticsAPICredentials, optional
        Credentials. Defaults to global credentials if None.

    Returns
    -------
    LlmResponse
        Parsed response. Access the reply text via ``.text``.

    Examples
    --------
    >>> reply = create_llm_message("What is the capital of France?")
    >>> print(reply.text)
    Paris

    >>> reply = create_llm_message(
    ...     "Summarise this data.",
    ...     instructions="You are a concise industrial data analyst.",
    ... )
    """
    messages: List[dict] = []
    if history:
        messages.extend(m.model_dump() for m in history)
    messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

    raw = endpoints.llm.create_llm_message(
        messages=messages,
        instructions=instructions,
        max_tokens=max_tokens,
        api_credentials=api_credentials,
    )
    return LlmResponse(
        created=raw["created"],
        model=raw["model"],
        output=[LlmContentBlock(**block) for block in raw["output"]],
        stopReason=raw["stopReason"],
        usage=LlmUsage(**raw["usage"]),
    )

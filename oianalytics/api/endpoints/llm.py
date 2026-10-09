from typing import List, Optional


from .. import _credentials

__all__ = ["create_llm_message"]


def create_llm_message(
    messages: List[dict],
    instructions: Optional[str] = None,
    max_tokens: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    POST /api/oianalytics/llm/messages

    Parameters
    ----------
    messages : list of dict
        List of ``{"role": ..., "content": [...]}`` dicts. Roles: user, assistant.
        Each content item is ``{"type": "text", "text": "..."}``.
    instructions : str, optional
        System-level instructions for the model.
    max_tokens : int, optional
        Maximum tokens to generate.
    api_credentials : OIAnalyticsAPICredentials, optional
        Credentials. Defaults to global credentials if None.

    Returns
    -------
    dict
        Raw API response with keys: created, model, output, stopReason, usage.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    body: dict = {"messages": messages}
    if instructions is not None:
        body["instructions"] = instructions
    if max_tokens is not None:
        body["maxTokens"] = max_tokens

    response = _credentials.SESSION.post(
        url=f"{api_credentials.base_url}/api/oianalytics/llm/messages",
        json=body,
        **api_credentials.auth_kwargs,
    )
    response.raise_for_status()
    return response.json()

from typing import Optional, Any

from pydantic import BaseModel

__all__ = [
    "ResourceFile",
]


class ResourceFile(BaseModel):
    """
    Describes a binary resource file to attach to an event or a batch through a
    resource column/DataFrame passed to create_or_update_events / create_or_update_batches.

    Attributes
    ----------
    file_name : str, optional
        The name of the file to upload. If None, the server manages naming.
    content : Any
        The content of the file to upload (str, bytes, io.StringIO or io.BytesIO).
    """

    file_name: Optional[str] = None
    content: Any

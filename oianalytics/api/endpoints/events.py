from typing import Optional, Union, List
from datetime import datetime
import io


from .. import _credentials
from .. import utils

__all__ = [
    "get_event_types",
    "get_event_type_details",
    "create_event_type",
    "update_event_type",
    "get_single_event",
    "get_events",
    "delete_event",
    "set_event_binary_resource",
]


def get_event_types(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/event-types"
    response = _credentials.SESSION.get(
        url=url,
        params={
            "page": page,
            "size": page_size,
        },
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def get_event_type_details(
    event_type_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}"
    response = _credentials.SESSION.get(url=url, **api_credentials.auth_kwargs)

    # Output
    response.raise_for_status()
    return response.json()


def get_single_event(
    event_type_id: str,
    event_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}/events/{event_id}"
    response = _credentials.SESSION.get(
        url=url,
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def create_event_type(
    name: str,
    asset_type_ids: List[str],
    tag_keys: List[dict],
    tag_context: List[dict],
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:

    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/event-types"
    response = _credentials.SESSION.post(
        url=url,
        json={
            "name": name,
            "assetTypeIds": asset_type_ids,
            "tagKeys": tag_keys,
            "tagContext": tag_context,
        },
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def update_event_type(
    event_type_id: str,
    name: str,
    asset_type_ids: List[str],
    tag_keys: List[dict],
    tag_context: List[dict],
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Update an existing event type.

    Parameters
    ----------
    event_type_id : str
        The OIAnalytics ID of the event type to update.
    name : str
        The name of the event type to create.
    asset_type_ids : list of str
        The IDs of the types of asset that can fire this type of event.
    tag_keys : list of dict
        The array of source tag keys to create on the event type.
    tag_context : list of dict
        The array of tag access to attach to the event type to restrict access of users.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        Status Code.
    """

    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}"
    response = _credentials.SESSION.put(
        url=url,
        json={
            "name": name,
            "assetTypeIds": asset_type_ids,
            "tagKeys": tag_keys,
            "tagContext": tag_context,
        },
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.status_code


def get_events(
    event_type_id: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    description: Optional[str] = None,
    features_value_ids: Optional[Union[str, List[str]]] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Format dates
    start_date_iso = utils.get_zulu_isoformat(start_date)
    end_date_iso = utils.get_zulu_isoformat(end_date)

    # Query endpoint
    url = (
        f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}/events"
    )
    response = _credentials.SESSION.get(
        url=url,
        params={
            "start": start_date_iso,
            "end": end_date_iso,
            "description": description,
            "feature-values": features_value_ids,
            "page": page,
            "size": page_size,
        },
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def delete_event(
    event_type_id: str,
    event_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}/events/{event_id}"
    response = _credentials.SESSION.delete(
        url=url,
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.status_code


def set_event_binary_resource(
    event_type_id: str,
    event_id: str,
    descriptor_id: str,
    file_name: Optional[str],
    content: Union[str, bytes, io.StringIO, io.BytesIO],
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Upload a binary resource file to an existing event.

    Parameters
    ----------
    event_type_id : str
        The OIAnalytics ID of the event type the event belongs to.
    event_id : str
        The OIAnalytics ID of the event to upload the binary resource to. Must be an existing event id.
    descriptor_id : str
        The OIAnalytics ID of the binary resource descriptor defined on the event type.
    file_name : str, optional
        The name of the file to upload. If None, the server manages naming.
    content : str | bytes | io.StringIO | io.BytesIO
        The content of the file to upload.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        Status Code.
    """

    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = (
        f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}"
        f"/events/{event_id}/binary-resource/{descriptor_id}"
    )
    response = _credentials.SESSION.put(
        url=url,
        files={"file": (file_name or "", content)},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def create_or_update_events(
    event_type_id: str,
    events: List[dict],
    create_upload_event: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/event-types/{event_type_id}/events/create-or-update"
    response = _credentials.SESSION.post(
        url=url,
        json=events,
        params={"create-upload-event": create_upload_event},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()

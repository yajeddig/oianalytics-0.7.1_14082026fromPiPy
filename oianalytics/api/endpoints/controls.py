from typing import Optional, List


from .. import _credentials

__all__ = [
    # Controls
    "list_controls",
    "get_control",
    "create_control",
    "update_control",
    "delete_control",
    "get_control_values",
    # Control labels
    "list_control_labels",
    "get_control_label",
    "create_control_label",
    "update_control_label",
    "delete_control_label",
    # Control limit designs
    "list_control_limit_designs",
    "get_control_limit_design",
    "create_control_limit_design",
    "update_control_limit_design",
    "delete_control_limit_design",
    # Control limits
    "list_control_limits",
    "get_control_limits",
    "create_control_limits",
    "update_control_limits",
    "delete_control_limits",
    # Control rules
    "list_control_rules",
    "get_control_rule",
    "create_control_rule",
    "update_control_rule",
    "delete_control_rule",
    # Control contexts
    "list_control_contexts",
    "get_control_context",
    "create_control_context",
    "update_control_context",
    "delete_control_context",
    # Control condition blocks
    "list_control_condition_blocks",
    "get_control_condition_block",
    "create_control_condition_block",
    "update_control_condition_block",
    "delete_control_condition_block",
]


# ─────────────────────────────────────────────────────────────────────────────
# Controls
# ─────────────────────────────────────────────────────────────────────────────


def list_controls(
    text: Optional[str] = None,
    page: int = 0,
    page_size: int = 20,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    List controls by page.

    Parameters
    ----------
    text : str, optional
        Text to filter controls by name. Defaults to empty string (returns all).
    page : int, default 0
        The page to retrieve.
    page_size : int, default 20
        The size of one page.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary containing the paginated controls response with keys:
        - content: List of controls, each with id, name, tagContext, unit, data,
          batchStructure, context, contextualizedLimits, noContextLimits, labels,
          applicableConditions, rules
        - size: Size of the page
        - number: Page number
        - totalElements: Total number of controls matching the provided parameters
        - totalPages: Total number of pages
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/controls"
    response = _credentials.SESSION.get(
        url=url,
        params={"text": text, "page": page, "size": page_size},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def get_control(
    control_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Retrieve a control by its ID.

    Parameters
    ----------
    control_id : str
        The OIAnalytics ID of the control to retrieve.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary representing the control. The 'type' field is a discriminator
        indicating the concrete control type:
        - 'time-numeric-univariate': time-series control on numeric data
        - 'multi-batch-numeric-univariate': batch-level control on numeric data
        - 'inside-batch-time-numeric-univariate': time-series control inside a batch
        - 'asset-time-numeric-univariate': asset-linked time-series control
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/controls/{control_id}"
    response = _credentials.SESSION.get(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.json()


def create_control(
    control_type: str,
    name: str,
    unit_id: str,
    tag_context: Optional[List[dict]] = None,
    batch_structure_id: Optional[str] = None,
    data_id: Optional[str] = None,
    context_id: Optional[str] = None,
    no_context_limits_id: Optional[str] = None,
    label_ids: Optional[List[str]] = None,
    applicable_condition_block_ids: Optional[List[str]] = None,
    rule_ids: Optional[List[str]] = None,
    contextualized_limits: Optional[List[dict]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Create a new control.

    Parameters
    ----------
    control_type : str
        The type of the control. One of 'time-numeric-univariate',
        'multi-batch-numeric-univariate', 'inside-batch-time-numeric-univariate',
        or 'asset-time-numeric-univariate'.
    name : str
        The name of the control.
    unit_id : str
        The OIAnalytics ID of the unit of measurement.
    tag_context : list of dict, optional
        Tag access context. Each element is a TagAccessCommand dict with keys
        'tagKeyId' (str) and 'accessibleTagValueIds' (list of str).
    batch_structure_id : str, optional
        The OIAnalytics ID of the batch structure. Required for
        'multi-batch-numeric-univariate' and 'inside-batch-time-numeric-univariate' types.
    data_id : str, optional
        The OIAnalytics ID of the monitored data. Required for 'time-numeric-univariate',
        'multi-batch-numeric-univariate', and 'inside-batch-time-numeric-univariate' types.
    context_id : str, optional
        The OIAnalytics ID of the ControlContext providing contextual limits.
    no_context_limits_id : str, optional
        The OIAnalytics ID of the default control limits applied when no context matches.
    label_ids : list of str, optional
        OIAnalytics IDs of control labels to attach to the control.
    applicable_condition_block_ids : list of str, optional
        OIAnalytics IDs of the applicable condition blocks.
    rule_ids : list of str, optional
        OIAnalytics IDs of the control rules to apply.
    contextualized_limits : list of dict, optional
        Contextualized limits per condition block. Each element is a dict with keys
        'conditionBlockId' (str) and 'limitsId' (str).
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        The created control as a dictionary.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/controls"
    response = _credentials.SESSION.post(
        url=url,
        json={
            "type": control_type,
            "name": name,
            "unitId": unit_id,
            "tagContext": tag_context or [],
            "batchStructureId": batch_structure_id,
            "dataId": data_id,
            "contextId": context_id,
            "noContextLimitsId": no_context_limits_id,
            "labelIds": label_ids or [],
            "applicableConditionBlockIds": applicable_condition_block_ids or [],
            "ruleIds": rule_ids or [],
            "contextualizedLimits": contextualized_limits or [],
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def update_control(
    control_id: str,
    control_type: str,
    name: str,
    unit_id: str,
    tag_context: Optional[List[dict]] = None,
    batch_structure_id: Optional[str] = None,
    data_id: Optional[str] = None,
    context_id: Optional[str] = None,
    no_context_limits_id: Optional[str] = None,
    label_ids: Optional[List[str]] = None,
    applicable_condition_block_ids: Optional[List[str]] = None,
    rule_ids: Optional[List[str]] = None,
    contextualized_limits: Optional[List[dict]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Update an existing control.

    Parameters
    ----------
    control_id : str
        The OIAnalytics ID of the control to update.
    control_type : str
        The type of the control. One of 'time-numeric-univariate',
        'multi-batch-numeric-univariate', 'inside-batch-time-numeric-univariate',
        or 'asset-time-numeric-univariate'.
    name : str
        The name of the control.
    unit_id : str
        The OIAnalytics ID of the unit of measurement.
    tag_context : list of dict, optional
        Tag access context. Each element is a TagAccessCommand dict with keys
        'tagKeyId' (str) and 'accessibleTagValueIds' (list of str).
    batch_structure_id : str, optional
        The OIAnalytics ID of the batch structure. Required for
        'multi-batch-numeric-univariate' and 'inside-batch-time-numeric-univariate' types.
    data_id : str, optional
        The OIAnalytics ID of the monitored data. Required for 'time-numeric-univariate',
        'multi-batch-numeric-univariate', and 'inside-batch-time-numeric-univariate' types.
    context_id : str, optional
        The OIAnalytics ID of the ControlContext.
    no_context_limits_id : str, optional
        The OIAnalytics ID of the default control limits.
    label_ids : list of str, optional
        OIAnalytics IDs of control labels to attach.
    applicable_condition_block_ids : list of str, optional
        OIAnalytics IDs of the applicable condition blocks.
    rule_ids : list of str, optional
        OIAnalytics IDs of the control rules to apply.
    contextualized_limits : list of dict, optional
        Contextualized limits per condition block.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/controls/{control_id}"
    response = _credentials.SESSION.put(
        url=url,
        json={
            "type": control_type,
            "name": name,
            "unitId": unit_id,
            "tagContext": tag_context or [],
            "batchStructureId": batch_structure_id,
            "dataId": data_id,
            "contextId": context_id,
            "noContextLimitsId": no_context_limits_id,
            "labelIds": label_ids or [],
            "applicableConditionBlockIds": applicable_condition_block_ids or [],
            "ruleIds": rule_ids or [],
            "contextualizedLimits": contextualized_limits or [],
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def delete_control(
    control_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete a control by its ID.

    Parameters
    ----------
    control_id : str
        The OIAnalytics ID of the control to delete.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/controls/{control_id}"
    response = _credentials.SESSION.delete(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.status_code


def get_control_values(
    control_id: str,
    query: dict,
    return_uncontrolled_points: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Query the time-series values for a control over a given time, batch or asset-time context.

    Parameters
    ----------
    control_id : str
        The OIAnalytics ID of the control.
    query : dict
        A polymorphic ControlValueQuery object. The 'type' field determines the query context:

        - 'time-context-control-value-query': time-based context, requires keys:
          'start' (ISO 8601 str), 'end' (ISO 8601 str), 'timezone' (e.g. 'Europe/Paris')

        - 'batch-context-control-value-query': batch-based context, requires keys:
          'start', 'end', 'timezone', 'batchStructureId' (str), 'batchId' (str)

        - 'asset-time-context-control-value-query': asset-linked time context, requires keys:
          'start', 'end', 'timezone', 'assetId' (str)

    return_uncontrolled_points : bool, default False
        If True, includes points where control could not be performed.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary containing the control result with keys:
        - type: discriminator of the concrete result type
        - interval: the time interval covered (start, end)
        - timestamps: list of ISO 8601 timestamps for each control point
        - values: list of control values (or null when control is not possible)
        - colors: list of hex colors for the most severe violated rule at each point
        - reasonsForNoControl: list of reasons why a point could not be controlled
        - violatedControlRuleIds: list of violated rule ID lists at each point
        - ranges: list of colored limit ranges
        - limitLines: limit line values at each timestamp
        - indicators: computed statistical indicators
        - batchNames: batch names at each control point (multi-batch type only)
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/controls/{control_id}/values"
    response = _credentials.SESSION.post(
        url=url,
        json=query,
        params={"returnUncontrolledPoints": return_uncontrolled_points},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


# ─────────────────────────────────────────────────────────────────────────────
# Control labels
# ─────────────────────────────────────────────────────────────────────────────


def list_control_labels(
    text: Optional[str] = None,
    page: int = 0,
    page_size: int = 20,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    List control labels by page.

    Parameters
    ----------
    text : str, optional
        Text to filter control labels by name. Defaults to empty string (returns all).
    page : int, default 0
        The page to retrieve.
    page_size : int, default 20
        The size of one page.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary containing the paginated control labels response with keys:
        - content: List of control labels, each with id, label (name), and color (hex)
        - size: Size of the page
        - number: Page number
        - totalElements: Total number of control labels matching the provided parameters
        - totalPages: Total number of pages
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-labels"
    response = _credentials.SESSION.get(
        url=url,
        params={"text": text, "page": page, "size": page_size},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def get_control_label(
    control_label_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Retrieve a control label by its ID.

    Parameters
    ----------
    control_label_id : str
        The OIAnalytics ID of the control label to retrieve.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary representing the control label with keys:
        - id: the OIAnalytics ID
        - label: the name of the control label
        - color: the hex color (e.g. '#FF0000')
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = (
        f"{api_credentials.base_url}/api/oianalytics/control-labels/{control_label_id}"
    )
    response = _credentials.SESSION.get(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.json()


def create_control_label(
    label: str,
    color: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Create a new control label.

    Parameters
    ----------
    label : str
        The name of the control label.
    color : str
        The color of the control label in hex format (e.g. '#FF0000').
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        The created control label as a dictionary with keys id, label, and color.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-labels"
    response = _credentials.SESSION.post(
        url=url,
        json={"label": label, "color": color},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def update_control_label(
    control_label_id: str,
    label: str,
    color: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Update an existing control label.

    Parameters
    ----------
    control_label_id : str
        The OIAnalytics ID of the control label to update.
    label : str
        The updated name of the control label.
    color : str
        The updated color of the control label in hex format (e.g. '#FF0000').
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = (
        f"{api_credentials.base_url}/api/oianalytics/control-labels/{control_label_id}"
    )
    response = _credentials.SESSION.put(
        url=url,
        json={"label": label, "color": color},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def delete_control_label(
    control_label_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete a control label by its ID.

    Parameters
    ----------
    control_label_id : str
        The OIAnalytics ID of the control label to delete.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = (
        f"{api_credentials.base_url}/api/oianalytics/control-labels/{control_label_id}"
    )
    response = _credentials.SESSION.delete(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.status_code


# ─────────────────────────────────────────────────────────────────────────────
# Control limit designs
# ─────────────────────────────────────────────────────────────────────────────


def list_control_limit_designs(
    text: Optional[str] = None,
    page: int = 0,
    page_size: int = 20,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    List control limit designs by page.

    Parameters
    ----------
    text : str, optional
        Text to filter designs by name. Defaults to empty string (returns all).
    page : int, default 0
        The page to retrieve.
    page_size : int, default 20
        The size of one page.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary containing the paginated control limit designs response with keys:
        - content: List of designs, each with id, name, defaultDesign, and one
          LimitDesign object per limit slot (inferiorLimit3, inferiorLimit2,
          inferiorLimit1, target, superiorLimit1, superiorLimit2, superiorLimit3).
          Each LimitDesign has 'zone' (with 'color') and 'line' (with 'width', 'style',
          'color') sub-objects.
        - size: Size of the page
        - number: Page number
        - totalElements: Total number of designs matching the provided parameters
        - totalPages: Total number of pages
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-limit-designs"
    response = _credentials.SESSION.get(
        url=url,
        params={"text": text, "page": page, "size": page_size},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def get_control_limit_design(
    control_limit_design_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Retrieve a control limit design by its ID.

    Parameters
    ----------
    control_limit_design_id : str
        The OIAnalytics ID of the control limit design to retrieve.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary representing the control limit design with keys: id, name,
        defaultDesign, and one LimitDesign object per limit slot (inferiorLimit3,
        inferiorLimit2, inferiorLimit1, target, superiorLimit1, superiorLimit2,
        superiorLimit3). Each LimitDesign has 'zone' and 'line' sub-objects.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-limit-designs/{control_limit_design_id}"
    response = _credentials.SESSION.get(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.json()


def create_control_limit_design(
    name: str,
    default_design: bool,
    design: dict,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Create a new named control limit design.

    Parameters
    ----------
    name : str
        The name of the control limit design.
    default_design : bool
        Whether this design should be the default.
    design : dict
        The visual design for each of the 7 control limit slots. Keys are:
        'inferiorLimit3', 'inferiorLimit2', 'inferiorLimit1', 'target',
        'superiorLimit1', 'superiorLimit2', 'superiorLimit3'. Each value is a
        LimitDesign dict with optional 'zone' (dict with 'color' str) and 'line'
        (dict with 'width' int, 'style' str, 'color' str) sub-objects.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        The created control limit design as a dictionary.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-limit-designs"
    response = _credentials.SESSION.post(
        url=url,
        json={"name": name, "defaultDesign": default_design, "design": design},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def update_control_limit_design(
    control_limit_design_id: str,
    name: str,
    default_design: bool,
    design: dict,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Update an existing control limit design.

    Parameters
    ----------
    control_limit_design_id : str
        The OIAnalytics ID of the control limit design to update.
    name : str
        The updated name of the control limit design.
    default_design : bool
        Whether this design should be the default.
    design : dict
        The updated visual design for each of the 7 control limit slots. Keys are:
        'inferiorLimit3', 'inferiorLimit2', 'inferiorLimit1', 'target',
        'superiorLimit1', 'superiorLimit2', 'superiorLimit3'. Each value is a
        LimitDesign dict with optional 'zone' and 'line' sub-objects.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-limit-designs/{control_limit_design_id}"
    response = _credentials.SESSION.put(
        url=url,
        json={"name": name, "defaultDesign": default_design, "design": design},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def delete_control_limit_design(
    control_limit_design_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete a control limit design by its ID.

    Parameters
    ----------
    control_limit_design_id : str
        The OIAnalytics ID of the control limit design to delete.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-limit-designs/{control_limit_design_id}"
    response = _credentials.SESSION.delete(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.status_code


# ─────────────────────────────────────────────────────────────────────────────
# Control limits
# ─────────────────────────────────────────────────────────────────────────────


def list_control_limits(
    text: Optional[str] = None,
    page: int = 0,
    page_size: int = 20,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    List control limits by page.

    Parameters
    ----------
    text : str, optional
        Text to filter control limits by name. Defaults to empty string (returns all).
    page : int, default 0
        The page to retrieve.
    page_size : int, default 20
        The size of one page.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary containing the paginated control limits response with keys:
        - content: List of control limits, each with id, name, type, controlCount,
          currentApplicableLimits, measurement, unit, design, tagContext, timedLimits,
          labels, and assetType
        - size: Size of the page
        - number: Page number
        - totalElements: Total number of control limits matching the provided parameters
        - totalPages: Total number of pages
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-limits"
    response = _credentials.SESSION.get(
        url=url,
        params={"text": text, "page": page, "size": page_size},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def get_control_limits(
    control_limits_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Retrieve control limits by their ID.

    Parameters
    ----------
    control_limits_id : str
        The OIAnalytics ID of the control limits to retrieve.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary representing the control limits with keys: id, name, type,
        controlCount, currentApplicableLimits, measurement, unit, design, tagContext,
        timedLimits, labels, and assetType. The 'type' is one of 'fixed-limits',
        'data-limits', 'profiled-limits', 'asset-type-static-data-limits', or
        'asset-type-numeric-data-limits'.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = (
        f"{api_credentials.base_url}/api/oianalytics/control-limits/{control_limits_id}"
    )
    response = _credentials.SESSION.get(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.json()


def create_control_limits(
    name: str,
    measurement_id: str,
    unit_id: str,
    limits_type: str,
    timed_limits: List[dict],
    asset_type_id: Optional[str] = None,
    named_design_id: Optional[str] = None,
    tag_context: Optional[List[dict]] = None,
    label_ids: Optional[List[str]] = None,
    design: Optional[dict] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Create new control limits with at least one timed limits definition.

    Parameters
    ----------
    name : str
        The name of the control limits.
    measurement_id : str
        The OIAnalytics ID of the measurement.
    unit_id : str
        The OIAnalytics ID of the unit.
    limits_type : str
        The type of the control limits. One of 'fixed-limits', 'data-limits',
        'profiled-limits', 'asset-type-static-data-limits', or
        'asset-type-numeric-data-limits'.
    timed_limits : list of dict
        At least one timed limits definition. Each element is a ControlTimedLimitsCommand
        dict with keys 'applicableFrom' (ISO 8601 str), 'applicableUntil' (ISO 8601 str
        or null), and 'limitsDefinition' (dict). The 'limitsDefinition' has a 'type' key
        plus the numeric limit values (inferiorLimit3, inferiorLimit2, inferiorLimit1,
        target, superiorLimit1, superiorLimit2, superiorLimit3), which can be null.
    asset_type_id : str, optional
        The OIAnalytics ID of the asset type. Required for 'asset-type-static-data-limits'
        and 'asset-type-numeric-data-limits' types.
    named_design_id : str, optional
        The OIAnalytics ID of a named control limit design. Mutually exclusive with
        the 'design' parameter.
    tag_context : list of dict, optional
        Tag access context. Each element is a TagAccessCommand dict with keys
        'tagKeyId' (str) and 'accessibleTagValueIds' (list of str).
    label_ids : list of str, optional
        The OIAnalytics IDs of control labels to attach to these limits.
    design : dict, optional
        An inline design definition (mutually exclusive with named_design_id). Dict with
        keys for each limit slot (inferiorLimit3, ..., superiorLimit3), each a LimitDesign
        dict with optional 'zone' and 'line' sub-objects.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        The created control limits as a dictionary.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-limits"
    response = _credentials.SESSION.post(
        url=url,
        json={
            "name": name,
            "measurementId": measurement_id,
            "unitId": unit_id,
            "type": limits_type,
            "assetTypeId": asset_type_id,
            "namedDesignId": named_design_id,
            "tagContext": tag_context or [],
            "labelIds": label_ids or [],
            "design": design,
            "timedLimits": timed_limits,
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def update_control_limits(
    control_limits_id: str,
    name: str,
    measurement_id: str,
    unit_id: str,
    limits_type: str,
    timed_limits: List[dict],
    asset_type_id: Optional[str] = None,
    named_design_id: Optional[str] = None,
    tag_context: Optional[List[dict]] = None,
    label_ids: Optional[List[str]] = None,
    design: Optional[dict] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Update existing control limits.

    Parameters
    ----------
    control_limits_id : str
        The OIAnalytics ID of the control limits to update.
    name : str
        The name of the control limits.
    measurement_id : str
        The OIAnalytics ID of the measurement.
    unit_id : str
        The OIAnalytics ID of the unit.
    limits_type : str
        The type of the control limits. One of 'fixed-limits', 'data-limits',
        'profiled-limits', 'asset-type-static-data-limits', or
        'asset-type-numeric-data-limits'.
    timed_limits : list of dict
        At least one timed limits definition. Each element is a ControlTimedLimitsCommand
        dict with keys 'applicableFrom', 'applicableUntil', and 'limitsDefinition'.
    asset_type_id : str, optional
        The OIAnalytics ID of the asset type. Required for asset-type-based limits.
    named_design_id : str, optional
        The OIAnalytics ID of a named control limit design. Mutually exclusive with
        the 'design' parameter.
    tag_context : list of dict, optional
        Tag access context. Each element is a TagAccessCommand dict with keys
        'tagKeyId' (str) and 'accessibleTagValueIds' (list of str).
    label_ids : list of str, optional
        The OIAnalytics IDs of control labels to attach to these limits.
    design : dict, optional
        An inline design definition (mutually exclusive with named_design_id).
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = (
        f"{api_credentials.base_url}/api/oianalytics/control-limits/{control_limits_id}"
    )
    response = _credentials.SESSION.put(
        url=url,
        json={
            "name": name,
            "measurementId": measurement_id,
            "unitId": unit_id,
            "type": limits_type,
            "assetTypeId": asset_type_id,
            "namedDesignId": named_design_id,
            "tagContext": tag_context or [],
            "labelIds": label_ids or [],
            "design": design,
            "timedLimits": timed_limits,
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def delete_control_limits(
    control_limits_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete control limits by their ID.

    Parameters
    ----------
    control_limits_id : str
        The OIAnalytics ID of the control limits to delete.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = (
        f"{api_credentials.base_url}/api/oianalytics/control-limits/{control_limits_id}"
    )
    response = _credentials.SESSION.delete(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.status_code


# ─────────────────────────────────────────────────────────────────────────────
# Control rules
# ─────────────────────────────────────────────────────────────────────────────


def list_control_rules(
    text: Optional[str] = None,
    page: int = 0,
    page_size: int = 20,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    List control rules by page.

    Parameters
    ----------
    text : str, optional
        Text to filter rules by name. Defaults to empty string (returns all).
    page : int, default 0
        The page to retrieve.
    page_size : int, default 20
        The size of one page.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary containing the paginated control rules response with keys:
        - content: List of control rules, each with id, name, type, threshold,
          sampleSize, and color
        - size: Size of the page
        - number: Page number
        - totalElements: Total number of control rules matching the provided parameters
        - totalPages: Total number of pages
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-rules"
    response = _credentials.SESSION.get(
        url=url,
        params={"text": text, "page": page, "size": page_size},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def get_control_rule(
    control_rule_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Retrieve a control rule by its ID.

    Parameters
    ----------
    control_rule_id : str
        The OIAnalytics ID of the control rule to retrieve.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary representing the control rule with keys: id, name, type,
        threshold, sampleSize, and color. The 'type' is one of:
        'OUT_OF_LIMIT_3', 'N_OUT_OF_S_OUT_OF_LIMIT_3', 'OUT_OF_LIMIT_2',
        'N_OUT_OF_S_OUT_OF_LIMIT_2', 'OUT_OF_LIMIT_1', 'N_OUT_OF_S_OUT_OF_LIMIT_1',
        'SAME_SIDE_OF_TARGET', or 'SAME_DIRECTION'.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-rules/{control_rule_id}"
    response = _credentials.SESSION.get(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.json()


def create_control_rule(
    name: str,
    rule_type: str,
    threshold: int,
    sample_size: int,
    color: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Create a new control rule.

    Parameters
    ----------
    name : str
        The name of the control rule.
    rule_type : str
        The type of the control rule. One of:
        'OUT_OF_LIMIT_3', 'N_OUT_OF_S_OUT_OF_LIMIT_3', 'OUT_OF_LIMIT_2',
        'N_OUT_OF_S_OUT_OF_LIMIT_2', 'OUT_OF_LIMIT_1', 'N_OUT_OF_S_OUT_OF_LIMIT_1',
        'SAME_SIDE_OF_TARGET', or 'SAME_DIRECTION'.
    threshold : int
        Number of consecutive points triggering the rule (N). Minimum: 1.
    sample_size : int
        Sample window size (S) for 'N_OUT_OF_S_*' rule types. Minimum: 1.
    color : str
        Hex color used to highlight points violating this rule (e.g. '#FF0000').
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        The created control rule as a dictionary.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-rules"
    response = _credentials.SESSION.post(
        url=url,
        json={
            "name": name,
            "type": rule_type,
            "threshold": threshold,
            "sampleSize": sample_size,
            "color": color,
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def update_control_rule(
    control_rule_id: str,
    name: str,
    rule_type: str,
    threshold: int,
    sample_size: int,
    color: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Update an existing control rule.

    Parameters
    ----------
    control_rule_id : str
        The OIAnalytics ID of the control rule to update.
    name : str
        The updated name of the control rule.
    rule_type : str
        The updated type of the control rule. One of:
        'OUT_OF_LIMIT_3', 'N_OUT_OF_S_OUT_OF_LIMIT_3', 'OUT_OF_LIMIT_2',
        'N_OUT_OF_S_OUT_OF_LIMIT_2', 'OUT_OF_LIMIT_1', 'N_OUT_OF_S_OUT_OF_LIMIT_1',
        'SAME_SIDE_OF_TARGET', or 'SAME_DIRECTION'.
    threshold : int
        Number of consecutive points triggering the rule (N). Minimum: 1.
    sample_size : int
        Sample window size (S) for 'N_OUT_OF_S_*' rule types. Minimum: 1.
    color : str
        Hex color used to highlight violating points (e.g. '#FF0000').
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-rules/{control_rule_id}"
    response = _credentials.SESSION.put(
        url=url,
        json={
            "name": name,
            "type": rule_type,
            "threshold": threshold,
            "sampleSize": sample_size,
            "color": color,
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def delete_control_rule(
    control_rule_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete a control rule by its ID.

    Parameters
    ----------
    control_rule_id : str
        The OIAnalytics ID of the control rule to delete.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-rules/{control_rule_id}"
    response = _credentials.SESSION.delete(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.status_code


# ─────────────────────────────────────────────────────────────────────────────
# Control contexts
# ─────────────────────────────────────────────────────────────────────────────


def list_control_contexts(
    text: Optional[str] = None,
    page: int = 0,
    page_size: int = 20,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    List control contexts by page.

    Parameters
    ----------
    text : str, optional
        Text to filter contexts by name. Defaults to empty string (returns all).
    page : int, default 0
        The page to retrieve.
    page_size : int, default 20
        The size of one page.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary containing the paginated control contexts response with keys:
        - content: List of control contexts, each with id, name, type, tagContext,
          batchStructure, assetType, and conditionBlocks
        - size: Size of the page
        - number: Page number
        - totalElements: Total number of control contexts matching the provided parameters
        - totalPages: Total number of pages
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-contexts"
    response = _credentials.SESSION.get(
        url=url,
        params={"text": text, "page": page, "size": page_size},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def get_control_context(
    control_context_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Retrieve a control context by its ID.

    Parameters
    ----------
    control_context_id : str
        The OIAnalytics ID of the control context to retrieve.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary representing the control context with keys: id, name, type,
        tagContext, batchStructure, assetType, and conditionBlocks. The 'type' is
        one of 'BATCH', 'TEMPORAL', or 'ASSET'.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-contexts/{control_context_id}"
    response = _credentials.SESSION.get(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.json()


def create_control_context(
    name: str,
    context_type: str,
    condition_block_ids: List[str],
    batch_structure_id: Optional[str] = None,
    asset_type_id: Optional[str] = None,
    tag_context: Optional[List[dict]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Create a new control context.

    A control context groups one or more condition blocks and is linked to a control
    to provide contextual (condition-dependent) limit sets.

    Parameters
    ----------
    name : str
        The name of the control context.
    context_type : str
        The context type. One of 'TEMPORAL', 'BATCH', or 'ASSET'.
    condition_block_ids : list of str
        Ordered list of OIAnalytics IDs of the ControlConditionBlock objects to include.
        At least one is required.
    batch_structure_id : str, optional
        The OIAnalytics ID of the batch structure. Required when context_type is 'BATCH'.
    asset_type_id : str, optional
        The OIAnalytics ID of the asset type. Required when context_type is 'ASSET'.
    tag_context : list of dict, optional
        Tag access context. Each element is a TagAccessCommand dict with keys
        'tagKeyId' (str) and 'accessibleTagValueIds' (list of str).
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        The created control context as a dictionary.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-contexts"
    response = _credentials.SESSION.post(
        url=url,
        json={
            "name": name,
            "type": context_type,
            "batchStructureId": batch_structure_id,
            "assetTypeId": asset_type_id,
            "tagContext": tag_context or [],
            "conditionBlockIds": condition_block_ids,
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def update_control_context(
    control_context_id: str,
    name: str,
    context_type: str,
    condition_block_ids: List[str],
    batch_structure_id: Optional[str] = None,
    asset_type_id: Optional[str] = None,
    tag_context: Optional[List[dict]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Update an existing control context.

    Parameters
    ----------
    control_context_id : str
        The OIAnalytics ID of the control context to update.
    name : str
        The updated name of the control context.
    context_type : str
        The context type. One of 'TEMPORAL', 'BATCH', or 'ASSET'.
    condition_block_ids : list of str
        Updated ordered list of OIAnalytics IDs of the ControlConditionBlock objects.
        At least one is required.
    batch_structure_id : str, optional
        The OIAnalytics ID of the batch structure. Required when context_type is 'BATCH'.
    asset_type_id : str, optional
        The OIAnalytics ID of the asset type. Required when context_type is 'ASSET'.
    tag_context : list of dict, optional
        Tag access context. Each element is a TagAccessCommand dict with keys
        'tagKeyId' (str) and 'accessibleTagValueIds' (list of str).
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-contexts/{control_context_id}"
    response = _credentials.SESSION.put(
        url=url,
        json={
            "name": name,
            "type": context_type,
            "batchStructureId": batch_structure_id,
            "assetTypeId": asset_type_id,
            "tagContext": tag_context or [],
            "conditionBlockIds": condition_block_ids,
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def delete_control_context(
    control_context_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete a control context by its ID.

    Parameters
    ----------
    control_context_id : str
        The OIAnalytics ID of the control context to delete.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-contexts/{control_context_id}"
    response = _credentials.SESSION.delete(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.status_code


# ─────────────────────────────────────────────────────────────────────────────
# Control condition blocks
# ─────────────────────────────────────────────────────────────────────────────


def list_control_condition_blocks(
    text: Optional[str] = None,
    page: int = 0,
    page_size: int = 20,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    List control condition blocks by page.

    Parameters
    ----------
    text : str, optional
        Text to filter blocks by name. Defaults to empty string (returns all).
    page : int, default 0
        The page to retrieve.
    page_size : int, default 20
        The size of one page.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary containing the paginated control condition blocks response with keys:
        - content: List of blocks, each with id, name, contextType, tagContext,
          batchStructure, assetType, and conditions
        - size: Size of the page
        - number: Page number
        - totalElements: Total number of blocks matching the provided parameters
        - totalPages: Total number of pages
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-condition-blocks"
    response = _credentials.SESSION.get(
        url=url,
        params={"text": text, "page": page, "size": page_size},
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def get_control_condition_block(
    control_condition_block_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Retrieve a control condition block by its ID.

    Parameters
    ----------
    control_condition_block_id : str
        The OIAnalytics ID of the control condition block to retrieve.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        A dictionary representing the condition block with keys: id, name, contextType,
        tagContext, batchStructure, assetType, and conditions. Each condition has a
        'type' discriminator — one of 'time-numeric-control-condition',
        'time-string-control-condition', 'batch-numeric-control-condition',
        'batch-tag-control-condition', or 'asset-numeric-control-condition'.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-condition-blocks/{control_condition_block_id}"
    response = _credentials.SESSION.get(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.json()


def create_control_condition_block(
    name: str,
    context_type: str,
    conditions: Optional[List[dict]] = None,
    batch_structure_id: Optional[str] = None,
    asset_type_id: Optional[str] = None,
    tag_context: Optional[List[dict]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    """
    Create a new control condition block.

    A condition block is a named group of conditions (e.g. "temperature > 35°C") that
    can be referenced by a control context to define when specific limit sets apply.

    Parameters
    ----------
    name : str
        The name of the control condition block.
    context_type : str
        The context type. One of 'TEMPORAL', 'BATCH', or 'ASSET'.
    conditions : list of dict, optional
        The conditions inside this block. Each element is a ControlConditionCommand dict
        whose shape depends on the 'type' discriminator:

        - 'time-numeric-control-condition': time-series numeric condition, fields:
          'dataId' (str), 'unitId' (str), 'minValue' (float|None), 'maxValue' (float|None)

        - 'time-string-control-condition': time-series string condition, fields:
          'dataId' (str), 'acceptableValues' (list of str, at least one required)

        - 'batch-numeric-control-condition': batch numeric condition, fields:
          'dataId' (str), 'unitId' (str), 'minValue' (float|None), 'maxValue' (float|None)

        - 'batch-tag-control-condition': batch tag condition, fields:
          'batchTagKeyId' (str), 'acceptableTagValueIds' (list of str),
          'includeNullValues' (bool)

        - 'asset-numeric-control-condition': asset numeric condition, fields:
          'dataId' (str), 'unitId' (str), 'minValue' (float|None), 'maxValue' (float|None)

    batch_structure_id : str, optional
        The OIAnalytics ID of the batch structure. Required when context_type is 'BATCH'.
    asset_type_id : str, optional
        The OIAnalytics ID of the asset type. Required when context_type is 'ASSET'.
    tag_context : list of dict, optional
        Tag access context. Each element is a TagAccessCommand dict with keys
        'tagKeyId' (str) and 'accessibleTagValueIds' (list of str).
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    dict
        The created control condition block as a dictionary.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-condition-blocks"
    response = _credentials.SESSION.post(
        url=url,
        json={
            "name": name,
            "contextType": context_type,
            "batchStructureId": batch_structure_id,
            "assetTypeId": asset_type_id,
            "tagContext": tag_context or [],
            "conditions": conditions or [],
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.json()


def update_control_condition_block(
    control_condition_block_id: str,
    name: str,
    context_type: str,
    conditions: Optional[List[dict]] = None,
    batch_structure_id: Optional[str] = None,
    asset_type_id: Optional[str] = None,
    tag_context: Optional[List[dict]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Update an existing control condition block.

    Parameters
    ----------
    control_condition_block_id : str
        The OIAnalytics ID of the control condition block to update.
    name : str
        The updated name of the control condition block.
    context_type : str
        The context type. One of 'TEMPORAL', 'BATCH', or 'ASSET'.
    conditions : list of dict, optional
        The updated conditions inside this block. Each element is a
        ControlConditionCommand dict — see create_control_condition_block for the
        full description of each condition type.
    batch_structure_id : str, optional
        The OIAnalytics ID of the batch structure. Required when context_type is 'BATCH'.
    asset_type_id : str, optional
        The OIAnalytics ID of the asset type. Required when context_type is 'ASSET'.
    tag_context : list of dict, optional
        Tag access context. Each element is a TagAccessCommand dict with keys
        'tagKeyId' (str) and 'accessibleTagValueIds' (list of str).
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-condition-blocks/{control_condition_block_id}"
    response = _credentials.SESSION.put(
        url=url,
        json={
            "name": name,
            "contextType": context_type,
            "batchStructureId": batch_structure_id,
            "assetTypeId": asset_type_id,
            "tagContext": tag_context or [],
            "conditions": conditions or [],
        },
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def delete_control_condition_block(
    control_condition_block_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete a control condition block by its ID.

    Parameters
    ----------
    control_condition_block_id : str
        The OIAnalytics ID of the control condition block to delete.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        HTTP status code (204 on success).
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    url = f"{api_credentials.base_url}/api/oianalytics/control-condition-blocks/{control_condition_block_id}"
    response = _credentials.SESSION.delete(url=url, **api_credentials.auth_kwargs)

    response.raise_for_status()
    return response.status_code

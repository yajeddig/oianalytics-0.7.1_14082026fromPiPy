"""
Unified controls SDK — typed Pydantic models and functions for all
control-related OIAnalytics API resources.

Each resource exposes:
    list_<resource>(...)               -> pd.DataFrame
    get_<resource>(id)                 -> <ResponseModel>
    create_<resource>(command)         -> <ResponseModel>
    update_<resource>(id, command)     -> None
    delete_<resource>(id)              -> None
"""

from typing import Annotated, Any, List, Literal, Optional, Union

import pandas as pd
from pydantic import BaseModel, Field

from .. import _credentials
from .. import endpoints
from .. import utils
from .tags import TagKey, TagValue, TagAccess, TagAccessCommand
from .quantities import Quantity, Unit, UnitFamily
from .measurements import Measurement
from .data import DataLight
from .assets import AssetTypeLight, AssetTypeStaticDataLight, AssetTypeDataLight
from .batches import BatchTypeLight

# ─────────────────────────────────────────────────────────────────────────────
# Shared design models
# ─────────────────────────────────────────────────────────────────────────────

DashStyle = Literal["Solid", "ShortDash", "Dash", "ShortDot", "Dot"]


class LimitZone(BaseModel):
    color: str


class LimitLine(BaseModel):
    width: int
    style: DashStyle
    color: str


class LimitSlot(BaseModel):
    zone: Optional[LimitZone] = None
    line: Optional[LimitLine] = None


class LimitSlots(BaseModel):
    """Visual design for the 7 limit slots of a control limit design."""

    inferiorLimit3: Optional[LimitSlot] = None
    inferiorLimit2: Optional[LimitSlot] = None
    inferiorLimit1: Optional[LimitSlot] = None
    target: Optional[LimitSlot] = None
    superiorLimit1: Optional[LimitSlot] = None
    superiorLimit2: Optional[LimitSlot] = None
    superiorLimit3: Optional[LimitSlot] = None


# ─────────────────────────────────────────────────────────────────────────────
# Control labels — models
# ─────────────────────────────────────────────────────────────────────────────


class ControlLabelCommand(BaseModel):
    label: str
    color: str


class ControlLabel(BaseModel):
    id: str
    label: str
    color: str


# ─────────────────────────────────────────────────────────────────────────────
# Control labels — functions
# ─────────────────────────────────────────────────────────────────────────────


def list_control_labels(
    text: Optional[str] = None,
    page: int = 0,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List control labels. Returns a DataFrame indexed by id with columns: label, color.

    Parameters
    ----------
    text : str, optional
        Filter by name.
    page : int, default 0
        Page to retrieve. Ignored when get_all_pages is True.
    page_size : int, optional
        Page size. Ignored when get_all_pages is True unless explicitly set, in which case
        it is used instead of the default of 10000.
    get_all_pages : bool, default True
        Fetch all pages automatically.
    multithread_pages : bool, default False
        Fetch pages concurrently when getting all pages.
    api_credentials : OIAnalyticsAPICredentials, optional
        Credentials. Defaults to global credentials if None.
    """
    if get_all_pages:
        page = 0
        if page_size is None:
            page_size = 10000

    def _get(page_num):
        return endpoints.controls.list_control_labels(
            text=text,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def _parse(r):
        df = pd.DataFrame(r["content"])
        if df.empty:
            df = pd.DataFrame(columns=["id", "label", "color"])
        return df.set_index("id")

    return utils.concat_pages_to_dataframe(
        getter=_get,
        parser=_parse,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )


def get_control_label(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlLabel:
    """
    Retrieve a control label by its ID.

    Parameters
    ----------
    id : str
        OIAnalytics ID of the control label.
    api_credentials : OIAnalyticsAPICredentials, optional
        Credentials. Defaults to global credentials if None.

    Returns
    -------
    ControlLabel
    """
    return ControlLabel.model_validate(
        endpoints.controls.get_control_label(id, api_credentials=api_credentials)
    )


def create_control_label(
    command: ControlLabelCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlLabel:
    """
    Create a new control label.

    Parameters
    ----------
    command : ControlLabelCommand
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlLabel
    """
    return ControlLabel.model_validate(
        endpoints.controls.create_control_label(
            label=command.label, color=command.color, api_credentials=api_credentials
        )
    )


def update_control_label(
    id: str,
    command: ControlLabelCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Update an existing control label.

    Parameters
    ----------
    id : str
    command : ControlLabelCommand
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.update_control_label(
        control_label_id=id,
        label=command.label,
        color=command.color,
        api_credentials=api_credentials,
    )


def delete_control_label(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Delete a control label by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.delete_control_label(
        control_label_id=id, api_credentials=api_credentials
    )


# ─────────────────────────────────────────────────────────────────────────────
# Control limit designs — models
# ─────────────────────────────────────────────────────────────────────────────


class ControlLimitDesignCommand(BaseModel):
    name: str
    defaultDesign: bool
    design: LimitSlots


class ControlLimitDesign(BaseModel):
    type: Literal["named"] = "named"
    id: str
    name: str
    defaultDesign: bool
    inferiorLimit3: Optional[LimitSlot] = None
    inferiorLimit2: Optional[LimitSlot] = None
    inferiorLimit1: Optional[LimitSlot] = None
    target: Optional[LimitSlot] = None
    superiorLimit1: Optional[LimitSlot] = None
    superiorLimit2: Optional[LimitSlot] = None
    superiorLimit3: Optional[LimitSlot] = None


# ─────────────────────────────────────────────────────────────────────────────
# Control limit designs — functions
# ─────────────────────────────────────────────────────────────────────────────


def list_control_limit_designs(
    text: Optional[str] = None,
    page: int = 0,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List control limit designs. Returns a DataFrame indexed by id.

    Parameters
    ----------
    text : str, optional
        Filter by name.
    page : int, default 0
    page_size : int, optional
    get_all_pages : bool, default True
    multithread_pages : bool, default False
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    if get_all_pages:
        page = 0
        if page_size is None:
            page_size = 10000

    def _get(page_num):
        return endpoints.controls.list_control_limit_designs(
            text=text,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def _parse(r):
        df = pd.DataFrame(r["content"])
        if df.empty:
            df = pd.DataFrame(columns=["id", "name", "defaultDesign"])
        return df.set_index("id")

    return utils.concat_pages_to_dataframe(
        getter=_get,
        parser=_parse,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )


def get_control_limit_design(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlLimitDesign:
    """
    Retrieve a control limit design by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlLimitDesign
    """
    return ControlLimitDesign.model_validate(
        endpoints.controls.get_control_limit_design(id, api_credentials=api_credentials)
    )


def create_control_limit_design(
    command: ControlLimitDesignCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlLimitDesign:
    """
    Create a new named control limit design.

    Parameters
    ----------
    command : ControlLimitDesignCommand
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlLimitDesign
    """
    return ControlLimitDesign.model_validate(
        endpoints.controls.create_control_limit_design(
            name=command.name,
            default_design=command.defaultDesign,
            design=command.design.model_dump(exclude_none=True),
            api_credentials=api_credentials,
        )
    )


def update_control_limit_design(
    id: str,
    command: ControlLimitDesignCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Update an existing control limit design.

    Parameters
    ----------
    id : str
    command : ControlLimitDesignCommand
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.update_control_limit_design(
        control_limit_design_id=id,
        name=command.name,
        default_design=command.defaultDesign,
        design=command.design.model_dump(exclude_none=True),
        api_credentials=api_credentials,
    )


def delete_control_limit_design(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Delete a control limit design by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.delete_control_limit_design(
        control_limit_design_id=id, api_credentials=api_credentials
    )


# ─────────────────────────────────────────────────────────────────────────────
# Control rules — models
# ─────────────────────────────────────────────────────────────────────────────


class ControlRuleCommand(BaseModel):
    name: str
    type: str
    threshold: int
    sampleSize: int
    color: str


class ControlRule(BaseModel):
    id: str
    name: str
    type: str
    threshold: int
    sampleSize: int
    color: str


# ─────────────────────────────────────────────────────────────────────────────
# Control rules — functions
# ─────────────────────────────────────────────────────────────────────────────


def list_control_rules(
    text: Optional[str] = None,
    page: int = 0,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List control rules. Returns a DataFrame indexed by id with columns:
    name, type, threshold, sampleSize, color.

    Parameters
    ----------
    text : str, optional
        Filter by name.
    page : int, default 0
    page_size : int, optional
    get_all_pages : bool, default True
    multithread_pages : bool, default False
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    if get_all_pages:
        page = 0
        if page_size is None:
            page_size = 10000

    def _get(page_num):
        return endpoints.controls.list_control_rules(
            text=text,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def _parse(r):
        df = pd.DataFrame(r["content"])
        if df.empty:
            df = pd.DataFrame(
                columns=["id", "name", "type", "threshold", "sampleSize", "color"]
            )
        return df.set_index("id")

    return utils.concat_pages_to_dataframe(
        getter=_get,
        parser=_parse,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )


def get_control_rule(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlRule:
    """
    Retrieve a control rule by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlRule
    """
    return ControlRule.model_validate(
        endpoints.controls.get_control_rule(id, api_credentials=api_credentials)
    )


def create_control_rule(
    command: ControlRuleCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlRule:
    """
    Create a new control rule.

    Parameters
    ----------
    command : ControlRuleCommand
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlRule
    """
    return ControlRule.model_validate(
        endpoints.controls.create_control_rule(
            name=command.name,
            rule_type=command.type,
            threshold=command.threshold,
            sample_size=command.sampleSize,
            color=command.color,
            api_credentials=api_credentials,
        )
    )


def update_control_rule(
    id: str,
    command: ControlRuleCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Update an existing control rule.

    Parameters
    ----------
    id : str
    command : ControlRuleCommand
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.update_control_rule(
        control_rule_id=id,
        name=command.name,
        rule_type=command.type,
        threshold=command.threshold,
        sample_size=command.sampleSize,
        color=command.color,
        api_credentials=api_credentials,
    )


def delete_control_rule(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Delete a control rule by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.delete_control_rule(
        control_rule_id=id, api_credentials=api_credentials
    )


# ─────────────────────────────────────────────────────────────────────────────
# Control limits — models
# ─────────────────────────────────────────────────────────────────────────────


class FixedLimitsDefinitionCommand(BaseModel):
    """
    Limit values expressed as fixed numeric thresholds in the control unit.

    Use when limits are constant over time and do not depend on external data
    or asset properties.  All 7 limit slots are optional — set only the ones
    you need; omit or pass ``None`` for the rest.

    Attributes
    ----------
    type : Literal["fixed-limits"]
        Discriminator — always ``"fixed-limits"``.
    inferiorLimit3 : float, optional
        Inferior limit level 3 (most extreme lower bound).
    inferiorLimit2 : float, optional
        Inferior limit level 2.
    inferiorLimit1 : float, optional
        Inferior limit level 1 (first lower warning threshold).
    target : float, optional
        Target / nominal value.
    superiorLimit1 : float, optional
        Superior limit level 1 (first upper warning threshold).
    superiorLimit2 : float, optional
        Superior limit level 2.
    superiorLimit3 : float, optional
        Superior limit level 3 (most extreme upper bound).

    Example:

        ControlTimedLimitsCommand(
            applicableFrom="1970-01-01T00:00:00Z",
            limitsDefinition=FixedLimitsDefinitionCommand(
                inferiorLimit1=80.0,
                target=100.0,
                superiorLimit1=120.0,
            )
        )
    """

    type: Literal["fixed-limits"] = "fixed-limits"
    inferiorLimit3: Optional[float] = None
    inferiorLimit2: Optional[float] = None
    inferiorLimit1: Optional[float] = None
    target: Optional[float] = None
    superiorLimit1: Optional[float] = None
    superiorLimit2: Optional[float] = None
    superiorLimit3: Optional[float] = None


class DataLimitsDefinitionCommand(BaseModel):
    """
    Limit values driven by stored time-series data series.

    Each limit slot references the OIAnalytics ID of the data series whose
    values will be used as the dynamic limit.  Pass ``None`` for inactive slots.

    Attributes
    ----------
    type : Literal["data-limits"]
        Discriminator — always ``"data-limits"``.
    inferiorLimit3 : str, optional
        OIAnalytics data ID for inferior limit 3.
    inferiorLimit2 : str, optional
    inferiorLimit1 : str, optional
    target : str, optional
    superiorLimit1 : str, optional
    superiorLimit2 : str, optional
    superiorLimit3 : str, optional

    Example:

        DataLimitsDefinitionCommand(inferiorLimit1="D123", superiorLimit1="D456")
    """

    type: Literal["data-limits"] = "data-limits"
    inferiorLimit3: Optional[str] = None
    inferiorLimit2: Optional[str] = None
    inferiorLimit1: Optional[str] = None
    target: Optional[str] = None
    superiorLimit1: Optional[str] = None
    superiorLimit2: Optional[str] = None
    superiorLimit3: Optional[str] = None


class AssetTypeStaticDataLimitsDefinitionCommand(BaseModel):
    """
    Limit values driven by asset-type static data fields.

    Each slot references the OIAnalytics ID of a static-data definition on
    the asset type.  Requires ``assetTypeId`` on the parent
    :class:`ControlLimitsCommand`.

    Attributes
    ----------
    type : Literal["asset-type-static-data-limits"]
        Discriminator — always ``"asset-type-static-data-limits"``.
    inferiorLimit3 : str, optional
        OIAnalytics ID of the static-data definition for inferior limit 3.
    inferiorLimit2 : str, optional
    inferiorLimit1 : str, optional
    target : str, optional
    superiorLimit1 : str, optional
    superiorLimit2 : str, optional
    superiorLimit3 : str, optional
    """

    type: Literal["asset-type-static-data-limits"] = "asset-type-static-data-limits"
    inferiorLimit3: Optional[str] = None
    inferiorLimit2: Optional[str] = None
    inferiorLimit1: Optional[str] = None
    target: Optional[str] = None
    superiorLimit1: Optional[str] = None
    superiorLimit2: Optional[str] = None
    superiorLimit3: Optional[str] = None


class AssetTypeNumericDataLimitsDefinitionCommand(BaseModel):
    """
    Limit values driven by asset-type numeric (time-varying) data fields.

    Similar to :class:`AssetTypeStaticDataLimitsDefinitionCommand` but
    references numeric data fields rather than static ones.  Requires
    ``assetTypeId`` on the parent :class:`ControlLimitsCommand`.

    Attributes
    ----------
    type : Literal["asset-type-numeric-data-limits"]
        Discriminator — always ``"asset-type-numeric-data-limits"``.
    inferiorLimit3 : str, optional
    inferiorLimit2 : str, optional
    inferiorLimit1 : str, optional
    target : str, optional
    superiorLimit1 : str, optional
    superiorLimit2 : str, optional
    superiorLimit3 : str, optional
    """

    type: Literal["asset-type-numeric-data-limits"] = "asset-type-numeric-data-limits"
    inferiorLimit3: Optional[str] = None
    inferiorLimit2: Optional[str] = None
    inferiorLimit1: Optional[str] = None
    target: Optional[str] = None
    superiorLimit1: Optional[str] = None
    superiorLimit2: Optional[str] = None
    superiorLimit3: Optional[str] = None


class ProfiledLimitValue(BaseModel):
    """
    A single point on a profiled limit curve.

    Attributes
    ----------
    timeDeltaInSeconds : float
        Offset in seconds from the start of the batch step at which this
        limit value applies.
    value : float
        The limit value at this time delta, expressed in the control unit.
    """

    timeDeltaInSeconds: float
    value: float


class ProfiledLimit(BaseModel):
    """
    A time-varying limit defined as an ordered list of (timeDelta, value) pairs.

    Each pair specifies the limit value at a given number of seconds from the
    start of the batch step.  At least one value is required.

    Attributes
    ----------
    values : List[ProfiledLimitValue]
        Ordered list of limit values by time delta.

    Example:

        ProfiledLimit(values=[
            ProfiledLimitValue(timeDeltaInSeconds=0, value=20.0),
            ProfiledLimitValue(timeDeltaInSeconds=3600, value=30.0),
            ProfiledLimitValue(timeDeltaInSeconds=7200, value=35.0),
        ])
    """

    values: List[ProfiledLimitValue]


class ProfiledLimitsDefinitionCommand(BaseModel):
    """
    Limit values that vary over the batch duration (inside-batch controls only).

    Used exclusively with ``inside-batch-time-numeric-univariate`` controls.
    Each slot is a :class:`ProfiledLimit` — an ordered list of
    (timeDeltaInSeconds, value) pairs that define how the limit changes over
    the course of the batch step.  Pass ``None`` to leave a slot inactive.

    Attributes
    ----------
    type : Literal["profiled-limits"]
        Discriminator — always ``"profiled-limits"``.
    inferiorProfiledLimit : ProfiledLimit, optional
        Time-varying inferior limit curve.
    targetProfiledLimit : ProfiledLimit, optional
        Time-varying target curve.
    superiorProfiledLimit : ProfiledLimit, optional
        Time-varying superior limit curve.

    Example:

        ProfiledLimitsDefinitionCommand(
            inferiorProfiledLimit=ProfiledLimit(values=[
                ProfiledLimitValue(timeDeltaInSeconds=0, value=20.0),
                ProfiledLimitValue(timeDeltaInSeconds=7200, value=35.0),
            ]),
            superiorProfiledLimit=ProfiledLimit(values=[
                ProfiledLimitValue(timeDeltaInSeconds=0, value=40.0),
                ProfiledLimitValue(timeDeltaInSeconds=7200, value=50.0),
            ])
        )
    """

    type: Literal["profiled-limits"] = "profiled-limits"
    inferiorProfiledLimit: Optional[ProfiledLimit] = None
    targetProfiledLimit: Optional[ProfiledLimit] = None
    superiorProfiledLimit: Optional[ProfiledLimit] = None


LimitsDefinitionCommand = Annotated[
    Union[
        FixedLimitsDefinitionCommand,
        DataLimitsDefinitionCommand,
        AssetTypeStaticDataLimitsDefinitionCommand,
        AssetTypeNumericDataLimitsDefinitionCommand,
        ProfiledLimitsDefinitionCommand,
    ],
    Field(discriminator="type"),
]
"""
Discriminated union of all ``limitsDefinition`` command types.

Pydantic selects the concrete model based on the ``type`` field:

- ``"fixed-limits"``                   → :class:`FixedLimitsDefinitionCommand`
- ``"data-limits"``                    → :class:`DataLimitsDefinitionCommand`
- ``"asset-type-static-data-limits"``  → :class:`AssetTypeStaticDataLimitsDefinitionCommand`
- ``"asset-type-numeric-data-limits"`` → :class:`AssetTypeNumericDataLimitsDefinitionCommand`
- ``"profiled-limits"``                → :class:`ProfiledLimitsDefinitionCommand`
"""


class ControlTimedLimitsCommand(BaseModel):
    """
    A timed limits definition with an applicability window.

    Each :class:`ControlLimitsCommand` carries at least one timed limits
    entry.  The ``applicableFrom`` / ``applicableUntil`` window defines when
    these limit values are active.  Entries are ordered most-recent first.

    Attributes
    ----------
    applicableFrom : str
        ISO 8601 datetime from which these limit values apply
        (e.g. ``"1970-01-01T00:00:00Z"`` for a permanent baseline).
    applicableUntil : str, optional
        ISO 8601 datetime until which these limits apply.
        ``None`` means the limits are open-ended (no expiry).
    limitsDefinition : LimitsDefinitionCommand
        The actual limit values.  Use the concrete subclass that matches your
        use-case — see :data:`~oianalytics.api._dataframes.common_models.LimitsDefinitionCommand`.
    """

    applicableFrom: str
    applicableUntil: Optional[str] = None
    limitsDefinition: LimitsDefinitionCommand


class ControlLimitsDesignCommand(BaseModel):
    """
    Inline visual design for a control limits object.

    Defines the zone colour and line style for each of the 7 limit slots.
    Use this as the ``design`` field of :class:`ControlLimitsCommand` when
    you want to specify a custom design inline instead of referencing a named
    design via ``namedDesignId``.

    All slots are optional — only set the ones you need.

    Attributes
    ----------
    inferiorLimit3 : LimitSlot, optional
        Design for inferior limit 3.
    inferiorLimit2 : LimitSlot, optional
        Design for inferior limit 2.
    inferiorLimit1 : LimitSlot, optional
        Design for inferior limit 1.
    target : LimitSlot, optional
        Design for the target line.
    superiorLimit1 : LimitSlot, optional
        Design for superior limit 1.
    superiorLimit2 : LimitSlot, optional
        Design for superior limit 2.
    superiorLimit3 : LimitSlot, optional
        Design for superior limit 3.

    Example:

        ControlLimitsDesignCommand(
            inferiorLimit1=LimitSlot(zone=LimitZone(color="#ffd178"), line=LimitLine(width=1, style="Solid", color="#ffd178")),
            superiorLimit1=LimitSlot(zone=LimitZone(color="#ffd178"), line=LimitLine(width=1, style="Solid", color="#ffd178")),
        )
    """

    inferiorLimit3: Optional[LimitSlot] = None
    inferiorLimit2: Optional[LimitSlot] = None
    inferiorLimit1: Optional[LimitSlot] = None
    target: Optional[LimitSlot] = None
    superiorLimit1: Optional[LimitSlot] = None
    superiorLimit2: Optional[LimitSlot] = None
    superiorLimit3: Optional[LimitSlot] = None


class ControlLimitsCommand(BaseModel):
    """
    Command for creating or updating control limits.

    Attributes
    ----------
    name : str
        The name of the control limits.
    measurementId : str
        OIAnalytics ID of the measurement.
    unitId : str
        OIAnalytics ID of the unit in which limit values are expressed.
    type : str
        The type of the control limits. One of ``"fixed-limits"``,
        ``"data-limits"``, ``"profiled-limits"``,
        ``"asset-type-static-data-limits"``, or
        ``"asset-type-numeric-data-limits"``.
    timedLimits : List[ControlTimedLimitsCommand]
        At least one timed limits definition.
    assetTypeId : str, optional
        OIAnalytics ID of the asset type. Required for
        ``"asset-type-static-data-limits"`` and
        ``"asset-type-numeric-data-limits"`` types.
    namedDesignId : str, optional
        OIAnalytics ID of a named control limit design to apply.
        **Exactly one of** ``namedDesignId`` **or** ``design`` **must be set.**
    tagContext : List[TagAccessCommand], optional
        Tag access context restricting visibility of these limits.
    labelIds : List[str]
        OIAnalytics IDs of control labels to attach. Pass an empty list when
        no labels are needed.
    design : ControlLimitsDesignCommand, optional
        Inline visual design definition for the 7 limit slots.
        **Exactly one of** ``namedDesignId`` **or** ``design`` **must be set.**
    """

    name: str
    measurementId: str
    unitId: str
    type: str
    timedLimits: List[ControlTimedLimitsCommand]
    labelIds: List[str]
    assetTypeId: Optional[str] = None
    namedDesignId: Optional[str] = None
    tagContext: List[TagAccessCommand]
    design: Optional[ControlLimitsDesignCommand] = None


# ── Response models for ControlLimitsDesign ──────────────────────────────────


class ControlLimitsDesignResponse(BaseModel):
    """
    Visual design applied to a control limits object in API responses.

    The ``type`` field is either ``"anonymous"`` (inline design, no id/name)
    or ``"named"`` (references a saved :class:`ControlLimitDesign`).
    All 7 limit slot designs are optional.
    """

    type: str
    defaultDesign: bool
    id: Optional[str] = None
    name: Optional[str] = None
    inferiorLimit3: Optional[LimitSlot] = None
    inferiorLimit2: Optional[LimitSlot] = None
    inferiorLimit1: Optional[LimitSlot] = None
    target: Optional[LimitSlot] = None
    superiorLimit1: Optional[LimitSlot] = None
    superiorLimit2: Optional[LimitSlot] = None
    superiorLimit3: Optional[LimitSlot] = None


# ── Response models for LimitsDefinition (polymorphic) ───────────────────────


class FixedLimitsDefinition(BaseModel):
    """Response variant of fixed-limits — 7 optional float slots."""

    type: Literal["fixed-limits"] = "fixed-limits"
    inferiorLimit3: Optional[float] = None
    inferiorLimit2: Optional[float] = None
    inferiorLimit1: Optional[float] = None
    target: Optional[float] = None
    superiorLimit1: Optional[float] = None
    superiorLimit2: Optional[float] = None
    superiorLimit3: Optional[float] = None


class DataLimitsDefinition(BaseModel):
    """
    Response variant of data-limits.
    Each slot is a :class:`~oianalytics.api._dataframes.common_models.DataLight`
    object referencing the data series used as the limit value.
    """

    type: Literal["data-limits"] = "data-limits"
    inferiorLimit3: Optional[DataLight] = None
    inferiorLimit2: Optional[DataLight] = None
    inferiorLimit1: Optional[DataLight] = None
    target: Optional[DataLight] = None
    superiorLimit1: Optional[DataLight] = None
    superiorLimit2: Optional[DataLight] = None
    superiorLimit3: Optional[DataLight] = None


class AssetTypeStaticDataLimitsDefinition(BaseModel):
    """
    Response variant of asset-type-static-data-limits.

    Each slot is an :class:`~oianalytics.api._dataframes.common_models.AssetTypeStaticDataLight`
    object referencing the static data field of the asset type used as the limit.
    Requires ``assetTypeId`` to be set on the parent :class:`ControlLimits`.
    """

    type: Literal["asset-type-static-data-limits"] = "asset-type-static-data-limits"
    inferiorLimit3: Optional[AssetTypeStaticDataLight] = None
    inferiorLimit2: Optional[AssetTypeStaticDataLight] = None
    inferiorLimit1: Optional[AssetTypeStaticDataLight] = None
    target: Optional[AssetTypeStaticDataLight] = None
    superiorLimit1: Optional[AssetTypeStaticDataLight] = None
    superiorLimit2: Optional[AssetTypeStaticDataLight] = None
    superiorLimit3: Optional[AssetTypeStaticDataLight] = None


class AssetTypeNumericDataLimitsDefinition(BaseModel):
    """
    Response variant of asset-type-numeric-data-limits.

    Each slot is an :class:`~oianalytics.api._dataframes.common_models.AssetTypeDataLight`
    object referencing the time-varying numeric data field of the asset type
    used as the limit.  Requires ``assetTypeId`` to be set on the parent
    :class:`ControlLimits`.
    """

    type: Literal["asset-type-numeric-data-limits"] = "asset-type-numeric-data-limits"
    inferiorLimit3: Optional[AssetTypeDataLight] = None
    inferiorLimit2: Optional[AssetTypeDataLight] = None
    inferiorLimit1: Optional[AssetTypeDataLight] = None
    target: Optional[AssetTypeDataLight] = None
    superiorLimit1: Optional[AssetTypeDataLight] = None
    superiorLimit2: Optional[AssetTypeDataLight] = None
    superiorLimit3: Optional[AssetTypeDataLight] = None


LimitsDefinition = Annotated[
    Union[
        FixedLimitsDefinition,
        DataLimitsDefinition,
        ProfiledLimitsDefinitionCommand,  # same structure in responses
        AssetTypeStaticDataLimitsDefinition,
        AssetTypeNumericDataLimitsDefinition,
    ],
    Field(discriminator="type"),
]
"""Discriminated union of all limits definition response types."""


class ControlTimedLimits(BaseModel):
    """
    A timed limits entry as returned by the API.

    Attributes
    ----------
    applicableFrom : str
        ISO 8601 datetime from which these limits are active.
    applicableUntil : str, optional
        ISO 8601 datetime until which these limits are active (``None`` = open-ended).
    limitsDefinition : LimitsDefinition
        The actual limit values. The concrete type depends on the ``type``
        discriminator (``"fixed-limits"``, ``"data-limits"``, etc.).
    """

    applicableFrom: str
    applicableUntil: Optional[str] = None
    limitsDefinition: LimitsDefinition


# ─────────────────────────────────────────────────────────────────────────────


class ControlLimits(BaseModel):
    id: str
    name: str
    type: str
    measurement: Optional[Measurement] = None
    unit: Optional[Unit] = None
    design: ControlLimitsDesignResponse
    tagContext: List[TagAccess]
    timedLimits: List[ControlTimedLimits]
    labels: List[ControlLabel]
    assetType: Optional[AssetTypeLight] = None
    controlCount: int
    currentApplicableLimits: Optional[ControlTimedLimits] = None


# ─────────────────────────────────────────────────────────────────────────────
# Control limits — functions
# ─────────────────────────────────────────────────────────────────────────────


def list_control_limits(
    text: Optional[str] = None,
    page: int = 0,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List control limits. Returns a DataFrame indexed by id with columns:
    name, type, controlCount, measurement, unit, design, tagContext, timedLimits,
    labels, assetType, currentApplicableLimits.

    Parameters
    ----------
    text : str, optional
        Filter by name.
    page : int, default 0
    page_size : int, optional
    get_all_pages : bool, default True
    multithread_pages : bool, default False
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    if get_all_pages:
        page = 0
        if page_size is None:
            page_size = 10000

    def _get(page_num):
        return endpoints.controls.list_control_limits(
            text=text,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def _parse(r):
        df = pd.DataFrame(r["content"])
        if df.empty:
            df = pd.DataFrame(columns=["id", "name", "type", "controlCount"])
        return df.set_index("id")

    return utils.concat_pages_to_dataframe(
        getter=_get,
        parser=_parse,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )


def get_control_limits(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlLimits:
    """
    Retrieve control limits by their ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlLimits
    """
    return ControlLimits.model_validate(
        endpoints.controls.get_control_limits(id, api_credentials=api_credentials)
    )


def create_control_limits(
    command: ControlLimitsCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlLimits:
    """
    Create new control limits with at least one timed limits definition.

    Parameters
    ----------
    command : ControlLimitsCommand
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlLimits
    """
    if command.namedDesignId is None and command.design is None:
        raise ValueError(
            "Either 'namedDesignId' or 'design' must be provided in ControlLimitsCommand."
        )
    body = command.model_dump(mode="json")
    return ControlLimits.model_validate(
        endpoints.controls.create_control_limits(
            name=body["name"],
            measurement_id=body["measurementId"],
            unit_id=body["unitId"],
            limits_type=body["type"],
            timed_limits=body["timedLimits"],
            asset_type_id=body.get("assetTypeId"),
            named_design_id=body.get("namedDesignId"),
            tag_context=body.get("tagContext"),
            label_ids=body.get("labelIds"),
            design=body.get("design"),
            api_credentials=api_credentials,
        )
    )


def update_control_limits(
    id: str,
    command: ControlLimitsCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Update existing control limits.

    Parameters
    ----------
    id : str
    command : ControlLimitsCommand
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    if command.namedDesignId is None and command.design is None:
        raise ValueError(
            "Either 'namedDesignId' or 'design' must be provided in ControlLimitsCommand."
        )
    body = command.model_dump(mode="json")
    endpoints.controls.update_control_limits(
        control_limits_id=id,
        name=body["name"],
        measurement_id=body["measurementId"],
        unit_id=body["unitId"],
        limits_type=body["type"],
        timed_limits=body["timedLimits"],
        asset_type_id=body.get("assetTypeId"),
        named_design_id=body.get("namedDesignId"),
        tag_context=body.get("tagContext"),
        label_ids=body.get("labelIds"),
        design=body.get("design"),
        api_credentials=api_credentials,
    )


def delete_control_limits(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Delete control limits by their ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.delete_control_limits(
        control_limits_id=id, api_credentials=api_credentials
    )


# ─────────────────────────────────────────────────────────────────────────────
# Control condition blocks — models
# ─────────────────────────────────────────────────────────────────────────────

# ── Condition command models (discriminated union) ────────────────────────────


class TimeNumericControlConditionCommand(BaseModel):
    """
    Condition on a time-series numeric data series.

    The condition is met when the data value falls within [minValue, maxValue]
    (``None`` bounds are unbounded).

    Attributes
    ----------
    type : Literal["time-numeric-control-condition"]
    dataId : str
        OIAnalytics ID of the time-series numeric data series.
    unitId : str
        OIAnalytics ID of the unit for minValue / maxValue.
    minValue : float, optional
    maxValue : float, optional
    """

    type: Literal["time-numeric-control-condition"] = "time-numeric-control-condition"
    dataId: str
    unitId: str
    minValue: Optional[float] = None
    maxValue: Optional[float] = None


class TimeStringControlConditionCommand(BaseModel):
    """
    Condition on a time-series string data series.

    The condition is met when the data value is one of ``acceptableValues``.

    Attributes
    ----------
    type : Literal["time-string-control-condition"]
    dataId : str
        OIAnalytics ID of the time-series string data series.
    acceptableValues : List[str]
        At least one acceptable string value.
    """

    type: Literal["time-string-control-condition"] = "time-string-control-condition"
    dataId: str
    acceptableValues: List[str]


class BatchNumericControlConditionCommand(BaseModel):
    """
    Condition on a batch-level numeric data value.

    Attributes
    ----------
    type : Literal["batch-numeric-control-condition"]
    dataId : str
        OIAnalytics ID of the batch numeric data.
    unitId : str
        OIAnalytics ID of the unit for minValue / maxValue.
    minValue : float, optional
    maxValue : float, optional
    """

    type: Literal["batch-numeric-control-condition"] = "batch-numeric-control-condition"
    dataId: str
    unitId: str
    minValue: Optional[float] = None
    maxValue: Optional[float] = None


class BatchTagControlConditionCommand(BaseModel):
    """
    Condition on a batch tag value.

    The condition is met when the batch tag value for ``batchTagKeyId``
    is one of ``acceptableTagValueIds``.

    Attributes
    ----------
    type : Literal["batch-tag-control-condition"]
    batchTagKeyId : str
        OIAnalytics ID of the batch tag key.
    acceptableTagValueIds : List[str]
        At least one acceptable batch tag value ID.
    includeNullValues : bool
        Whether batches with no tag value also satisfy the condition.
    """

    type: Literal["batch-tag-control-condition"] = "batch-tag-control-condition"
    batchTagKeyId: str
    acceptableTagValueIds: List[str]
    includeNullValues: bool


class AssetNumericControlConditionCommand(BaseModel):
    """
    Condition on an asset-type numeric data field.

    Attributes
    ----------
    type : Literal["asset-numeric-control-condition"]
    assetTypeNumericDataId : str
        OIAnalytics ID of the asset type numeric data definition.
    unitId : str
        OIAnalytics ID of the unit for minValue / maxValue.
    minValue : float, optional
    maxValue : float, optional
    """

    type: Literal["asset-numeric-control-condition"] = "asset-numeric-control-condition"
    assetTypeNumericDataId: str
    unitId: str
    minValue: Optional[float] = None
    maxValue: Optional[float] = None


ControlConditionCommand = Annotated[
    Union[
        TimeNumericControlConditionCommand,
        TimeStringControlConditionCommand,
        BatchNumericControlConditionCommand,
        BatchTagControlConditionCommand,
        AssetNumericControlConditionCommand,
    ],
    Field(discriminator="type"),
]
"""
Discriminated union of all control condition command types.

- ``"time-numeric-control-condition"``  → :class:`TimeNumericControlConditionCommand`
- ``"time-string-control-condition"``   → :class:`TimeStringControlConditionCommand`
- ``"batch-numeric-control-condition"`` → :class:`BatchNumericControlConditionCommand`
- ``"batch-tag-control-condition"``     → :class:`BatchTagControlConditionCommand`
- ``"asset-numeric-control-condition"`` → :class:`AssetNumericControlConditionCommand`
"""


class ControlConditionBlockCommand(BaseModel):
    name: str
    contextType: str
    conditions: List[ControlConditionCommand]
    tagContext: List[TagAccessCommand]
    batchStructureId: Optional[str] = None
    assetTypeId: Optional[str] = None


# ── Control condition response models (discriminated union) ───────────────────


class TimeNumericControlCondition(BaseModel):
    """Response: condition on a time-series numeric data series."""

    type: Literal["time-numeric-control-condition"]
    id: str
    data: DataLight
    minValue: Optional[float] = None
    maxValue: Optional[float] = None


class TimeStringControlCondition(BaseModel):
    """Response: condition on a time-series string data series."""

    type: Literal["time-string-control-condition"]
    id: str
    data: DataLight
    acceptableValues: List[str]


class BatchNumericControlCondition(BaseModel):
    """Response: condition on a batch-level numeric data value."""

    type: Literal["batch-numeric-control-condition"]
    id: str
    data: DataLight
    minValue: Optional[float] = None
    maxValue: Optional[float] = None


class BatchTagControlCondition(BaseModel):
    """Response: condition on a batch tag value."""

    type: Literal["batch-tag-control-condition"]
    id: str
    batchStructure: BatchTypeLight
    batchTagKey: Any
    acceptableValues: List[Any]
    includeNullValues: bool


class AssetNumericControlCondition(BaseModel):
    """Response: condition on an asset-type numeric data field."""

    type: Literal["asset-numeric-control-condition"]
    id: str
    assetTypeNumericData: Any
    minValue: Optional[float] = None
    maxValue: Optional[float] = None


ControlCondition = Annotated[
    Union[
        TimeNumericControlCondition,
        TimeStringControlCondition,
        BatchNumericControlCondition,
        BatchTagControlCondition,
        AssetNumericControlCondition,
    ],
    Field(discriminator="type"),
]
"""Discriminated union of all control condition response types."""


class ControlConditionBlock(BaseModel):
    id: str
    name: str
    contextType: str
    conditions: List[ControlCondition]
    tagContext: List[TagAccess]
    batchStructure: Optional[BatchTypeLight] = None
    assetType: Optional[AssetTypeLight] = None


# ─────────────────────────────────────────────────────────────────────────────
# Control condition blocks — functions
# ─────────────────────────────────────────────────────────────────────────────


def list_control_condition_blocks(
    text: Optional[str] = None,
    page: int = 0,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List control condition blocks. Returns a DataFrame indexed by id with columns:
    name, contextType, conditions, batchStructure, assetType, tagContext.

    Parameters
    ----------
    text : str, optional
        Filter by name.
    page : int, default 0
    page_size : int, optional
    get_all_pages : bool, default True
    multithread_pages : bool, default False
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    if get_all_pages:
        page = 0
        if page_size is None:
            page_size = 10000

    def _get(page_num):
        return endpoints.controls.list_control_condition_blocks(
            text=text,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def _parse(r):
        df = pd.DataFrame(r["content"])
        if df.empty:
            df = pd.DataFrame(columns=["id", "name", "contextType", "conditions"])
        return df.set_index("id")

    return utils.concat_pages_to_dataframe(
        getter=_get,
        parser=_parse,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )


def get_control_condition_block(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlConditionBlock:
    """
    Retrieve a control condition block by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlConditionBlock
    """
    return ControlConditionBlock.model_validate(
        endpoints.controls.get_control_condition_block(
            id, api_credentials=api_credentials
        )
    )


def create_control_condition_block(
    command: ControlConditionBlockCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlConditionBlock:
    """
    Create a new control condition block.

    Parameters
    ----------
    command : ControlConditionBlockCommand
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlConditionBlock
    """
    return ControlConditionBlock.model_validate(
        endpoints.controls.create_control_condition_block(
            name=command.name,
            context_type=command.contextType,
            conditions=command.conditions,
            batch_structure_id=command.batchStructureId,
            asset_type_id=command.assetTypeId,
            tag_context=command.tagContext,
            api_credentials=api_credentials,
        )
    )


def update_control_condition_block(
    id: str,
    command: ControlConditionBlockCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Update an existing control condition block.

    Parameters
    ----------
    id : str
    command : ControlConditionBlockCommand
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.update_control_condition_block(
        control_condition_block_id=id,
        name=command.name,
        context_type=command.contextType,
        conditions=command.conditions,
        batch_structure_id=command.batchStructureId,
        asset_type_id=command.assetTypeId,
        tag_context=command.tagContext,
        api_credentials=api_credentials,
    )


def delete_control_condition_block(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Delete a control condition block by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.delete_control_condition_block(
        control_condition_block_id=id, api_credentials=api_credentials
    )


# ─────────────────────────────────────────────────────────────────────────────
# Control contexts — models
# ─────────────────────────────────────────────────────────────────────────────


class ControlContextCommand(BaseModel):
    name: str
    type: str
    conditionBlockIds: List[str]
    batchStructureId: Optional[str] = None
    assetTypeId: Optional[str] = None
    tagContext: List[TagAccessCommand]


class ControlContext(BaseModel):
    id: str
    name: str
    type: str
    conditionBlocks: Optional[List[Any]] = None
    batchStructure: Optional[BatchTypeLight] = None
    assetType: Optional[AssetTypeLight] = None
    tagContext: List[TagAccess]


# ─────────────────────────────────────────────────────────────────────────────
# Control contexts — functions
# ─────────────────────────────────────────────────────────────────────────────


def list_control_contexts(
    text: Optional[str] = None,
    page: int = 0,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List control contexts. Returns a DataFrame indexed by id with columns:
    name, type, conditionBlocks, batchStructure, assetType, tagContext.

    Parameters
    ----------
    text : str, optional
        Filter by name.
    page : int, default 0
    page_size : int, optional
    get_all_pages : bool, default True
    multithread_pages : bool, default False
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    if get_all_pages:
        page = 0
        if page_size is None:
            page_size = 10000

    def _get(page_num):
        return endpoints.controls.list_control_contexts(
            text=text,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def _parse(r):
        df = pd.DataFrame(r["content"])
        if df.empty:
            df = pd.DataFrame(columns=["id", "name", "type", "conditionBlocks"])
        return df.set_index("id")

    return utils.concat_pages_to_dataframe(
        getter=_get,
        parser=_parse,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )


def get_control_context(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlContext:
    """
    Retrieve a control context by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlContext
    """
    return ControlContext.model_validate(
        endpoints.controls.get_control_context(id, api_credentials=api_credentials)
    )


def create_control_context(
    command: ControlContextCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> ControlContext:
    """
    Create a new control context.

    Parameters
    ----------
    command : ControlContextCommand
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    ControlContext
    """
    return ControlContext.model_validate(
        endpoints.controls.create_control_context(
            name=command.name,
            context_type=command.type,
            condition_block_ids=command.conditionBlockIds,
            batch_structure_id=command.batchStructureId,
            asset_type_id=command.assetTypeId,
            tag_context=command.tagContext,
            api_credentials=api_credentials,
        )
    )


def update_control_context(
    id: str,
    command: ControlContextCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Update an existing control context.

    Parameters
    ----------
    id : str
    command : ControlContextCommand
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.update_control_context(
        control_context_id=id,
        name=command.name,
        context_type=command.type,
        condition_block_ids=command.conditionBlockIds,
        batch_structure_id=command.batchStructureId,
        asset_type_id=command.assetTypeId,
        tag_context=command.tagContext,
        api_credentials=api_credentials,
    )


def delete_control_context(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Delete a control context by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.delete_control_context(
        control_context_id=id, api_credentials=api_credentials
    )


# ─────────────────────────────────────────────────────────────────────────────
# Controls — models
# ─────────────────────────────────────────────────────────────────────────────


class ControlCommand(BaseModel):
    type: str
    name: str
    unitId: str
    tagContext: List[TagAccessCommand]
    batchStructureId: Optional[str] = None
    dataId: Optional[str] = None
    contextId: Optional[str] = None
    noContextLimitsId: Optional[str] = None
    labelIds: Optional[List[str]] = None
    applicableConditionBlockIds: Optional[List[str]] = None
    ruleIds: Optional[List[str]] = None
    contextualizedLimits: Optional[List[dict]] = None


class Control(BaseModel):
    id: str
    name: str
    type: str
    tagContext: List[TagAccess]
    unit: Optional[Unit] = None
    data: Optional[Any] = None
    batchStructure: Optional[BatchTypeLight] = None
    context: Optional[Any] = None
    contextualizedLimits: Optional[List[Any]] = None
    noContextLimits: Optional[Any] = None
    labels: Optional[List[ControlLabel]] = None
    applicableConditions: Optional[List[Any]] = None
    rules: Optional[List[ControlRule]] = None


# ─────────────────────────────────────────────────────────────────────────────
# Controls — functions
# ─────────────────────────────────────────────────────────────────────────────


def list_controls(
    text: Optional[str] = None,
    page: int = 0,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List controls. Returns a DataFrame indexed by id with columns:
    name, type, unit, data, batchStructure, context, contextualizedLimits,
    noContextLimits, labels, applicableConditions, rules, tagContext.

    Parameters
    ----------
    text : str, optional
        Filter by name.
    page : int, default 0
    page_size : int, optional
    get_all_pages : bool, default True
    multithread_pages : bool, default False
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    if get_all_pages:
        page = 0
        if page_size is None:
            page_size = 10000

    def _get(page_num):
        return endpoints.controls.list_controls(
            text=text,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def _parse(r):
        df = pd.DataFrame(r["content"])
        if df.empty:
            df = pd.DataFrame(columns=["id", "name", "type"])
        return df.set_index("id")

    return utils.concat_pages_to_dataframe(
        getter=_get,
        parser=_parse,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )


def get_control(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> Control:
    """
    Retrieve a control by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    Control
    """
    return Control.model_validate(
        endpoints.controls.get_control(id, api_credentials=api_credentials)
    )


def create_control(
    command: ControlCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> Control:
    """
    Create a new control.

    Parameters
    ----------
    command : ControlCommand
    api_credentials : OIAnalyticsAPICredentials, optional

    Returns
    -------
    Control
    """
    return Control.model_validate(
        endpoints.controls.create_control(
            control_type=command.type,
            name=command.name,
            unit_id=command.unitId,
            tag_context=command.tagContext,
            batch_structure_id=command.batchStructureId,
            data_id=command.dataId,
            context_id=command.contextId,
            no_context_limits_id=command.noContextLimitsId,
            label_ids=command.labelIds,
            applicable_condition_block_ids=command.applicableConditionBlockIds,
            rule_ids=command.ruleIds,
            contextualized_limits=command.contextualizedLimits,
            api_credentials=api_credentials,
        )
    )


def update_control(
    id: str,
    command: ControlCommand,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Update an existing control.

    Parameters
    ----------
    id : str
    command : ControlCommand
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.update_control(
        control_id=id,
        control_type=command.type,
        name=command.name,
        unit_id=command.unitId,
        tag_context=command.tagContext,
        batch_structure_id=command.batchStructureId,
        data_id=command.dataId,
        context_id=command.contextId,
        no_context_limits_id=command.noContextLimitsId,
        label_ids=command.labelIds,
        applicable_condition_block_ids=command.applicableConditionBlockIds,
        rule_ids=command.ruleIds,
        contextualized_limits=command.contextualizedLimits,
        api_credentials=api_credentials,
    )


def delete_control(
    id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> None:
    """
    Delete a control by its ID.

    Parameters
    ----------
    id : str
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    endpoints.controls.delete_control(control_id=id, api_credentials=api_credentials)


def get_control_values(
    id: str,
    query: dict,
    return_uncontrolled_points: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    Query time-series values for a control. Returns a DataFrame indexed by timestamp
    with columns: value, color, reasonForNoControl, violatedControlRuleIds, batchName.

    Parameters
    ----------
    id : str
        OIAnalytics ID of the control.
    query : dict
        A ControlValueQuery dict — see endpoints.controls.get_control_values.
    return_uncontrolled_points : bool, default False
        If True, include points where control could not be performed.
    api_credentials : OIAnalyticsAPICredentials, optional
    """
    result = endpoints.controls.get_control_values(
        control_id=id,
        query=query,
        return_uncontrolled_points=return_uncontrolled_points,
        api_credentials=api_credentials,
    )
    timestamps = pd.to_datetime(result.get("timestamps", []), utc=True)
    n = len(timestamps)
    df = pd.DataFrame(
        {
            "value": result.get("values", []),
            "color": result.get("colors", []),
            "reasonForNoControl": result.get("reasonsForNoControl", []),
            "violatedControlRuleIds": result.get("violatedControlRuleIds", []),
            "batchName": result.get("batchNames") or [None] * n,
        },
        index=timestamps,
    )
    df.index.name = "timestamp"
    return df


__all__ = [
    # Functions — control labels
    "list_control_labels",
    "get_control_label",
    "create_control_label",
    "update_control_label",
    "delete_control_label",
    # Functions — control limit designs
    "list_control_limit_designs",
    "get_control_limit_design",
    "create_control_limit_design",
    "update_control_limit_design",
    "delete_control_limit_design",
    # Functions — control rules
    "list_control_rules",
    "get_control_rule",
    "create_control_rule",
    "update_control_rule",
    "delete_control_rule",
    # Functions — control limits
    "list_control_limits",
    "get_control_limits",
    "create_control_limits",
    "update_control_limits",
    "delete_control_limits",
    # Functions — control condition blocks
    "list_control_condition_blocks",
    "get_control_condition_block",
    "create_control_condition_block",
    "update_control_condition_block",
    "delete_control_condition_block",
    # Functions — control contexts
    "list_control_contexts",
    "get_control_context",
    "create_control_context",
    "update_control_context",
    "delete_control_context",
    # Functions — controls
    "list_controls",
    "get_control",
    "create_control",
    "update_control",
    "delete_control",
    "get_control_values",
    # Limits definition command variants
    "FixedLimitsDefinitionCommand",
    "DataLimitsDefinitionCommand",
    "AssetTypeStaticDataLimitsDefinitionCommand",
    "AssetTypeNumericDataLimitsDefinitionCommand",
    "ProfiledLimitsDefinitionCommand",
    "ProfiledLimit",
    "ProfiledLimitValue",
    "LimitsDefinitionCommand",
    # Models — commands
    "ControlCommand",
    "ControlLabelCommand",
    "ControlLimitDesignCommand",
    "ControlRuleCommand",
    "ControlLimitsCommand",
    "ControlLimitsDesignCommand",
    "ControlTimedLimitsCommand",
    "ControlConditionBlockCommand",
    "ControlConditionCommand",
    "TimeNumericControlConditionCommand",
    "TimeStringControlConditionCommand",
    "BatchNumericControlConditionCommand",
    "BatchTagControlConditionCommand",
    "AssetNumericControlConditionCommand",
    "ControlContextCommand",
    # Models — responses
    "Control",
    "ControlLabel",
    "ControlLimitDesign",
    "ControlRule",
    "ControlLimits",
    "ControlLimitsDesignResponse",
    "ControlTimedLimits",
    "LimitsDefinition",
    "FixedLimitsDefinition",
    "DataLimitsDefinition",
    "AssetTypeStaticDataLimitsDefinition",
    "AssetTypeNumericDataLimitsDefinition",
    "ControlConditionBlock",
    "ControlCondition",
    "TimeNumericControlCondition",
    "TimeStringControlCondition",
    "BatchNumericControlCondition",
    "BatchTagControlCondition",
    "AssetNumericControlCondition",
    "ControlContext",
    # Shared design models
    "LimitSlots",
    "LimitSlot",
    "LimitZone",
    "LimitLine",
]

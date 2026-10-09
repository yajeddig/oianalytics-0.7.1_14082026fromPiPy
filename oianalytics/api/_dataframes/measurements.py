from typing import Optional

import pandas as pd
from pydantic import BaseModel

from .. import _credentials
from .. import endpoints
from .. import utils
from .quantities import Unit, UnitFamily


class Measurement(BaseModel):
    """
    A measurement (physical quantity + storage unit) defined in OIAnalytics.

    Attributes
    ----------
    id : str
    name : str
    type : str
        ``"NUMERIC"`` or ``"STRING"``.
    quantityId : str
        OIAnalytics ID of the physical quantity.
    storageUnit : Unit
        Unit in which values are stored.
    defaultUnitFamily : UnitFamily, optional
        Default unit family for display conversion.
    """

    id: str
    name: str
    type: str
    quantityId: str
    storageUnit: Unit
    defaultUnitFamily: Optional[UnitFamily] = None


__all__ = [
    "Measurement",
    "get_measurements",
]


def get_measurements(
    name: Optional[str] = None,
    unit_id: Optional[str] = None,
    unit_family_id: Optional[str] = None,
    page: int = 0,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = False,
    expand_storage_unit: bool = True,
    expand_default_unit_family: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List measurements by page.

    Parameters
    ----------
    name : str, optional
        The text the measurement name should contain. The search is performed in case insensitive manner.
    unit_id : str, optional
        Search by storage unit ID.
    unit_family_id : str, optional
        Search by unit family ID.
    page : int, default 0
        The page to retrieve. It is ignored if 'get_all_pages' is set to True.
    page_size : int, optional
        The size of one page. Ignored when 'get_all_pages' is True unless explicitly set, in
        which case it is used instead of the default of 10000.
    get_all_pages : bool, default True
        Whether to get measurements of all pages.
        If the value is set to True, the 'page' argument will be ignored, and the function will retrieve all pages.
    multithread_pages : bool, default False
        Only used when getting all pages. If True, pages are retrieved in multiple threads simultaneously.
    expand_storage_unit : bool, default True
        Whether to expand the 'storageUnit' column.
    expand_default_unit_family : bool, default True
        Whether to expand the 'defaultUnitFamily' column.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the measurements indexed by their correspondent measurement IDs.
    """
    if get_all_pages:
        page = 0
        if page_size is None:
            page_size = 10000

    def get_page(page_num: int) -> dict:
        return endpoints.measurements.get_measurements(
            name=name,
            unit_id=unit_id,
            unit_family_id=unit_family_id,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def parse_page(page_response: dict) -> pd.DataFrame:
        page_df = pd.DataFrame(page_response["content"])
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(
                columns=[
                    "id",
                    "name",
                    "type",
                    "storageUnit",
                    "quantityId",
                    "defaultUnitFamily",
                ]
            )
        page_df.set_index("id", inplace=True)
        return page_df

    df = utils.concat_pages_to_dataframe(
        getter=get_page,
        parser=parse_page,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )

    if expand_storage_unit:
        df = utils.expand_dataframe_column(
            df=df,
            col="storageUnit",
        )

    if expand_default_unit_family:
        df = utils.expand_dataframe_column(
            df=df,
            col="defaultUnitFamily",
        )

    # output
    return df

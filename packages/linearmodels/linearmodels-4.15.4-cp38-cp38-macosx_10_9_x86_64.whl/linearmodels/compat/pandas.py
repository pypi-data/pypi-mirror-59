from distutils.version import LooseVersion

import numpy as np
import pandas as pd

from linearmodels.typing import AnyPandas

PD_LT_023 = LooseVersion(pd.__version__) < LooseVersion("0.23")

__all__ = [
    "is_string_dtype",
    "is_numeric_dtype",
    "is_categorical",
    "is_string_like",
    "is_categorical_dtype",
    "is_datetime64_any_dtype",
    "concat",
    "get_codes",
    "to_numpy",
    "assert_series_equal",
]

try:
    from pandas.testing import assert_series_equal
except ImportError:
    from pandas.util.testing import assert_series_equal


def concat(*args, **kwargs):
    """
    Shim around pandas concat that passes sort if allowed

    See pandas.compat
    """
    if PD_LT_023 and "sort" in kwargs:
        kwargs = kwargs.copy()
        del kwargs["sort"]
    elif not PD_LT_023:
        if "sort" not in kwargs:
            kwargs = kwargs.copy()
            kwargs["sort"] = False

    return pd.concat(*args, **kwargs)


try:
    from pandas.api.types import (
        is_numeric_dtype,
        is_categorical,
        is_string_dtype,
        is_categorical_dtype,
        is_datetime64_any_dtype,
    )

    # From pandas 0.20.1
    def is_string_like(obj):
        """
        Check if the object is a string.

        Parameters
        ----------
        obj : The object to check.

        Returns
        -------
        bool
            Whether `obj` is a string or not.
        """
        return isinstance(obj, str)


except ImportError:  # pragma: no cover
    from pandas.core.common import (
        is_string_dtype,
        is_numeric_dtype,
        is_categorical,
        is_categorical_dtype,
        is_datetime64_any_dtype,
        is_string_like,
    )


def get_codes(index):
    """
    Tries .codes before falling back to .labels
    """
    try:
        return index.codes
    except AttributeError:
        return index.labels


def to_numpy(df: AnyPandas) -> np.ndarray:
    try:
        return df.to_numpy()
    except AttributeError:
        return np.asarray(df)

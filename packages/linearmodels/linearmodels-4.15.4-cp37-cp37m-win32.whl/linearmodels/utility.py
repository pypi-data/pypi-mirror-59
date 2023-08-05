from linearmodels.compat.numpy import lstsq
from linearmodels.compat.pandas import concat

from collections import OrderedDict
from collections.abc import MutableMapping

import numpy as np
from pandas import DataFrame, MultiIndex, Series
from patsy.design_info import DesignInfo
from scipy.stats import chi2, f
from statsmodels.iolib.summary import SimpleTable, fmt_params


class MissingValueWarning(Warning):
    pass


missing_value_warning_msg = """
Inputs contain missing values. Dropping rows with missing observations."""


class MemoryWarning(Warning):
    pass


class InferenceUnavailableWarning(Warning):
    pass


class SingletonWarning(Warning):
    pass


class AttrDict(MutableMapping):
    """
    Ordered dictionary-like object that exposes keys as attributes
    """

    def update(self, *args, **kwargs):
        """
        Update AD from dictionary or iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: AD[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: AD[k] = v
        In either case, this is followed by: for k in F:  AD[k] = F[k]
        """
        self.__ordered_dict__.update(*args, **kwargs)

    def clear(self):
        """Remove all items from AD. """
        self.__ordered_dict__.clear()

    def copy(self):
        """Create a shallow copy of AD """
        ad = AttrDict()
        for key in self.__ordered_dict__.keys():
            ad[key] = self.__ordered_dict__[key]
        return ad

    def keys(self):
        """Return an ordered list-like object providing a view on AD's keys """
        return self.__ordered_dict__.keys()

    def items(self):
        """Return an ordered list-like object providing a view on AD's items """
        return self.__ordered_dict__.items()

    def values(self):
        """Return an ordered list-like object object providing a view on AD's values """
        return self.__ordered_dict__.values()

    def pop(self, key, default=None):
        """
        Remove specified key and return the corresponding value.
        If key is not found, default is returned if given, otherwise KeyError is raised
        """

        return self.__ordered_dict__.pop(key, default)

    def __len__(self):
        return self.__ordered_dict__.__len__()

    def __repr__(self):
        out = self.__ordered_dict__.__str__()
        return "Attr" + out[7:]

    def __str__(self):
        return self.__repr__()

    def __init__(self, *args, **kwargs):
        self.__dict__["__ordered_dict__"] = OrderedDict(*args, **kwargs)

    def __contains__(self, item):
        return self.__ordered_dict__.__contains__(item)

    def __getitem__(self, item):
        return self.__ordered_dict__[item]

    def __setitem__(self, key, value):
        if key == "__ordered_dict__":
            raise KeyError(key + " is reserved and cannot be set.")
        self.__ordered_dict__[key] = value

    def __delitem__(self, key):
        del self.__ordered_dict__[key]

    def __getattr__(self, item):
        if item not in self.__ordered_dict__:
            raise AttributeError
        return self.__ordered_dict__[item]

    def __setattr__(self, key, value):
        if key == "__ordered_dict__":
            raise AttributeError(key + " is invalid")
        self.__ordered_dict__[key] = value

    def __delattr__(self, name):
        del self.__ordered_dict__[name]

    def __dir__(self):
        out = super(AttrDict, self).__dir__() + list(self.__ordered_dict__.keys())
        out = filter(lambda s: isinstance(s, str) and s.isidentifier(), out)
        return sorted(set(out))

    def __iter__(self):
        return self.__ordered_dict__.__iter__()


def has_constant(x, x_rank=None):
    """
    Parameters
    ----------
    x: ndarray
        Array to be checked for a constant (n,k)
    x_rank : {int, None}
        Rank of x if previously computed.  If None, this value will be
        computed.

    Returns
    -------
    const : bool
        Flag indicating whether x contains a constant or has column span with
        a constant
    loc : int
        Column location of constant
    """
    if np.any(np.all(x == 1, axis=0)):
        loc = np.argwhere(np.all(x == 1, axis=0))
        return True, int(loc)

    if np.any((np.ptp(x, axis=0) == 0) & ~np.all(x == 0, axis=0)):
        loc = (np.ptp(x, axis=0) == 0) & ~np.all(x == 0, axis=0)
        loc = np.argwhere(loc)
        return True, int(loc)

    n = x.shape[0]
    aug_rank = np.linalg.matrix_rank(np.c_[np.ones((n, 1)), x])
    rank = np.linalg.matrix_rank(x) if x_rank is None else x_rank

    has_const = (aug_rank == rank) and x.shape[0] > x.shape[1]
    has_const = has_const or rank < min(x.shape)
    loc = None
    if has_const:
        out = lstsq(x, np.ones((n, 1)))
        beta = out[0].ravel()
        loc = np.argmax(np.abs(beta) * x.var(0))
    return bool(has_const), loc


def inv_sqrth(x):
    """
    Matrix inverse square root

    Parameters
    ----------
    x : ndarray
        Real, symmetric matrix

    Returns
    -------
    ndarray
        Input to the power -1/2
    """
    vals, vecs = np.linalg.eigh(x)
    return vecs @ np.diag(1 / np.sqrt(vals)) @ vecs.T


class WaldTestStatistic(object):
    """
    Test statistic holder for Wald-type tests

    Parameters
    ----------
    stat : float
        The test statistic
    null : str
        A statement of the test's null hypothesis
    df : int
        Degree of freedom.
    df_denom : int, optional
        Numerator degree of freedom.  If provided, uses an
        F(df, df_denom) distribution.
    name : str, optional
        Name of test

    See Also
    --------
    InvalidTestStatistic
    """

    def __init__(self, stat, null, df, df_denom=None, name=None):
        self._stat = stat
        self._null = null
        self.df = df
        self.df_denom = df_denom
        self._name = name
        if df_denom is None:
            self.dist = chi2(df)
            self.dist_name = "chi2({0})".format(df)
        else:
            self.dist = f(df, df_denom)
            self.dist_name = "F({0},{1})".format(df, df_denom)

    @property
    def stat(self):
        """Test statistic"""
        return self._stat

    @property
    def pval(self):
        """P-value of test statistic"""
        return 1 - self.dist.cdf(self.stat)

    @property
    def critical_values(self):
        """Critical values test for common test sizes"""
        return OrderedDict(zip(["10%", "5%", "1%"], self.dist.ppf([0.9, 0.95, 0.99])))

    @property
    def null(self):
        """Null hypothesis"""
        return self._null

    def __str__(self):
        name = "" if not self._name else self._name + "\n"
        msg = (
            "{name}H0: {null}\nStatistic: {stat:0.4f}\n"
            "P-value: {pval:0.4f}\nDistributed: {dist}"
        )
        return msg.format(
            name=name,
            null=self.null,
            stat=self.stat,
            pval=self.pval,
            dist=self.dist_name,
        )

    def __repr__(self):
        return (
            self.__str__()
            + "\n"
            + self.__class__.__name__
            + ", id: {0}".format(hex(id(self)))
        )


class InvalidTestWarning(UserWarning):
    pass


class InvalidTestStatistic(WaldTestStatistic):
    """
    Class returned if a requested test is not valid for a model

    Parameters
    ----------
    reason : str
        Explanation why test is invalid
    name : str, optional
        Name of test

    See Also
    --------
    WaldTestStatistic
    """

    def __init__(self, reason, *, name=None):
        self._reason = reason
        super(InvalidTestStatistic, self).__init__(
            np.NaN, np.NaN, df=1, df_denom=1, name=name
        )
        self.dist_name = "None"

    @property
    def pval(self):
        """Always returns np.NaN"""
        return np.NaN

    @property
    def critical_values(self):
        """Always returns None"""
        return None

    def __str__(self):
        msg = "Invalid test statistic\n{reason}\n{name}"
        name = "" if self._name is None else self._name
        return msg.format(name=name, reason=self._reason)


class InapplicableTestStatistic(WaldTestStatistic):
    """
    Class returned if a requested test is not applicable for a specification

    Parameters
    ----------
    reason : str
        Explanation why test is invalid
    name : str, optional
        Name of test

    See Also
    --------
    WaldTestStatistic
    """

    def __init__(self, *, reason=None, name=None):
        self._reason = reason
        if reason is None:
            self._reason = "Test is not applicable to model specification"

        super(InapplicableTestStatistic, self).__init__(
            np.NaN, np.NaN, df=1, df_denom=1, name=name
        )
        self.dist_name = "None"

    @property
    def pval(self):
        """Always returns np.NaN"""
        return np.NaN

    @property
    def critical_values(self):
        """Always returns None"""
        return None

    def __str__(self):
        msg = "Irrelevant test statistic\n{reason}\n{name}"
        name = "" if self._name is None else self._name
        return msg.format(name=name, reason=self._reason)


def _str(v):
    """Preferred basic formatter"""
    if np.isnan(v):
        return "        "
    av = abs(v)
    digits = 0
    if av != 0:
        digits = np.ceil(np.log10(av))
    if digits > 4 or digits <= -4:
        return "{0:8.4g}".format(v)

    if digits > 0:
        d = int(5 - digits)
    else:
        d = int(4)

    format_str = "{0:" + "0.{0}f".format(d) + "}"
    return format_str.format(v)


def pval_format(v):
    """Preferred formatting for x in [0,1]"""
    if np.isnan(v):
        return "        "
    return "{0:4.4f}".format(v)


class _SummaryStr(object):
    def __str__(self):
        return self.summary.as_text()

    def __repr__(self):
        return (
            self.__str__()
            + "\n"
            + self.__class__.__name__
            + ", id: {0}".format(hex(id(self)))
        )

    def _repr_html_(self):
        return self.summary.as_html() + "<br/>id: {0}".format(hex(id(self)))


def ensure_unique_column(col_name, df, addition="_"):
    while col_name in df:
        col_name = addition + col_name + addition
    return col_name


class _ModelComparison(_SummaryStr):
    """
    Base class for model comparisons
    """

    _supported = tuple()
    _PRECISION_TYPES = {
        "tstats": "T-stats",
        "pvalues": "P-values",
        "std_errors": "Std. Errors",
    }

    def __init__(self, results, *, precision="tstats"):
        if not isinstance(results, (dict, OrderedDict)):
            _results = OrderedDict()
            for i, res in enumerate(results):
                _results["Model " + str(i)] = res
            results = _results
        elif not isinstance(results, OrderedDict):
            _results = OrderedDict()
            for key in sorted(results.keys()):
                _results[key] = results[key]
            results = _results
        self._results = results

        for key in self._results:
            if not isinstance(self._results[key], self._supported):
                raise TypeError("Results from unknown model")
        precision = precision.lower().replace("-", "_")
        if precision not in ("tstats", "pvalues", "std_errors"):
            raise ValueError(
                "Unknown precision value. Must be one of 'tstats', 'std_errors' "
                "or 'pvalues'."
            )
        self._precision = precision

    def _get_series_property(self, name):
        out = [(k, getattr(v, name)) for k, v in self._results.items()]
        cols = [v[0] for v in out]
        values = concat([v[1] for v in out], 1)
        values.columns = cols
        return values

    def _get_property(self, name):
        out = OrderedDict()
        items = []
        for k, v in self._results.items():
            items.append(k)
            out[k] = getattr(v, name)
        return Series(out, name=name).loc[items]

    @property
    def nobs(self):
        """Parameters for all models"""
        return self._get_property("nobs")

    @property
    def params(self):
        """Parameters for all models"""
        return self._get_series_property("params")

    @property
    def tstats(self):
        """Parameter t-stats for all models"""
        return self._get_series_property("tstats")

    @property
    def std_errors(self):
        """Parameter t-stats for all models"""
        return self._get_series_property("std_errors")

    @property
    def pvalues(self):
        """Parameter p-vals for all models"""
        return self._get_series_property("pvalues")

    @property
    def rsquared(self):
        """Coefficients of determination (R**2)"""
        return self._get_property("rsquared")

    @property
    def f_statistic(self):
        """F-statistics and P-values"""
        out = self._get_property("f_statistic")
        out_df = DataFrame(
            np.empty((len(out), 2)), columns=["F stat", "P-value"], index=out.index
        )
        for loc in out.index:
            out_df.loc[loc] = out[loc].stat, out[loc].pval
        return out_df


def missing_warning(missing):
    """Utility function to perform missing value check and warning"""
    if not np.any(missing):
        return
    import linearmodels

    if linearmodels.WARN_ON_MISSING:
        import warnings

        warnings.warn(missing_value_warning_msg, MissingValueWarning)


def param_table(results, title, pad_bottom=False):
    """Formatted standard parameter table"""
    param_data = np.c_[
        np.asarray(results.params)[:, None],
        np.asarray(results.std_errors)[:, None],
        np.asarray(results.tstats)[:, None],
        np.asarray(results.pvalues)[:, None],
        results.conf_int(),
    ]
    data = []
    for row in param_data:
        txt_row = []
        for i, v in enumerate(row):
            f = _str
            if i == 3:
                f = pval_format
            txt_row.append(f(v))
        data.append(txt_row)
    header = ["Parameter", "Std. Err.", "T-stat", "P-value", "Lower CI", "Upper CI"]
    table_stubs = list(results.params.index)
    if pad_bottom:
        # Append blank row for spacing
        data.append([""] * 6)
        table_stubs += [""]

    return SimpleTable(
        data, stubs=table_stubs, txt_fmt=fmt_params, headers=header, title=title
    )


def format_wide(s, cols):
    """
    Format a list of strings.

    Parameters
    ----------
    s : List[str]
        List of strings to format
    cols : int
        Number of columns in output

    Returns
    -------
    List[List[str]]
        The joined list.
    """
    lines = []
    line = ""
    for i, val in enumerate(s):
        if line == "":
            line = val
            if i + 1 != len(s):
                line += ", "
        else:
            temp = line + val
            if i + 1 != len(s):
                temp += ", "
            if len(temp) > cols:
                lines.append([line])
                line = val
                if i + 1 != len(s):
                    line += ", "
            else:
                line = temp
    lines.append([line])
    return lines


def panel_to_frame(x, items, major_axis, minor_axis, swap=False):
    """
    Construct a multiindex DataFrame using Panel-like arguments

    Parameters
    ----------
    x : ndarray
        3-d array with size nite, nmajor, nminor
    items : list-like
        List like object with item labels
    major_axis : list-like
        List like object with major_axis labels
    minor_axis : list-like
        List like object with minor_axis labels
    swap : bool
        Swap is major and minor axes

    Notes
    -----
    This function is equivalent to

    Panel(x, items, major_axis, minor_axis).to_frame()

    if `swap` is True, it is equivalent to

    Panel(x, items, major_axis, minor_axis).swapaxes(1,2).to_frame()
    """
    nmajor = np.arange(len(major_axis))
    nminor = np.arange(len(minor_axis))
    final_levels = [major_axis, minor_axis]
    mi = MultiIndex.from_product([nmajor, nminor])
    if x is not None:
        shape = x.shape
        x = x.reshape((shape[0], shape[1] * shape[2])).T
    df = DataFrame(x, columns=items, index=mi)
    if swap:
        df.index = df.index.swaplevel()
        df.sort_index(inplace=True)
        final_levels = [minor_axis, major_axis]
    df.index.set_levels(final_levels, [0, 1], inplace=True)
    df.index.names = ["major", "minor"]
    return df


def quadratic_form_test(params, cov, restriction=None, value=None, formula=None):
    if formula is not None and restriction is not None:
        raise ValueError("restriction and formula cannot be used" "simultaneously.")
    if formula is not None:
        di = DesignInfo(list(params.index))
        lc = di.linear_constraint(formula)
        restriction, value = lc.coefs, lc.constants
    restriction = np.asarray(restriction)
    if value is None:
        value = np.zeros(restriction.shape[0])
    value = np.asarray(value).ravel()[:, None]
    diff = restriction @ params.values[:, None] - value
    rcov = restriction @ cov @ restriction.T
    stat = float(diff.T @ np.linalg.inv(rcov) @ diff)
    df = restriction.shape[0]
    null = "Linear equality constraint is valid"
    name = "Linear Equality Hypothesis Test"

    return WaldTestStatistic(stat, null, df, name=name)

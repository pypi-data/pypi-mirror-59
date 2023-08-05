from pandas_profiling.report.formatters import fmt_array
from pandas_profiling.visualisation.plot import mini_histogram, histogram
from pandas_profiling.report.presentation.core import (
    Table,
    Sequence,
    Image,
    Preview,
    FrequencyTable,
    Overview,
)
from pandas_profiling.report.structure.variables.render_common import render_common


def render_real(summary):
    template_variables = render_common(summary)

    if summary["min"] >= 0:
        name = "Real number (&Ropf;<sub>&ge;0</sub>)"
    else:
        name = "Real number (&Ropf;)"

    # Top
    info = Overview(summary["varid"], summary["varname"], name, summary["warnings"])

    table1 = Table(
        [
            {
                "name": "Distinct count",
                "value": summary["n_unique"],
                "fmt": "fmt",
                "class": "alert" if "n_unique" in summary["warn_fields"] else "",
            },
            {
                "name": "Unique (%)",
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_unique" in summary["warn_fields"] else "",
            },
            {
                "name": "Missing",
                "value": summary["n_missing"],
                "fmt": "fmt",
                "class": "alert" if "n_missing" in summary["warn_fields"] else "",
            },
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_missing" in summary["warn_fields"] else "",
            },
            {
                "name": "Infinite",
                "value": summary["n_infinite"],
                "fmt": "fmt",
                "class": "alert" if "n_infinite" in summary["warn_fields"] else "",
            },
            {
                "name": "Infinite (%)",
                "value": summary["p_infinite"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_infinite" in summary["warn_fields"] else "",
            },
        ]
    )

    table2 = Table(
        [
            {"name": "Mean", "value": summary["mean"], "fmt": "fmt"},
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt"},
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt"},
            {
                "name": "Zeros",
                "value": summary["n_zeros"],
                "fmt": "fmt",
                "class": "alert" if "n_zeros" in summary["warn_fields"] else "",
            },
            {
                "name": "Zeros (%)",
                "value": summary["p_zeros"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_zeros" in summary["warn_fields"] else "",
            },
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    histogram_bins = 10

    # TODO: replace with SmallImage...
    mini_histo = Image(
        mini_histogram(summary["histogram_data"], summary, histogram_bins),
        "Mini histogram",
    )

    template_variables["top"] = Sequence(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    quantile_statistics = Table(
        [
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt_numeric"},
            {"name": "5-th percentile", "value": summary["5%"], "fmt": "fmt_numeric"},
            {"name": "Q1", "value": summary["25%"], "fmt": "fmt_numeric"},
            {"name": "median", "value": summary["50%"], "fmt": "fmt_numeric"},
            {"name": "Q3", "value": summary["75%"], "fmt": "fmt_numeric"},
            {"name": "95-th percentile", "value": summary["95%"], "fmt": "fmt_numeric"},
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt_numeric"},
            {"name": "Range", "value": summary["range"], "fmt": "fmt_numeric"},
            {
                "name": "Interquartile range (IQR)",
                "value": summary["iqr"],
                "fmt": "fmt_numeric",
            },
        ],
        name="Quantile statistics",
    )

    descriptive_statistics = Table(
        [
            {
                "name": "Standard deviation",
                "value": summary["std"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Coefficient of variation (CV)",
                "value": summary["cv"],
                "fmt": "fmt_numeric",
            },
            {"name": "Kurtosis", "value": summary["kurtosis"], "fmt": "fmt_numeric"},
            {"name": "Mean", "value": summary["mean"], "fmt": "fmt_numeric"},
            {
                "name": "Median Absolute Deviation (MAD)",
                "value": summary["mad"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Skewness",
                "value": summary["skewness"],
                "fmt": "fmt_numeric",
                "class": "alert" if "skewness" in summary["warn_fields"] else "",
            },
            {"name": "Sum", "value": summary["sum"], "fmt": "fmt_numeric"},
            {"name": "Variance", "value": summary["variance"], "fmt": "fmt_numeric"},
        ],
        name="Descriptive statistics",
    )

    statistics = Sequence(
        [quantile_statistics, descriptive_statistics],
        anchor_id="{varid}statistics".format(varid=summary["varid"]),
        name="Statistics",
        sequence_type="grid",
    )

    seqs = [
        Image(
            histogram(summary["histogram_data"], summary, histogram_bins),
            alt="Histogram",
            caption="<strong>Histogram with fixed size bins</strong> (bins={})".format(
                histogram_bins
            ),
            name="Histogram",
            anchor_id="{varid}histogram".format(varid=summary["varid"]),
        )
    ]

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common values",
        anchor_id="{varid}common_values".format(varid=summary["varid"]),
    )

    evs = Sequence(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name="Minimum 5 values",
                anchor_id="{varid}firstn".format(varid=summary["varid"]),
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name="Maximum 5 values",
                anchor_id="{varid}lastn".format(varid=summary["varid"]),
            ),
        ],
        sequence_type="tabs",
        name="Extreme values",
        anchor_id="{varid}extreme_values".format(varid=summary["varid"]),
    )

    if "histogram_bins_bayesian_blocks" in summary:
        histo_dyn = Image(
            histogram(
                summary["histogram_data"],
                summary,
                summary["histogram_bins_bayesian_blocks"],
            ),
            alt="Histogram",
            caption='<strong>Histogram with variable size bins</strong> (bins={}, <a href="https://ui.adsabs.harvard.edu/abs/2013ApJ...764..167S/abstract" target="_blank">"bayesian blocks"</a> binning strategy used)'.format(
                fmt_array(summary["histogram_bins_bayesian_blocks"], threshold=5)
            ),
            name="Dynamic Histogram",
            anchor_id="{varid}dynamic_histogram".format(varid=summary["varid"]),
        )

        seqs.append(histo_dyn)

    template_variables["bottom"] = Sequence(
        [
            statistics,
            Sequence(
                seqs,
                sequence_type="tabs",
                name="Histogram(s)",
                anchor_id="{varid}histograms".format(varid=summary["varid"]),
            ),
            fq,
            evs,
        ],
        sequence_type="tabs",
        anchor_id="{varid}bottom".format(varid=summary["varid"]),
    )

    return template_variables

from pandas_profiling.report.formatters import fmt_array
from pandas_profiling.visualisation.plot import mini_histogram, histogram
from pandas_profiling.report.presentation.core import (
    FrequencyTable,
    Sequence,
    Image,
    Preview,
    Table,
    Overview,
)
from pandas_profiling.report.structure.variables.render_common import render_common


def render_count(summary):
    template_variables = render_common(summary)

    # Top
    info = Overview(
        summary["varid"],
        summary["varname"],
        "Real number (&Ropf; / &Ropf;<sub>&ge;0</sub>)",
        summary["warnings"],
    )

    table1 = Table(
        [
            {"name": "Distinct count", "value": summary["n_unique"], "fmt": "fmt"},
            {"name": "Unique (%)", "value": summary["p_unique"], "fmt": "fmt_percent"},
            {"name": "Missing", "value": summary["n_missing"], "fmt": "fmt"},
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
            },
            # {'name': 'Infinite', 'value': summary['n_infinite'], 'fmt': 'fmt'},
            # {'name': 'Infinite (%)', 'value': summary['p_infinite'], 'fmt': 'fmt_percent'},
        ]
    )

    table2 = Table(
        [
            {"name": "Mean", "value": summary["mean"], "fmt": "fmt"},
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt"},
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt"},
            {"name": "Zeros", "value": summary["n_zeros"], "fmt": "fmt"},
            {"name": "Zeros (%)", "value": summary["p_zeros"], "fmt": "fmt_percent"},
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    # TODO: replace with SmallImage...
    mini_histo = Image(
        mini_histogram(summary["histogram_data"], summary, summary["histogram_bins"]),
        "Mini histogram",
    )

    template_variables["top"] = Sequence(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    quantile_statistics = {
        "name": "Quantile statistics",
        "items": [
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt_numeric"},
            {
                "name": "5-th percentile",
                "value": summary["quantile_5"],
                "fmt": "fmt_numeric",
            },
            {"name": "Q1", "value": summary["quantile_25"], "fmt": "fmt_numeric"},
            {"name": "median", "value": summary["quantile_50"], "fmt": "fmt_numeric"},
            {"name": "Q3", "value": summary["quantile_75"], "fmt": "fmt_numeric"},
            {
                "name": "95-th percentile",
                "value": summary["quantile_95"],
                "fmt": "fmt_numeric",
            },
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt_numeric"},
            {"name": "Range", "value": summary["range"], "fmt": "fmt_numeric"},
            {
                "name": "Interquartile range",
                "value": summary["iqr"],
                "fmt": "fmt_numeric",
            },
        ],
    }

    descriptive_statistics = {
        "name": "Descriptive statistics",
        "items": [
            {
                "name": "Standard deviation",
                "value": summary["std"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Coefficient of variation",
                "value": summary["cv"],
                "fmt": "fmt_numeric",
            },
            {"name": "Kurtosis", "value": summary["kurt"], "fmt": "fmt_numeric"},
            {"name": "Mean", "value": summary["mean"], "fmt": "fmt_numeric"},
            {"name": "MAD", "value": summary["mad"], "fmt": "fmt_numeric"},
            {"name": "Skewness", "value": summary["skew"], "fmt": "fmt_numeric"},
            {"name": "Sum", "value": summary["sum"], "fmt": "fmt_numeric"},
            {"name": "Variance", "value": summary["var"], "fmt": "fmt_numeric"},
        ],
    }

    # TODO: Make sections data structure
    # statistics = ItemRenderer(
    #     'statistics',
    #     'Statistics',
    #     'table',
    #     [
    #         quantile_statistics,
    #         descriptive_statistics
    #     ]
    # )

    seqs = [
        Image(
            histogram(summary["histogram_data"], summary, summary["histogram_bins"]),
            alt="Histogram",
            caption="<strong>Histogram with fixed size bins</strong> (bins={})".format(
                summary["histogram_bins"]
            ),
            name="Histogram",
            anchor_id="histogram",
        )
    ]

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common values",
        anchor_id="common_values",
    )

    evs = Sequence(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name="Minimum 5 values",
                anchor_id="firstn",
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name="Maximum 5 values",
                anchor_id="lastn",
            ),
        ],
        sequence_type="tabs",
        name="Extreme values",
        anchor_id="extreme_values",
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
            anchor_id="dynamic_histogram",
        )

        seqs.append(histo_dyn)

    template_variables["bottom"] = Sequence(
        [
            # statistics,
            Sequence(
                seqs, sequence_type="tabs", name="Histogram(s)", anchor_id="histograms"
            ),
            fq,
            evs,
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    return template_variables

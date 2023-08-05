from pandas_profiling.visualisation.plot import mini_histogram, histogram
from pandas_profiling.report.presentation.core import (
    Image,
    Preview,
    Sequence,
    Table,
    Overview,
)


def render_date(summary):
    # TODO: render common?
    template_variables = {}
    # Top
    info = Overview(summary["varid"], summary["varname"], "Date", [])

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
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    table2 = Table(
        [
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt"},
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt"},
            # {'name': '', 'value': '', 'fmt': 'fmt'},
            # {'name': '', 'value': '', 'fmt': 'fmt'},
            # {'name': '', 'value': '', 'fmt': 'fmt'},
            # {'name': '', 'value': '', 'fmt': 'fmt'},
        ]
    )

    mini_histo = Image(
        mini_histogram(summary["histogram_data"], summary, summary["histogram_bins"]),
        "Mini histogram",
    )

    template_variables["top"] = Sequence(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    # Bottom
    bottom = Sequence(
        [
            Image(
                histogram(
                    summary["histogram_data"], summary, summary["histogram_bins"]
                ),
                alt="Histogram",
                caption="Histogram",
                name="Histogram",
                anchor_id="{varid}histogram".format(varid=summary["varid"]),
            )
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    template_variables["bottom"] = bottom

    return template_variables

from pandas_profiling.visualisation.plot import scatter_complex
from pandas_profiling.report.presentation.core import (
    HTML,
    Image,
    Preview,
    Sequence,
    Table,
    Overview,
)


def render_complex(summary):
    template_variables = {}

    # Top
    info = Overview(
        summary["varid"],
        summary["varname"],
        "Complex number (&Copf;)",
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
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    table2 = Table(
        [
            {"name": "Mean", "value": summary["mean"], "fmt": "fmt"},
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt"},
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt"},
            {"name": "Zeros", "value": summary["n_zeros"], "fmt": "fmt"},
            {"name": "Zeros (%)", "value": summary["p_zeros"], "fmt": "fmt_percent"},
        ]
    )

    placeholder = HTML("")

    template_variables["top"] = Sequence(
        [info, table1, table2, placeholder], sequence_type="grid"
    )

    # Bottom
    items = [
        Image(
            scatter_complex(summary["scatter_data"]),
            alt="Scatterplot",
            caption="Scatterplot in the complex plane",
            name="Scatter",
            anchor_id="{varid}scatter".format(varid=summary["varid"]),
        )
    ]

    bottom = Sequence(items, sequence_type="tabs", anchor_id=summary["varid"])

    template_variables["bottom"] = bottom

    return template_variables

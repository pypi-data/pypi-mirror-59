from ipywidgets import widgets

from pandas_profiling.report.presentation.abstract.renderable import Renderable
from pandas_profiling.report.presentation.core.sequence import Sequence


def get_name(item: Renderable):
    if hasattr(item, "name"):
        return item.name
    else:
        return item.anchor_id


def get_tabs(items):
    children = []
    titles = []
    for item in items:
        children.append(item.render())
        titles.append(get_name(item))

    tab = widgets.Tab()
    tab.children = children
    for id, title in enumerate(titles):
        tab.set_title(id, title)
    return tab


def get_list(items):
    return widgets.VBox(
        [
            widgets.VBox(
                [
                    widgets.HTML("<strong>{name}</strong>".format(name=get_name(item))),
                    item.render(),
                ]
            )
            for item in items
        ]
    )


def get_row(items):
    if len(items) == 1:
        layout = widgets.Layout(width="100%", grid_template_columns="100%")
    elif len(items) == 2:
        layout = widgets.Layout(width="100%", grid_template_columns="50% 50%")
    elif len(items) == 3:
        layout = widgets.Layout(width="100%", grid_template_columns="25% 25% 50%")
    elif len(items) == 4:
        layout = widgets.Layout(width="100%", grid_template_columns="25% 25% 25% 25%")
    else:
        raise ValueError("Layout undefined for this number of columns")

    return widgets.GridBox([item.render() for item in items], layout=layout)


def get_accordion(items):
    children = []
    titles = []
    for item in items:
        children.append(item.render())
        titles.append(get_name(item))

    accordion = widgets.Accordion(children=children)
    for id, title in enumerate(titles):
        accordion.set_title(id, title)

    return accordion


class WidgetSequence(Sequence):
    def render(self):
        if self.sequence_type == "list":
            widget = get_list(self.content["items"])
        elif self.sequence_type == "variable":
            i1 = self.content["items"][0].render()
            i2 = self.content["items"][1].render()
            toggle = widgets.ToggleButton(description="Toggle details")

            def hide_slider(widg):
                if widg["new"]:
                    i2.layout.display = ""
                else:
                    i2.layout.display = "none"

            toggle.observe(hide_slider, names=["value"])
            i2.layout.display = "none"

            toggle_box = widgets.HBox([toggle])
            toggle_box.layout.align_items = "flex-end"
            toggle_box.layout.object_position = "right center"
            toggle_box.layout.width = "100%"

            return widgets.VBox([i1, toggle_box, i2])

        elif self.sequence_type in ["tabs", "sections"]:
            widget = get_tabs(self.content["items"])
        elif self.sequence_type == "accordion":
            widget = get_accordion(self.content["items"])
        elif self.sequence_type == "grid":
            widget = get_row(self.content["items"])
        else:
            raise ValueError("widget type not understood", self.sequence_type)

        return widget

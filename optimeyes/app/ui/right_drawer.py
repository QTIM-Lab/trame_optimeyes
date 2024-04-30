from trame.widgets import vuetify3 as vuetify, html

COLORS = [
    (255, 0, 0),
    (255, 255, 0),
    (255, 255, 255),
    (0, 255, 0),
    (0, 0, 255),
]


class RightDrawer(vuetify.VNavigationDrawer):
    def __init__(self):
        super().__init__(
            width=250,
            location="right",
            model_value=(
                "['eraser', 'brush', 'polygon', 'freeform_1', 'freeform_2'].includes(tool_active)",
            ),
        )

        self.server.state.setdefault("brush_color", (255, 0, 0))
        with self:
            with vuetify.VTabs(
                v_model=("drawer_right_mode", "brush"),
                align_tabs="center",
                grow=True,
            ):
                with vuetify.VTab(value="brush"):
                    vuetify.VIcon("mdi-brush")
                with vuetify.VTab(value="polygon"):
                    vuetify.VIcon("mdi-vector-polygon")
            with vuetify.VWindow(v_model="drawer_right_mode"):
                with vuetify.VWindowItem(value="brush"):
                    with vuetify.VList():
                        for c in COLORS:
                            with vuetify.VListItem(
                                click=f"brush_color = [{c[0]}, {c[1]}, {c[2]}, 255]"
                            ):
                                with html.Div(
                                    classes="d-flex align-center justify-space-around"
                                ):
                                    html.Div(
                                        style=f"width: 1rem; height: 1rem; background: rgb({c[0]}, {c[1]}, {c[2]}); border: solid 1px #333;"
                                    )
                                    vuetify.VListItemTitle("segmentation A")

                with vuetify.VWindowItem(value="polygon"):
                    html.Div("...polygon...")

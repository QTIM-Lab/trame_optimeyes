from trame.widgets import vuetify3 as vuetify, html


class RightDrawer(vuetify.VNavigationDrawer):
    def __init__(self):
        super().__init__(
            width=250,
            location="right",
            model_value=(
                "['eraser', 'brush', 'polygon', 'freeform_1', 'freeform_2'].includes(tool_active)",
            ),
        )

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
                    html.Div("...brush...")
                with vuetify.VWindowItem(value="polygon"):
                    html.Div("...polygon...")

from trame.widgets import vuetify3 as vuetify, html
from trame.decorators import TrameApp, change

COLORS = [
    (255, 0, 0),
    (255, 255, 0),
    (255, 255, 255),
    (0, 255, 0),
    (0, 0, 255),
]


@TrameApp()
class RightDrawer(vuetify.VNavigationDrawer):
    def __init__(self):
        super().__init__(
            width=250,
            location="right",
            model_value=("['brush'].includes(tool_active)",),
        )

        # FIXME - begin
        self.state.seg_classes = [
            {"id": 1, "color": [255, 0, 0], "name": "Red"},
            {"id": 2, "color": [255, 0, 255], "name": "Yellow"},
            {"id": 3, "color": [0, 255, 0], "name": "Green"},
            {"id": 4, "color": [0, 0, 255], "name": "Blue"},
        ]
        self.state.seg_class_active = [1]
        self.state.polygons = [
            {"id": 1, "color": [255, 0, 0], "name": "Red part 1"},
            {"id": 2, "color": [255, 0, 0], "name": "Red part 2"},
        ]
        # FIXME - end

        self.server.state.setdefault("brush_color", (255, 0, 0))
        with self:
            with vuetify.VExpansionPanels(
                flat=True,
                static=True,
                multiple=True,
                v_model=("panels", ["seg_classes"]),
            ):
                with vuetify.VExpansionPanel(
                    value="seg_classes",
                    static=True,
                    expand_icon="mdi-format-list-bulleted-type",
                    title="Segmentation classes",
                    classes="mt-0",
                ):
                    with vuetify.VExpansionPanelText(classes="px-0 mx-n6 py-0"):
                        with vuetify.VList(
                            items=("seg_classes", []),
                            item_title="name",
                            item_value="id",
                            density="compact",
                            v_model_selected=("seg_class_active", None),
                            mandatory=True,
                            __properties=[("v_model_selected", "v-model:selected")],
                        ):
                            with vuetify.Template(
                                raw_attrs=['v-slot:prepend="{ item }"']
                            ):
                                html.Div(
                                    classes="mr-2",
                                    style=(
                                        "`width: 1rem; height: 1rem; background: rgb(${item.color[0]}, ${item.color[1]}, ${item.color[2]}); border: solid 1px #333;`",
                                    ),
                                )
                with vuetify.VExpansionPanel(
                    value="tools",
                    static=True,
                    expand_icon="mdi-brush",
                    title="Tools",
                    classes="mt-0",
                ):
                    with vuetify.VExpansionPanelText(classes="px-0 mx-n6 py-0"):
                        with vuetify.VBtnToggle(
                            v_model=("active_brush", "brush"),
                            mandatory=True,
                            density="compact",
                        ):
                            with vuetify.VBtn(value="navigation"):
                                vuetify.VIcon("mdi-gesture-tap")
                            with vuetify.VBtn(value="eraser"):
                                vuetify.VIcon("mdi-eraser")
                            with vuetify.VBtn(value="brush"):
                                vuetify.VIcon("mdi-brush")
                            with vuetify.VBtn(value="polygon"):
                                vuetify.VIcon("mdi-vector-polygon")

                        with html.Div(
                            v_show="['eraser', 'brush'].includes(active_brush)"
                        ):
                            vuetify.VSlider(
                                prepend_icon="mdi-brush",
                                v_model=("brush_size", 5),
                                min=1,
                                max=50,
                                step=1,
                                classes="mx-4",
                            )

                        with html.Div(v_show="['polygon'].includes(active_brush)"):
                            with vuetify.VList(
                                items=("polygons", []),
                                item_title="name",
                                item_value="id",
                                density="compact",
                                v_model_selected=("polygon_active", None),
                                __properties=[("v_model_selected", "v-model:selected")],
                            ):
                                with vuetify.Template(
                                    raw_attrs=['v-slot:prepend="{ item }"']
                                ):
                                    html.Div(
                                        classes="mr-2",
                                        style=(
                                            "`width: 1rem; height: 1rem; background: rgb(${item.color[0]}, ${item.color[1]}, ${item.color[2]}); border: solid 1px #333;`",
                                        ),
                                    )

    @property
    def state(self):
        return self.server.state

    @change("seg_class_active", "active_brush")
    def on_active_class_change(self, active_brush, seg_class_active, seg_classes, **_):
        selected_class = next(
            item for item in seg_classes if seg_class_active[0] == item.get("id")
        )
        if active_brush == "eraser":
            self.state.brush_color = [0, 0, 0, 0]
        else:
            self.state.brush_color = [*selected_class.get("color"), 255]

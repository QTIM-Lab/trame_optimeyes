from trame.widgets import vuetify3 as vuetify


class Toolbar(vuetify.VAppBar):
    def __init__(self, reload=None):
        super().__init__(density="compact")

        with self:
            with vuetify.Template(v_slot_prepend=True):
                with vuetify.VAppBarNavIcon(
                    click="drawer_left_open = !drawer_left_open"
                ):
                    vuetify.VIcon("mdi-eye-outline")
            vuetify.VAppBarTitle("OptimEYES")

            with vuetify.VBtnToggle(v_model=("tool_active", "navigation")):
                with vuetify.VBtn(value="navigation"):
                    vuetify.VIcon("mdi-gesture-tap")
                with vuetify.VBtn(value="ruler"):
                    vuetify.VIcon("mdi-ruler")
                with vuetify.VBtn(value="eraser"):
                    vuetify.VIcon("mdi-eraser")
                with vuetify.VBtn(value="brush"):
                    vuetify.VIcon("mdi-brush")
                with vuetify.VBtn(value="polygon"):
                    vuetify.VIcon("mdi-vector-polygon")
                with vuetify.VBtn(value="freeform_1"):
                    vuetify.VIcon("mdi-gesture")
                with vuetify.VBtn(value="freeform_2"):
                    vuetify.VIcon("mdi-draw")

            vuetify.VSpacer()

            if reload:
                with vuetify.VBtn(icon=True, click=reload):
                    vuetify.VIcon("mdi-refresh")

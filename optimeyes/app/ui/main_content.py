from trame.widgets import vuetify3 as vuetify, html, vtk


class MainContent(vuetify.VMain):
    def __init__(self, render_window):
        super().__init__()

        with self:
            with vuetify.VSystemBar(classes="bg-black"):
                html.Div("Task: ...")
                vuetify.VDivider(vertical=True, classes="mx-2", style="opacity: 0.8")
                html.Div("Image: {{batch_images[batch_selection[0]] }}")
                vuetify.VDivider(vertical=True, classes="mx-2", style="opacity: 0.8")
                html.Div(
                    "Index: {{ batch_selection[0] + 1 }} of {{ batch_images.length }} "
                )
                vuetify.VSpacer()
                html.Div(
                    "{{ batch_selection[0] }}",
                    style="user-select: none;",
                    v_show="batch_selection[0]",
                )
                with vuetify.VBtn(
                    density="compact",
                    flat=True,
                    icon=True,
                    size="small",
                    color="rgba(0,0,0,0)",
                    v_show="batch_selection[0]",
                    click="batch_selection = [batch_selection[0] - 1]",
                ):
                    vuetify.VIcon("mdi-menu-left", classes="bg-black")

                with vuetify.VBtn(
                    density="compact",
                    flat=True,
                    icon=True,
                    size="small",
                    color="rgba(0,0,0,0)",
                    v_show="batch_selection[0] + 1 < batch_images.length",
                    click="batch_selection = [batch_selection[0] + 1]",
                ):
                    vuetify.VIcon("mdi-menu-right", classes="bg-black")
                html.Div(
                    "{{ batch_selection[0] + 2 }}",
                    v_show="batch_selection[0] + 1 < batch_images.length",
                    classes="text-left",
                    style="user-select: none; width: 30px;",
                )
                with vuetify.VBtn(
                    density="compact",
                    flat=True,
                    icon=True,
                    size="small",
                    color="rgba(0,0,0,0)",
                    click=self.server.controller.view_reset_color,
                ):
                    vuetify.VIcon("mdi-undo", classes="bg-black")
                with vuetify.VBtn(
                    density="compact",
                    flat=True,
                    icon=True,
                    size="small",
                    color="rgba(0,0,0,0)",
                    click=self.server.controller.view_reset_camera,
                ):
                    vuetify.VIcon("mdi-crop-free", classes="bg-black")

            with vtk.VtkRemoteView(render_window, interactive_ratio=1) as view:
                self.server.controller.view_update = view.update
                self.server.controller.view_reset_camera = view.reset_camera

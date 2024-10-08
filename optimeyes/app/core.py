from pathlib import Path
from trame.app import get_server
from trame.decorators import TrameApp, change, controller
from trame.ui.vuetify3 import VAppLayout
from trame.widgets.vuetify3 import VLayout

from . import ui
from .vtk import AnnotationEngine


@TrameApp()
class OptimEyes:
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.annotation_engine = AnnotationEngine(self.server)
        self.active_directory = None

        # handle cli
        self.server.cli.add_argument("--batch", help="Path to batch directory")
        args, _ = self.server.cli.parse_known_args()

        if args.batch:
            self.active_directory = Path(args.batch).resolve()
            self.load_batch(self.active_directory)
            self.server.enable_module(dict(serve={"data": str(self.active_directory)}))

        self._build_ui()

    @property
    def state(self):
        return self.server.state

    def load_batch(self, directory):
        self.state.batch_images = [file.name for file in Path(directory).glob("*.jpg")]

    @change("batch_selection")
    def _on_batch_selection(self, batch_selection, batch_images, **_):
        if self.active_directory:
            file_to_load = str(self.active_directory / batch_images[batch_selection[0]])
            self.annotation_engine.load_image(file_to_load)

    @controller.set("view_reset_color")
    def _on_window_level_reset(self):
        self.annotation_engine.reset_color()

    @controller.set("update_brush_scale")
    def _on_zoom_change(self):
        self.annotation_engine.update_brush_scale()

    @change("tool_active", "active_brush")
    def _on_interaction_mode_change(self, tool_active, active_brush, **kwargs):
        if tool_active == "brush":
            tool_active = active_brush
        self.annotation_engine.select_interactor(tool_active)

    @change("brush_color")
    def _on_brush_color_change(self, brush_color, **kwargs):
        self.annotation_engine.set_active_color(brush_color)

    def _build_ui(self):
        extra_args = {}
        if self.server.hot_reload:
            ui.reload(ui)
            extra_args["reload"] = self._build_ui

        with VAppLayout(self.server, full_height=True) as self.ui:
            with VLayout():
                ui.Toolbar(**extra_args)
                ui.LeftDrawer()
                ui.RightDrawer()
                ui.MainContent(render_window=self.annotation_engine.render_window)


def main():
    app = OptimEyes()
    app.server.start()

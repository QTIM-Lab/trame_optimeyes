from trame.widgets import vuetify3 as vuetify, html
from trame_client.utils.defaults import TrameDefault


class LeftDrawer(vuetify.VNavigationDrawer):
    def __init__(self):
        super().__init__(
            v_model=("drawer_left_open", True),
            width=150,
        )

        with self:
            with vuetify.VList(
                v_model_selected=("batch_selection", [0]),
                selectable=True,
                mandatory=True,
                active_class="elevation-1 bg-grey-darken-1",
                active_color="grey-darken-1",
                items=(
                    "batch_images.map((title, value) => ({ title, value }))",
                    TrameDefault(batch_images=[]),
                ),
                density="compact",
                __properties=[
                    ("v_model_selected", "v-model:selected"),
                    "selectable",
                ],
            ):
                with vuetify.Template(v_slot_title="{ item }"):
                    vuetify.VImg(
                        src=("`data/${item.title}`",),
                    )

import os
import itk
import vtk

from trame.app import get_server
from trame.widgets import vuetify, vtk as vtk_widgets
from trame.ui.vuetify import SinglePageLayout

images_path = "images"
os.listdir(images_path)
# image1_name = os.path.join(images_path, "JPEGReader_1.png")
image1_name = os.path.join(images_path, "MRN 803567 2_fixed.jpg")
# image2_name = os.path.join(images_path, "JPEGReader_2.png")
image2_name = os.path.join(images_path, "MRN 803567 2_aff_registered.jpg")


# Read Images
image1 = itk.imread(image1_name)
image2 = itk.imread(image2_name)

image1_vtk = itk.vtk_image_from_image(image1)
image2_vtk = itk.vtk_image_from_image(image2)

checker = vtk.vtkImageCheckerboard()
checker.SetInputData(0, image1_vtk)
checker.SetInputData(1, image2_vtk)
checker.SetNumberOfDivisions(3, 3, 1)

checkerActor = vtk.vtkImageActor()
checkerActor.GetMapper().SetInputConnection(checker.GetOutputPort())

viewer = vtk.vtkImageViewer2()
viewer.SetInputConnection(checker.GetOutputPort())

interactor = vtk.vtkRenderWindowInteractor()
viewer.SetupInteractor(interactor)

checkerWidget = vtk.vtkCheckerboardWidget()
checkerWidget.SetInteractor(interactor)

checkerRep = checkerWidget.GetRepresentation()
checkerRep.SetImageActor(checkerActor)
checkerRep.SetCheckerboard(checker)

viewer.GetRenderer().AddActor(checkerActor)

viewer.Render()
checkerWidget.On()


# Setup trame server
server = get_server()
state, ctrl = server.state, server.controller


@state.change("widget_active")
def on_widget_change(widget_active, **kwargs):
    if widget_active:
        checkerWidget.On()
    else:
        checkerWidget.Off()
    ctrl.view_update()


# Build UI
with SinglePageLayout(server) as layout:
    with layout.toolbar as toolbar:
        layout.title.set_text("Checkboard Viewer")
        vuetify.VSpacer()
        vuetify.VCheckbox(
            v_model=("widget_active", True),
            off_icon="mdi-gesture-tap",
            on_icon="mdi-gesture-tap",
            dense=True,
            hide_details=True,
            classes="my-0",
        )
        with vuetify.VBtn(icon=True, click=ctrl.view_reset_camera):
            vuetify.VIcon("mdi-crop-free")

    with layout.content:
        with vuetify.VContainer(classes="fluid fill-height pa-0"):
            with vtk_widgets.VtkRemoteView(viewer.GetRenderWindow()) as view:
                ctrl.view_update = view.update
                ctrl.view_reset_camera = view.reset_camera

# Start server
server.start()

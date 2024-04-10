"""
Need trame to work: `pip install trame`
"""

import os, vtk

from trame.app import get_server
from trame.widgets import vuetify, vtk as vtk_widgets
from trame.ui.vuetify import SinglePageLayout

# Attempt with https://kitware.github.io/vtk-examples/site/Java/IO/JPEGReader/
# vtk.vtkNativeLibrary # Didn't work, but maybe we don't need
vtk.vtkRenderWindowInteractor
# vtk.vtkImageReader2 # Need but we have already from vtk.vtkJPEGReader via inheritance
vtk.vtkJPEGReader  # inherits from vtk.vtkImageReader2
vtk.vtkNamedColors
vtk.vtkImageViewer2

images_path = "images"
os.listdir(images_path)
image = os.path.join(images_path, "MRN 803567 2_aff_registered.jpg")


# The following is python transcribed from java code almost exactly
# Colors
colors = vtk.vtkNamedColors()

# Read Image
jpegReader = vtk.vtkJPEGReader()
jpegReader.SetFileName(image)

# Visualize
imageViewer2 = vtk.vtkImageViewer2()
imageViewer2.SetInputConnection(jpegReader.GetOutputPort())
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
imageViewer2.SetupInteractor(renderWindowInteractor)
imageViewer2.Render()
imageViewer2.GetRenderer().ResetCamera()
imageViewer2.GetRenderer().SetBackground(colors.GetColor3d("DarkSlateGray"))
imageViewer2.GetRenderWindow().SetWindowName("JPEGReader")

# ---------------------------------------
# Disable regular VTK event handling
# ---------------------------------------
# imageViewer2.Render()
# renderWindowInteractor.Start()
# ---------------------------------------

# Setup trame server
server = get_server()
ctrl = server.controller

# Build UI
with SinglePageLayout(server) as layout:
    with layout.toolbar as toolbar:
        layout.title.set_text("JPEG Viewer")
        vuetify.VSpacer()
        with vuetify.VBtn(icon=True, click=ctrl.view_reset_camera):
            vuetify.VIcon("mdi-crop-free")

    with layout.content:
        with vuetify.VContainer(classes="fluid fill-height pa-0"):
            with vtk_widgets.VtkRemoteView(imageViewer2.GetRenderWindow()) as view:
                ctrl.view_update = view.update
                ctrl.view_reset_camera = view.reset_camera

# Start server
server.start()

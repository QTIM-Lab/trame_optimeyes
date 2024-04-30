from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkCommonDataModel import vtkVector3d
from vtkmodules.vtkInteractionStyle import (
    vtkInteractorStyleImage,
    vtkInteractorStyleUser,
)
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindowInteractor,
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderer,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa


class AnnotationEngine:
    def __init__(self, server):
        self.server = server

        self.current_image = None
        self.current_extent = None
        self.display_coord = vtkVector3d()
        self.active_color = [255, 0, 0, 255]

        # vtk viewer
        self.render_window = vtkRenderWindow()
        self.render_window.OffScreenRenderingOn()

        self.renderer = vtkRenderer()
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.renderer.SetBackground(0.5, 0.5, 0.5)

        self.render_window.AddRenderer(self.renderer)
        self.interactor = vtkRenderWindowInteractor()
        self.render_window.SetInteractor(self.interactor)
        self.interactor_style_image = vtkInteractorStyleImage()
        self.interactor_style_paint = vtkInteractorStyleUser()
        self.interactor.SetInteractorStyle(self.interactor_style_image)

        # Paint interactor setup
        self.interactor_style_paint.AddObserver(
            vtkCommand.MouseMoveEvent, self.on_paint
        )

        # image rendering
        self.image_actor = vtkImageActor()
        self.image_reader = vtkJPEGReader()
        self.image_actor.GetMapper().SetInputConnection(
            self.image_reader.GetOutputPort()
        )

        # painting
        self.painting_canvas = vtkImageCanvasSource2D()
        self.painting_actor = vtkImageActor()
        self.painting_actor.GetMapper().SetInputConnection(
            self.painting_canvas.GetOutputPort()
        )
        # self.painting_actor.SetPosition(0, 0, 1)
        # self.painting_actor.PickableOff()

        self.painting_canvas.SetNumberOfScalarComponents(4)
        self.painting_canvas.SetScalarType(3)

        # Fill renderer
        self.renderer.AddViewProp(self.painting_actor)
        self.renderer.AddViewProp(self.image_actor)

    def update(self):
        self.server.controller.view_update()

    def set_active_color(self, color_rgba):
        self.active_color = color_rgba
        self.painting_canvas.SetDrawColor(*self.active_color)

    def select_interactor(self, mode):
        if mode == "navigation":
            self.interactor.SetInteractorStyle(self.interactor_style_image)
        elif mode == "brush":
            self.painting_canvas.SetDrawColor(*self.active_color)
            self.interactor.SetInteractorStyle(self.interactor_style_paint)
        elif mode == "eraser":
            self.painting_canvas.SetDrawColor(0, 0, 0, 0)
            self.interactor.SetInteractorStyle(self.interactor_style_paint)
        else:
            self.interactor.SetInteractorStyle(self.interactor_style_image)

    def on_paint(self, style: vtkInteractorStyleUser, event):
        btn = style.GetButton()
        x_y_0 = style.GetOldPos()
        x_y_1 = style.GetLastPos()
        self.display_coord[0] = x_y_0[0]
        self.display_coord[1] = x_y_0[1]
        world_coord_0 = self.renderer.DisplayToWorld(self.display_coord)
        self.display_coord[0] = x_y_1[0]
        self.display_coord[1] = x_y_1[1]
        world_coord_1 = self.renderer.DisplayToWorld(self.display_coord)
        if btn:
            ijk = [0, 0, 0]
            self.current_image.TransformPhysicalPointToContinuousIndex(
                world_coord_0, ijk
            )
            i_0 = round(ijk[0])
            j_0 = round(ijk[1])
            self.current_image.TransformPhysicalPointToContinuousIndex(
                world_coord_1, ijk
            )
            i_1 = round(ijk[0])
            j_1 = round(ijk[1])
            self.painting_canvas.FillTube(i_0, j_0, i_1, j_1, 5)
            self.painting_canvas.DrawCircle(i_0, j_0, 5)
            self.painting_canvas.DrawCircle(i_1, j_1, 5)
            self.update()

    def reset_color(self):
        self.image_actor.GetProperty().SetColorLevel(127.5)
        self.image_actor.GetProperty().SetColorWindow(255)
        self.update()

    def reset_camera(self):
        self.render_window.Render()
        self.renderer.ResetCamera()
        self.update()

    def load_image(self, image_path):
        self.image_reader.SetFileName(image_path)

        # Sync canvas
        self.image_reader.Update()
        self.current_image = self.image_reader.GetOutput()
        self.current_extent = self.current_image.GetExtent()
        self.painting_canvas.SetExtent(self.current_extent)
        self.painting_canvas.SetDrawColor(0, 0, 0, 0)
        self.painting_canvas.FillBox(
            0, self.current_extent[1], 0, self.current_extent[3]
        )
        self.painting_canvas.SetDrawColor(255, 0, 0, 255)
        self.painting_canvas.FillTube(
            0, 0, self.current_extent[1], self.current_extent[3], 5
        )

        self.reset_color()
        self.reset_camera()

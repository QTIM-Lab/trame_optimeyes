from trame.decorators import TrameApp, change, controller

from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkCommonCore import vtkCommand, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkVector3d, vtkPolyData, vtkCellArray
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
    vtkPolyDataMapper,
    vtkActor,
)

import vtkmodules.vtkRenderingOpenGL2  # noqa


class Position:
    def __init__(self):
        self.display = vtkVector3d()
        self.world = vtkVector3d()


class Polygon:
    def __init__(self, name="Polygon", category_id=1):
        self.name = name
        self.cat_id = category_id
        self.polyline = vtkPolyData()
        self.points = vtkPoints()
        self.lines = vtkCellArray()
        self.polyline.SetPoints(self.points)
        self.polyline.SetLines(self.lines)
        self.mapper = vtkPolyDataMapper()
        self.actor = vtkActor()

        self.actor.GetProperty().SetLineWidth(5)
        self.actor.GetProperty().SetColor(1, 0, 0)
        self.actor.SetVisibility(0)
        self.actor.SetMapper(self.mapper)
        self.mapper.SetInputData(self.polyline)

    def show(self, visibility):
        self.actor.SetVisibility(1 if visibility else 0)

    @property
    def color(self):
        c = self.actor.GetProperty().GetColor()
        return [
            int(c[0] * 255),
            int(c[1] * 255),
            int(c[2] * 255),
        ]

    @color.setter
    def color(self, color):
        print(f"{color=}")
        self.actor.GetProperty().SetColor(color[0], color[1], color[2])

    def set_line_width(self, width):
        self.actor.GetProperty().SetLineWidth(width)

    def insert_point(self, position):
        idx = self.points.InsertNextPoint(position)
        self.points.Modified()
        if idx == 1:
            self.lines.InsertNextCell(2)
            self.lines.InsertCellPoint(0)
            self.lines.InsertCellPoint(1)
        if idx > 0:
            self.lines.InsertNextCell(2)
            self.lines.InsertCellPoint(idx - 1)
            self.lines.InsertCellPoint(idx)
            self.lines.ReplaceCellPointAtId(0, 1, idx)
            self.actor.SetVisibility(1)

    def update_last_point(self, position):
        last_pt_idx = self.points.GetNumberOfPoints() - 1
        self.points.SetPoint(last_pt_idx, position)
        self.points.Modified()

    def remove_last_point(self):
        new_size = self.points.GetNumberOfPoints() - 1
        if new_size > -1:
            self.points.SetNumberOfPoints(new_size)
            self.lines.Reset()
            for i in range(new_size):
                if i == 0:
                    self.lines.InsertNextCell(2)
                    self.lines.InsertCellPoint(0)
                    self.lines.InsertCellPoint(new_size - 1)
                else:
                    self.lines.InsertNextCell(2)
                    self.lines.InsertCellPoint(i - 1)
                    self.lines.InsertCellPoint(i)

    def get_last_point_dist2(self, position):
        last_pt_idx = self.points.GetNumberOfPoints() - 1
        last_point = self.points.GetPoint(last_pt_idx)
        dx = position[0] - last_point[0]
        dy = position[1] - last_point[1]
        dz = position[2] - last_point[2]
        return dx * dx + dy * dy + dz * dz


class PolygonInterationState:
    def __init__(self, style, renderer):
        # config
        self.z_world = 1
        self.draw_dist2 = 2 * 2

        # internals
        self.style: vtkInteractorStyleUser = style
        self.renderer = renderer

        self.position_press = Position()
        self.position_release = Position()
        self.position_move = Position()
        self.active = False
        self.enabled = True

        # Polygon
        self.polygon = Polygon()

    def update_position(self, pos):
        display = self.style.GetLastPos()
        pos.display[0] = display[0]
        pos.display[1] = display[1]
        world = self.renderer.DisplayToWorld(pos.display)
        pos.world[0] = world[0]
        pos.world[1] = world[1]
        pos.world[2] = self.z_world

    def press(self):
        if not self.enabled:
            return

        self.active = True
        self.update_position(self.position_press)
        self.polygon.insert_point(self.position_press.world)

    def move(self):
        if not self.enabled:
            return

        self.update_position(self.position_move)

        if not self.active or self.polygon.points.GetNumberOfPoints() < 1:
            return False

        if self.style.GetShiftKey():
            if self.draw_dist2 < self.polygon.get_last_point_dist2(
                self.position_move.world
            ):
                self.polygon.insert_point(self.position_move.world)
        else:
            self.polygon.update_last_point(self.position_move.world)
            return True

        return self.active

    def release(self):
        if not self.enabled:
            return

        self.update_position(self.position_release)
        self.active = False


class PolygonsManager:
    def __init__(self, renderer, poly_editor):
        self.renderer = renderer
        self.poly_editor = poly_editor
        self._next_id = 1
        self.polys = {}

    def add(self, name, category_id):
        poly_id = self._next_id
        self._next_id += 1
        poly = Polygon(name, category_id)
        self.polys[poly_id] = poly
        self.renderer.AddActor(poly.actor)
        return poly_id

    def remove(self, poly_id):
        if poly_id in self.polys:
            poly = self.polys.pop(poly_id)
            self.renderer.RemoveActor(poly.actor)

    def get(self, poly_id):
        return self.polys.get(poly_id)

    def activate(self, poly_id):
        other_visibility = True  # poly_id is None
        self.poly_editor.enabled = poly_id is not None

        for k, p in self.polys.items():
            if k == poly_id:
                self.poly_editor.polygon = p
                p.set_line_width(5)
                p.show(True)
            else:
                p.set_line_width(2)
                p.show(other_visibility)

    def to_list(self):
        polys = []
        for k, p in self.polys.items():
            polys.append(
                dict(
                    id=k,
                    name=p.name,
                    color=p.color,
                )
            )
        return polys


@TrameApp()
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
        self.interactor_style_polygon = vtkInteractorStyleUser()
        self.interactor.SetInteractorStyle(self.interactor_style_image)

        # paint interactor setup
        self.interactor_style_paint.AddObserver(
            vtkCommand.MouseMoveEvent, self.on_paint
        )

        # polygon interator setup
        self.polygon_state = PolygonInterationState(
            self.interactor_style_polygon, self.renderer
        )
        self.polygons_manager = PolygonsManager(self.renderer, self.polygon_state)
        self.interactor_style_polygon.AddObserver(
            vtkCommand.LeftButtonPressEvent, self.on_polygon_press
        )
        self.interactor_style_polygon.AddObserver(
            vtkCommand.LeftButtonReleaseEvent, self.on_polygon_release
        )
        self.interactor_style_polygon.AddObserver(
            vtkCommand.MouseMoveEvent, self.on_polygon_move
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

        # Polygon data structures

        # Fill renderer
        self.renderer.AddViewProp(self.painting_actor)
        self.renderer.AddViewProp(self.image_actor)

    def update(self):
        self.server.controller.view_update()

    @property
    def state(self):
        return self.server.state

    @property
    def brush_size(self):
        return self.server.state.brush_size

    def set_active_color(self, color_rgba):
        self.active_color = color_rgba
        self.painting_canvas.SetDrawColor(*self.active_color)
        self.polygon_state.polygon.color = self.active_color
        self.update()

    def select_interactor(self, mode):
        if mode == "navigation":
            self.interactor.SetInteractorStyle(self.interactor_style_image)
        elif mode in ["brush", "eraser"]:
            self.painting_canvas.SetDrawColor(*self.active_color)
            self.interactor.SetInteractorStyle(self.interactor_style_paint)
        elif mode == "polygon":
            self.interactor.SetInteractorStyle(self.interactor_style_polygon)
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
            self.painting_canvas.FillTube(i_0, j_0, i_1, j_1, self.brush_size)
            for r in range(2, 2 * self.brush_size):
                self.painting_canvas.DrawCircle(i_0, j_0, r * 0.5)
                self.painting_canvas.DrawCircle(i_1, j_1, r * 0.5)
            self.update()

    def on_polygon_press(self, style: vtkInteractorStyleUser, event):
        self.polygon_state.press()

    def on_polygon_release(self, style: vtkInteractorStyleUser, event):
        self.polygon_state.release()
        self.update()

    def on_polygon_move(self, style: vtkInteractorStyleUser, event):
        if self.polygon_state.move():
            self.update()

    def update_brush_scale(self):
        vec3 = [0, 0, 0]
        self.current_image.TransformContinuousIndexToPhysicalPoint(0, 0, 0, vec3)
        self.renderer.SetWorldPoint([*vec3, 0])
        self.renderer.WorldToDisplay()
        xd0 = self.renderer.GetDisplayPoint()[0]
        self.current_image.TransformContinuousIndexToPhysicalPoint(1, 1, 1, vec3)
        self.renderer.SetWorldPoint([*vec3, 0])
        self.renderer.WorldToDisplay()
        xd1 = self.renderer.GetDisplayPoint()[0]
        self.server.state.brush_scale = xd1 - xd0

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

        self.reset_color()
        self.reset_camera()
        self.update_brush_scale()

    @controller.set("polygon_delete_last_point")
    def polygon_delete_last_point(self):
        self.polygon_state.polygon.remove_last_point()
        self.update()

    @controller.set("polygon_create")
    def polygon_add(self, name):
        cat_id = self.state.seg_class_active[0]
        new_poly_id = self.polygons_manager.add(name, cat_id)
        self.polygons_manager.get(new_poly_id).color = self.active_color
        self.state.polygons = self.polygons_manager.to_list()
        return new_poly_id

    @controller.set("polygon_remove")
    def polygon_remove(self, poly_id):
        self.polygons_manager.remove(poly_id)
        self.state.polygons = self.polygons_manager.to_list()

    @controller.set("polygon_edit")
    def polygon_edit(self, poly_id=None):
        self.polygons_manager.activate(poly_id)
        self.update()

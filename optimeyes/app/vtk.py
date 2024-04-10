import vtk

vtk.vtkRenderWindowInteractor
vtk.vtkJPEGReader


class AnnotationEngine:
    def __init__(self, server):
        self.server = server
        self.image_reader = vtk.vtkJPEGReader()
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.viewer = vtk.vtkImageViewer2()
        self.viewer.SetupInteractor(self.interactor)
        self.viewer.GetRenderer().SetBackground(0.5, 0.5, 0.5)

        self.render_window.OffScreenRenderingOn()

    def update(self):
        self.server.controller.view_update()

    def reset_camera(self):
        self.render_window.Render()
        self.renderer.ResetCamera()
        self.update()

    @property
    def render_window(self):
        return self.viewer.GetRenderWindow()

    @property
    def renderer(self):
        return self.viewer.GetRenderer()

    def load_image(self, image_path):
        self.image_reader.SetFileName(image_path)
        self.viewer.SetInputConnection(self.image_reader.GetOutputPort())
        self.reset_camera()

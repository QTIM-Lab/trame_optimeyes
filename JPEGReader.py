import os, vtk
# Attempt with https://kitware.github.io/vtk-examples/site/Java/IO/JPEGReader/
# vtk.vtkNativeLibrary # Didn't work, but maybe we don't need
vtk.vtkRenderWindowInteractor
# vtk.vtkImageReader2 # Need but we have already from vtk.vtkImageReader2 via inheritance
vtk.vtkJPEGReader # inherits from vtk.vtkImageReader2
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
imageViewer2.Render()
renderWindowInteractor.Start()
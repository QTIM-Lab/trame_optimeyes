import os, vtk

images_path = "images"
os.listdir(images_path)
image = os.path.join(images_path, "MRN 803567 2_aff_registered.jpg")

# Attempt with https://kitware.github.io/vtk-examples/site/Java/IO/JPEGReader/


# vtk.vtkNativeLibrary # Didn't work
vtk.vtkRenderWindowInteractor
vtk.vtkJPEGReader
vtk.vtkImageViewer2
vtk.vtkImageReader2

from vtkmodules import vtkIOImage
vtkIOImage.vtkImageReader2

jpgReader = vtk.vtkJPEGReader
jpgReader.SetFileName(image)
jpgReader.SetFileName(vtkIOImage.vtkImageReader2, image)
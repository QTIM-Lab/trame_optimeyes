# Kitware Tutorials

## Tutorial_Step1.py
This one is self explainatory and is step one for anyone.

## Select_Examples.py
This one is awesome. It let's you specify a vtk class and language and github examples are printed to the screen for you to use as examples.

Ex:
```python
$ ./Select_Examples.py vtkActor python
VTK Class: vtkActor, language: Python
Number of example(s): 5.
https://kitware.github.io/vtk-examples/site/Python/Interaction/InteractorStyleTrackballCamera
https://kitware.github.io/vtk-examples/site/Python/VisualizationAlgorithms/CreateBFont
https://kitware.github.io/vtk-examples/site/Python/VisualizationAlgorithms/CutWithCutFunction
https://kitware.github.io/vtk-examples/site/Python/VisualizationAlgorithms/LOxGrid
https://kitware.github.io/vtk-examples/site/Python/VisualizationAlgorithms/OfficeTube

$ ./Select_Examples.py -n 10 vtkActor python
VTK Class: vtkActor, language: Python
Number of example(s): 10.
https://kitware.github.io/vtk-examples/site/Python/ExplicitStructuredGrid/LoadESGrid
https://kitware.github.io/vtk-examples/site/Python/Filtering/ConstrainedDelaunay2D
https://kitware.github.io/vtk-examples/site/Python/GeometricObjects/Arrow
https://kitware.github.io/vtk-examples/site/Python/GeometricObjects/RegularPolygonSource
https://kitware.github.io/vtk-examples/site/Python/IO/ReadExodusData
https://kitware.github.io/vtk-examples/site/Python/Rendering/FlatVersusGouraud
https://kitware.github.io/vtk-examples/site/Python/Rendering/Rotations
https://kitware.github.io/vtk-examples/site/Python/StructuredGrid/SGrid
https://kitware.github.io/vtk-examples/site/Python/VisualizationAlgorithms/Motor
https://kitware.github.io/vtk-examples/site/Python/VisualizationAlgorithms/SplatFace
```

Current stats on examples they have: https://kitware.github.io/vtk-examples/site/Python/Coverage/PythonVTKClassesUsed/

As of writing this 442/2977 available examples exist for python.
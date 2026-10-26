# FreeCADCmd scripts/3d/step_to_mesh.py: tessellates the STEP and FCStd sources
# into meshes Blender can import, and prints each part's bounding box in mm.
import os, sys
import FreeCAD, Import, Mesh, MeshPart, Part

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "3d-models")
OUT = os.path.join(ROOT, "meshes")

def export(shape, name, deflection):
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=deflection,
                                  AngularDeflection=0.5, Relative=False)
    mesh.write(os.path.join(OUT, name + ".stl"))
    bb = shape.BoundBox
    print(f"{name}: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm, "
          f"{mesh.CountFacets} facets")

def step(path, name, deflection):
    doc = FreeCAD.newDocument(name)
    Import.insert(path, doc.Name)
    shapes = [o.Shape for o in doc.Objects if hasattr(o, "Shape") and not o.Shape.isNull()
              and o.Shape.Solids]
    export(Part.makeCompound([s for sh in shapes for s in sh.Solids]), name, deflection)

def fcstd(path, name):
    doc = FreeCAD.openDocument(path)
    bodies = [o for o in doc.Objects if o.TypeId == "PartDesign::Body"]
    for b in bodies:
        print(f"  {name} body {b.Label}")
    export(bodies[-1].Shape, name, 0.05)

step(os.path.join(ROOT, "elements/lilygo-t-sim7000g-1/TTGO_SIM7000GV1.STEP"), "lilygo", 0.1)
step(os.path.join(ROOT, "elements/aht20-bmp280-2/AHT20+BMP280.step"), "sensor", 0.05)
fcstd(os.path.join(ROOT, "casing/Base.FCStd"), "case-base")
fcstd(os.path.join(ROOT, "casing/Top.FCStd"), "case-top")

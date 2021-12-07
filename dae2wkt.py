import collada
import os

mesh = collada.Collada("input.dae")

grid = mesh.geometries[0]

grid = grid.primitives[0]

vertices = grid.vertex[:, 0:2]
vertices *= 100
triangles = grid.indices[:, :, 0]

file_str = ""
for t in triangles:
    p1 = vertices[t[0]]
    p1_str = str(p1[0]) + " " + str(p1[1])
    p2 = vertices[t[1]]
    p2_str = str(p2[0]) + " " + str(p2[1])
    p3 = vertices[t[2]]
    p3_str = str(p3[0]) + " " + str(p3[1])

    line_str = "LINESTRING ({})\n".format(
            p1_str + ", " + p2_str + ", " + p3_str + ", " + p1_str
            )

    file_str += line_str

with open("dae2wkt_output.wkt", "w") as f:
    f.write(file_str)

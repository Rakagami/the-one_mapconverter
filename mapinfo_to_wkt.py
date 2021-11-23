#/usr/bin/python
from bs4 import BeautifulSoup
from svg.path import parser
from svg.path import Move, Line, Close
import numpy as np
import sys
import tqdm

transform = {
        "scale": np.array([1.0, 1.0]),
        "translate": np.array([0.0, 0.0]),
        }

# Point is a numpy vector
def coords_normalize(cs, point, thr=1.0):
    for c in cs:
        d = np.linalg.norm(c - point)
        if(np.abs(d) < thr):
            return c
    cs.append(point)
    return point


def main(svg_filename, wkt_filename):
    with open(svg_filename, "r") as f:
        xml = f.read()
    
    main = BeautifulSoup(xml, "lxml")
    main = main.find_all("g")
    main = [g for g in main if g["inkscape:label"] == "Path"]

    if(len(main) < 1):
        raise Exception("svg path format not correct. No 'Path' layer")
    else:
        main = main[0]

    cs = [] #coords set

    lines = []
    for p in tqdm.tqdm(main.find_all("path")):
        svg_path = p["d"]
        #coords = coords[1:-1].strip().split(" ")
        #coords = [c.split(",")[0] + " " + c.split(",")[1] for c in coords]
        #print(svg_path)
        path = parser.parse_path(svg_path)
        coords = []
        for point in path:
            if(type(point) == Move):
                np_p = np.array([point.start.real, point.start.imag])
                coords.append(coords_normalize(cs, np_p))
            elif(type(point) == Line):
                np_p = np.array([point.end.real, point.end.imag])
                coords.append(coords_normalize(cs, np_p))
            elif(type(point) == Close):
                #np_p = np.array([point.end.real, point.end.imag])
                coords.append(coords[0].copy())
            else:
                raise Exception("svg path format not correct. There is an unsupported svg construct: "  + str(point))
        coords = np.array(coords)
        coords = np.round(coords, decimals=2)
        coords += transform["translate"]
        coords *= transform["scale"]
        #print("Path", path)
        #print("Coords", coords)
        str_coords = [str(c[0]) + " " + str(c[1]) for c in coords]
        lines.append(str_coords)
    
    file_str = ""
    for l in lines:
        file_str += "LINESTRING ({})\n".format(
                ", ".join(l)
                )

    origin_file_str = "LINESTRING (0 0, {})\n".format(lines[0][0])

    #print(file_str)
    
    output_file = wkt_filename
    with open(output_file, "w") as f:
        f.write(file_str)

    if len(output_file) > 4 and output_file[-4:] == ".wkt":
        origin_file = output_file[:-4] + "_origin.wkt"
    else:
        origin_file = output_file + "_origin.wkt"
    with open(origin_file, "w") as f:
        f.write(origin_file_str)

    print("Generated output file in", output_file)

### Script ###
usage = """
Usage:
 python3 mapinfo_to_wkt.py <mapname>                    converts file <mapname>.svg to <mapname>.wkt
 python3 mapinfo_to_wkt.py <mapname> -o <output_file>   displays oracle answer

Utility tool to create custom maps for The ONE simulator. It converts a svg into a wkt
 """

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if len(sys.argv[1]) > 4 and sys.argv[1][-4:] == ".svg":
            main(sys.argv[1], sys.argv[1][:-4] + ".wkt")
        else:
            main(sys.argv[1] + ".svg", sys.argv[1] + ".wkt")
    elif len(sys.argv) == 4 and sys.argv[2] == "-o":
        if len(sys.argv[1]) > 4 and sys.argv[1][-4:] == ".svg":
            main(sys.argv[1], sys.argv[3])
        else:
            main(sys.argv[1] + ".svg", sys.argv[3])
    else:
        print(usage)

#/usr/bin/python
from bs4 import BeautifulSoup
from svg.path import parser
from svg.path import Move, Line
import sys

def main(svg_filename, wkt_filename):
    with open(svg_filename, "r") as f:
        xml = f.read()
    
    main = BeautifulSoup(xml, "lxml")

    lines = []
    for p in main.find_all("path"):
        svg_path = p["d"]
        #coords = coords[1:-1].strip().split(" ")
        #coords = [c.split(",")[0] + " " + c.split(",")[1] for c in coords]
        #print(svg_path)
        path = parser.parse_path(svg_path)
        coords = []
        for point in path:
            if(type(point) == Move):
                coords.append([point.start.real, point.start.imag])
            elif(type(point) == Line):
                coords.append([point.end.real, point.end.imag])
            else:
                raise Exception("svg path format not correct")
        #print("Path", path)
        #print("Coords", coords)
        str_coords = [str(c[0]) + " " + str(c[1]) for c in coords]
        lines.append(str_coords)
    
    file_str = ""
    for l in lines:
        file_str += "LINESTRING ({})\n".format(
                ", ".join(l)
                )

    print(file_str)
    
    output_file = wkt_filename
    with open(output_file, "w") as f:
        f.write(file_str)

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

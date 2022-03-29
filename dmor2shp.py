from glob import glob
import os. path
import numpy as np
import json

from shapely.geometry import Polygon, mapping

def poly2shp(poly, prop={}):
    return { "type": "Feature",
             "properties": prop,
             "geometry": mapping(poly)
             }

def geojson_dump(fn, objs):
    with open(fn, 'w') as geojson:
        json.dump(
            { "type": "FeatureCollection",
              "features": objs
            },
            geojson,
            indent=2)
            
if '__main__' == __name__:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('dmor', nargs='?', default='jsonDMQR.json')
    p.add_argument('dir', nargs='?', default='labels')
    args = p.parse_args()

    yoloqr = json.load(open(args.dmor))

    for y in yoloqr:
        im = y.pop('filename')
        im_base, _ = os.path.splitext(im)
        corners = y.pop('corners')
        x0 = corners['x0']
        x1 = corners['x1']
        x2 = corners['x2']
        x3 = corners['x3']
        y0 = corners['y0']
        y1 = corners['y1']
        y2 = corners['y2']
        y3 = corners['y3']
        poly = Polygon([(x0,-y0),(x1,-y1),(x2,-y2),(x3,-y3)]) # auto close

        geojson_dump('%s/%s-dmor.json'%(args.dir, im_base),
                     [poly2shp(poly, y)])

        rpoly = poly.minimum_rotated_rectangle

        rcorners = rpoly.exterior.coords
        p0 = rcorners[0]
        p1 = rcorners[1]
        p2 = rcorners[2]

        y['x'] = (p0[0]+p2[0])/2
        y['y'] = (p0[1]+p2[1])/2

        y['w'] = np.sqrt((p1[0]-p0[0])*(p1[0]-p0[0])+(p1[1]-p0[1])*(p1[1]-p0[1]))
        y['h'] = np.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

        y['theta'] = np.arctan2(p1[1]-p0[1], p1[0]-p0[0])

        geojson_dump('%s/%s-rbox.json'%(args.dir, im_base),
                     [poly2shp(poly.minimum_rotated_rectangle, y)])

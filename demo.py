import os
import pyorient
import json



client = pyorient.OrientDB("localhost", 2424)

client.connect("root", "12Krokodil")

client.db_open("roads", "root", "12Krokodil")

# qu = "select expand(bothE(E)) from (select * from V where  ST_WITHIN(geometry,'POLYGON ((-0.114241 51.379962, -0.097418 51.380123, -0.097504 51.372837, -0.112267 51.372033, -0.114241 51.379962))') = true limit 30000)"

# result = client.query(qu)




from flask import Flask, make_response
app = Flask(__name__)

@app.route('/roads/<qu>', methods=["GET"])
def geometries(qu):

    result= client.query(qu)
    coords = []
    geom = []

    for j in result:

        d = [i.split(',') for i in j.oRecordData['geometry']['coordinates'].replace("[", "").replace("]]", "").replace("d", "").replace(")", "").split('],')]

        coords.append(d)

    for s in coords:

        poly = []

        for d in s:

            point = [float(d[0]), float(d[1])]

            poly.append(point)


        gj = { "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": poly

          },
        "properties": {
          "prop0": "value0",
          "prop1": 0.0
          }
        }

        geom.append(gj)


    geojson = {"type": "FeatureCollection",
               "features": geom}
    return make_response(json.dumps(geojson))


if __name__ == '__main__':
   app.run(debug = True)





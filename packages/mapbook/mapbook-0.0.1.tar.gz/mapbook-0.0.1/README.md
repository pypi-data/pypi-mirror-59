## How to install

```
conda install jupyter_contrib_nbextensions
jupyter contrib nbextension install --sys-prefix

pip install mapbook-0.0.1-py3-none-any.whl
jupyter serverextension enable --py mapbook --sys-prefix
jupyter nbextension install --py mapbook --sys-prefix
jupyter nbextension enable mapbook --py --sys-prefix
```

## How to uninstall

```
jupyter nbextension disable --py mapbook --sys-prefix
jupyter nbextension uninstall --py mapbook --sys-prefix
jupyter serverextension disable --py mapbook --sys-prefix
pip uninstall mapbook
```

Remove `--sys-prefix` for Windows system

## Notes

All the key and value pairs of javascript object written in python dict format should be quoted with double quote `"`, `"""` or `'''`. Javascript string must quoted by double quote `"`.

## Simple example

```
import mapbook as mb

# Create map container
div_opts = {
    "title": "div01 for map01",
    "div_class": "map",
    "css": {
        "width": "100%",
        "height": "100%",
        "cursor": "crosshair",
    }
}
divWin01 = mb.DivWindow(**div_opts)

# Create map
map_opts = {
    # "crs": "L.CRS.Simple",
    "center": [55.38, -3.43],
    "zoom": 6,
}
map1 = mb.Map(divWin01, **map_opts)

# Add base layer to map
lay01 = mb.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', **map_opts)
lay01.addTo(map1)

# Add geojson layer to map
data = """
{ "type": "FeatureCollection",
  "features": [
    { "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [17.9296875, 35.746512259918504]},
      "properties": {"prop0": "value0"}
      },
    { "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [-1.7578125,43.068887774169625],
          [12.3046875,52.26815737376817],
          [26.015625,40.44694705960048],
          [48.1640625,49.61070993807422]
        ]
        },
      "properties": {
        "prop0": "value0",
        "prop1": 0.0
        }
      },
    { "type": "Feature",
       "geometry": {
         "type": "Polygon",
         "coordinates": [
          [[-8.0859375, 25.16517336866393],
           [-12.3046875, 5.61598581915534],
           [0.3515625, -2.460181181020993],
           [22.8515625, 2.4601811810210052],
           [18.984375, 24.206889622398023],
           [2.109375, 32.54681317351514],
           [-8.0859375, 25.16517336866393]
          ]]
       },
       "properties": {
         "prop0": "value0",
         "prop1": {"this": "that"}
         }
       }
    ]
  }
"""
geom = mb.GeoJSON(data)
geom.addTo(map1)
```

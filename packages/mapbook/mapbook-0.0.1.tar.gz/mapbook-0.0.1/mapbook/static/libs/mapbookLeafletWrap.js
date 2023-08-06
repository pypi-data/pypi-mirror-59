/***************************************
 Modulo mapbookDiv
***************************************/
define('mapbookDiv', ['singleton', 'jquery', 'leaflet', 'goldenlayout'], 
function (singleton, $, L, GoldenLayout) {
  function mapbookDiv(divOptions){
    var mblut = singleton().lut;
    var newItemConfig = {
        type: 'component',
        componentName: 'mbDiv',
        componentState: divOptions,
        id: divOptions.id,
    };
    mblut['mbGoldenLayout'].root.contentItems[0].addChild(newItemConfig);
    mblut[divOptions.id] = "";
  }
  
  return mapbookDiv;
});

/***************************************
 Modulo mapbookMap
***************************************/
define('mapbookMap', ['singleton', 'jquery', 'leaflet', 'goldenlayout'], 
function (singleton, $, L, GoldenLayout) {
  function mapbookMap(divId, mapOptions){
    var mblut = singleton().lut;
    var map = L.map(divId, mapOptions);
    mblut[mapOptions.id] = map;
    mblut[divId] = mapOptions.id;
    // cursor for sync
    var svgrect = "<svg width='100' height='100' xmlns='http://www.w3.org/2000/svg'><path d='M50,100 L100,0 L50,25 L0,0 Z' style='stroke:black;stroke-width:5;stroke-linecap:round;fill:none;'></path></svg>";
    var svg_url = encodeURI("data:image/svg+xml," + svgrect).replace('#','%23');
    var  myIcon = L.icon({
        iconUrl: svg_url,
        iconSize: [40, 40],
        iconAnchor: [20, 42],
        /* className:'icon4sync', */
    });
    var marker_option = {
        icon: myIcon,
        clickable:false,
        opacity:0,
    };
    var marker = new L.marker([0,0], marker_option);
    map.addLayer(marker);
    map["icon4sync"] = marker;
    // TODO: use control class instead
    var contrl = L.control.layers(null, {}).addTo(map);
    mblut[mapOptions.id+"_control"] = contrl;
  }

  return mapbookMap;
});

/***************************************
  mapbook layer addTo
***************************************/
define('mapbookAddTo', ['singleton', 'jquery', 'leaflet', 'goldenlayout'], 
function (singleton, $, L, GoldenLayout) {
  function mapbookAddTo(lay_id, map_id){
    var mblut = singleton().lut;
    mblut[lay_id].addTo(mblut[map_id]);
  }

  return mapbookAddTo;
});

/***************************************
  mapbook layer removeFrom
***************************************/
define('mapbookRemoveFrom', ['singleton', 'jquery', 'leaflet', 'goldenlayout'], 
function (singleton, $, L, GoldenLayout) {
  function mapbookRemoveFrom(lay_id, map_id){
    var mblut = singleton().lut;
    mblut[map_id].removeLayer(mblut[lay_id]);
  }

  return mapbookRemoveFrom;
});

/***************************************
  mapbook tileLayer
***************************************/
define('mapbookTileLayer', ['singleton', 'jquery', 'leaflet', 'goldenlayout'], 
function (singleton, $, L, GoldenLayout) {
  function mapbookTileLayer(urlTemplate, layOptions){
    var mblut = singleton().lut;
    var lay = L.tileLayer(urlTemplate, layOptions);
    mblut[layOptions.id] = lay;
    // lay.addTo(mblut['map01']);
  }

  return mapbookTileLayer;
});

/***************************************
  mapbook imageOverlay
***************************************/
define('mapbookImageOverlay', ['singleton', 'jquery', 'leaflet', 'goldenlayout'], 
function (singleton, $, L, GoldenLayout) {
  function mapbookImageOverlay(imageUrl, bounds, layOptions){
    var mblut = singleton().lut;
    var lay = L.imageOverlay(imageUrl, bounds, layOptions);
    mblut[layOptions.id] = lay;
  }

  return mapbookImageOverlay;
});

/***************************************
  mapbook GeoJSON
***************************************/
define('mapbookGeoJSON', ['singleton', 'jquery', 'leaflet', 'goldenlayout'], 
function (singleton, $, L, GoldenLayout) {
  function mapbookGeoJSON(data, layOptions){
    var mblut = singleton().lut;
    var lay = L.geoJSON(data, layOptions);
    mblut[layOptions.id] = lay;
  }

  return mapbookGeoJSON;
});

/***************************************
  mapbook vectorGrid
***************************************/
define('mapbookVectorGrid', [
  'singleton', 
  'jquery', 
  'leaflet', 
  'goldenlayout', 
  'require', 
  'leaflet_vectorGrid'], 
function (singleton, $, L, GoldenLayout, require) {
  function mapbookVectorGrid(data, layOptions){
    var mblut = singleton().lut;
    var vectorGrid = require("leaflet_vectorGrid");
    var lay = L.vectorGrid.slicer( data, layOptions);
    mblut[layOptions.id] = lay;
  }

  return mapbookVectorGrid;
});

/***************************************
  mapbook mapsync
***************************************/
define('mapSync', 
function() {
  function mapSync() {
    var maps = new Set();
    var NO_ANIMATION = {
        pan: { animate: false, },
        zoom: { animate: true, },
        /* reset: true */
    };
    syncMaps = function(evt){
        /* setView, setZoom, panTo, getCenter()*/
        var type = evt.type;
        var zoom = evt.target.getZoom();
        var center = evt.target.getCenter();
        maps.forEach(function(map){
        if (map !== evt.target){
            map.setView(center, zoom, NO_ANIMATION);
        }
        });
    };
	  addCursor = function(evt){
	    maps.forEach(function(map){
	      map["icon4sync"].setOpacity(1);
	    });
	  };
	  removeCursor = function(evt){
	    maps.forEach(function(map){
	      map["icon4sync"].setOpacity(0);
	    });
	  };
	  fakeCursor = function(evt){
	    latlon = evt.latlng;
	    maps.forEach(function(map){
	      map["icon4sync"].setLatLng(latlon);
	    });
	  };

  
    return {
      sync: function (map_list) {
          map_list.forEach(function(map){
            maps.add(map);
            map.on('resize', syncMaps);
            map.on('move', syncMaps);
            //cursors
            map.on('mouseover', addCursor);
            map.on('mousemove', fakeCursor);
            map.on('mouseout',  removeCursor);
          });
          // console.log(maps);
      },
      unsync: function(map_list) {
          map_list.forEach(function(map){
            map["icon4sync"].setOpacity(0);
            maps.delete(map);
            map.off('resize');
            map.off('move');
            //cursors
            map.off('mouseover');
            map.off('mousemove');
            map.off('mouseout');
          });
          // console.log(maps);
      },
    };
  }
  
  return mapSync;
});

/***************************************
  mapbook CoordCtrl
***************************************/
define('mapbookCoordCtrl', ['singleton', 'jquery', 'leaflet', 'goldenlayout', 'leaflet.Coordinates'], 
function (singleton, $, L, GoldenLayout) {
  function mapbookCoordCtrl(layOptions){
    var mblut = singleton().lut;
    var lay = L.control.coordinates(layOptions);
    mblut[layOptions.id] = lay;
  }

  return mapbookCoordCtrl;
});


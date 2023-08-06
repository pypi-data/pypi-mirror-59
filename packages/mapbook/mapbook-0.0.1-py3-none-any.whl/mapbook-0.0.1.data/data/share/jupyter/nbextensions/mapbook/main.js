define([
    'base/js/namespace',
    'jquery',
    'require',
    'notebook/js/cell',
    'base/js/security',
    'components/marked/lib/marked',
    'base/js/events',
    'notebook/js/textcell'
], function(IPython, $, requirejs, cell, security, marked, events, textcell) {
    "use strict";
// start

   /**
     * Add CSS file
     *
     * @param name filename
     */
    var load_css = function (name) {
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = requirejs.toUrl(name);
        document.getElementsByTagName("head")[0].appendChild(link);
    };
    
    var load_ipython_extension = function() {
        const sleep = (milliseconds) => {
          return new Promise(resolve => setTimeout(resolve, milliseconds))
        };
        console.log('[mapbook]: loading ...');
        load_css('./libs/Leaflet/leaflet.css');
        load_css('./libs/GoldenLayout/goldenlayout-base.css');
        load_css('./libs/GoldenLayout/goldenlayout-light-theme.css');
        load_css('./libs/Leaflet.draw/leaflet.draw.css');
        load_css('./libs/Leaflet.Coordinates/Leaflet.Coordinates-0.1.5.css');
        load_css('./libs/handsontable/handsontable.full.min.css');
        load_css('./mapbook.css');
        var leafletUrl = requirejs.toUrl('./libs/Leaflet/leaflet.js');
        var goldenlayoutUrl = requirejs.toUrl('./libs/GoldenLayout/goldenlayout.min.js');
        var leaflet_vectorGridUrl = requirejs.toUrl('./libs/Leaflet.VectorGrid/Leaflet.VectorGrid.bundled.js');
        var leaflet_drawUrl = requirejs.toUrl('./libs/Leaflet.draw/Leaflet.draw_bundle.js');
        var leaflet_coordinatesUrl = requirejs.toUrl('./libs/Leaflet.Coordinates/Leaflet.Coordinates-0.1.5.min.js');
        var mapbookLeafletWrapUrl = requirejs.toUrl('./libs/mapbookLeafletWrap.js');
        var plotlyUrl = requirejs.toUrl('./libs/plotly/plotly-latest.min.js');
        var handsontableUrl = requirejs.toUrl('./libs/handsontable/handsontable.full.min.js');
        // console.log(leafletUrl);
        // console.log(goldenlayoutUrl);
        // console.log(leaflet_vectorGridUrl);
        console.log(handsontableUrl);
        require.config({
          paths: {
            'leaflet': leafletUrl, //'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet',
            'goldenlayout': goldenlayoutUrl, //'https://golden-layout.com/files/latest/js/goldenlayout.min',
            'leaflet_vectorGrid': leaflet_vectorGridUrl, // https://unpkg.com/leaflet.vectorgrid@1.3.0/dist/Leaflet.VectorGrid.bundled.js,
            'leaflet.draw': leaflet_drawUrl,
            'leaflet.Coordinates' : leaflet_coordinatesUrl,
            'mapbookLeafletWrap' : mapbookLeafletWrapUrl,
            'plotly' : plotlyUrl,
            'handsontable': handsontableUrl,
          },
          bundles: {
            'mapbookLeafletWrap': ['mapbookDiv', 
                                   'mapbookMap', 
                                   'mapbookAddTo',
                                   'mapbookRemoveFrom',
                                   'mapbookTileLayer',
                                   'mapbookImageOverlay',
                                   'mapbookGeoJSON',
                                   'mapbookVectorGrid',
                                   'mapbookCoordCtrl',
                                   'mapSync'],
          },
          shim: {
            'leaflet': {
                exports : 'L'
            },
            'leaflet_vectorGrid': {
                deps: ['leaflet']
            },
            'leaflet.draw': {
                deps: ['leaflet']
            },
            'leaflet.Coordinates': {
                deps: ['leaflet']
            },
            'plotly': {
                exports : 'Plotly'
            },
          },
        });
        requirejs(['leaflet', 
                   'goldenlayout', 
                   'plotly',
                   'handsontable',
                   'singleton', 
                   'init',
                   'mapbookComm',
                   'leaflet_vectorGrid', 
                   'leaflet.draw',
                   'leaflet.Coordinates',
                   'mapbookDiv', 
                   'mapbookMap', 
                   'mapbookAddTo',
                   'mapbookRemoveFrom',
                   'mapbookTileLayer',
                   'mapbookImageOverlay',
                   'mapbookGeoJSON',
                   'mapbookVectorGrid',
                   'mapbookCoordCtrl',
                   'mapSync'], 
        function(L, GoldenLayout, Plotly, Handsontable, singleton, init, mapbookComm) {
          sleep(50).then(() => {
              var mblut = singleton().lut;
              mblut['jquery version'] = $.fn.jquery;
              mblut['leaflet version'] = L.version;
              mblut['goldenlayout version'] = GoldenLayout.version;
              mblut['leaflet_vectorGrid'] = L.vectorGrid.name;
              mblut['leaflet.draw version'] = L.drawVersion;
              mblut['plotly version'] = Plotly.version;
              //mblut['handsontable']	= Handsontable.version;
              //mblut['leaflet.Coordinates version'] = L.control.coordinates().version;
              init();
              mapbookComm();
              console.log(mblut);
              console.log('[mapbook]: loaded.');
          })
        });
    };

    return {
        load_ipython_extension : load_ipython_extension
    };

// end 
});

/***************************************
  Global vars for python id -> js obj
***************************************/
define('lookUpTable', [], function () {
  return {};
});

/***************************************
  Singleton
***************************************/
define('singleton', ['lookUpTable'], function (lut) {
  'use strict';
  var instance = null;
  function Singleton() {
    this.lut = lut;
  }

  return function getInstance() {
    instance = instance || new Singleton();
    return instance;
  };
});

/***************************************
 Modulo mapbookComm
***************************************/
define('mapbookComm', ['singleton'],
function(singleton){
  function mapbookComm(){
    'use strict';  
    var mblut = singleton().lut;  
    var comm_manager=Jupyter.notebook.kernel.comm_manager
    var handle_msg=function(msg){
        console.log('got msg: ' + msg['content']['data']); 
    }
    comm_manager.register_target('mapbookComm', function(comm,msg){
        console.log('opened comm');
        // comm.send('from js 4');
        // register callback
        comm.on_msg(handle_msg)
        mblut['mapbookComm'] = comm;
    }); 
  }
  // end
  return mapbookComm;
});

/***************************************
 Modulo init
***************************************/
define('init', ['singleton', 'jquery', 'leaflet', 'goldenlayout', 'plotly'], 
function (singleton, $, L, GoldenLayout, Plotly) {
  'use strict';
  function init() {
    // Singleton
    var mblut = singleton().lut;
    //setup golden-layout windows manager
    var config = {
          content: [{
            type: 'row',
            content: [{
                type: 'component',
                id: 'jupyter-notebook',
                title: 'Jupyter Notebook',
                isClosable: false,
                componentName: 'JupyterNotebook',
                componentState: { id: 'jupyter-notebook' }
            }]
          }]
        };

    if (!('mbGoldenLayout' in mblut)) {
      var mbDivComponent = function(container, componentState) {
          let thisDiv = $("<div>", {
            id: componentState.id,
            class: componentState.class,
            css: componentState.css,
          });
          container.getElement().append(thisDiv);
          container.setTitle(componentState.title);
      };
      mbDivComponent.prototype._bindContainerEvents = function() {
        this._container.on( 'resize', this._resize.bind( this ) );
        //this._container.on( 'destroy', this.mymap.destroy.bind( this.mymap ) );
      };
      mbDivComponent.prototype._resize = function() {
        this.mymap.invalidateSize();
      };
      var JupyterNotebookComponent = function (container, componentState) {
          container.getElement().append($('#notebook_panel'));
          // container.getElement().html( '<div style="overflow-y: scroll;height: 100%;"><div id="notebook"></div></div>' );
      };
      let myLayout = new GoldenLayout(config, $('#ipython-main-app') );
      myLayout.registerComponent( 'mbDiv', mbDivComponent);
      myLayout.registerComponent('JupyterNotebook', JupyterNotebookComponent);
      myLayout.init();
      mblut['mbGoldenLayout'] = myLayout;
      //myLayout.updateSize();
      $(window).resize(function() {
        myLayout.updateSize();
      });
      myLayout.on('componentCreated',function(component) {
          component.container.on('resize',function() {
              // console.log('component.resize',component.componentName);
              var div_id = component.config.componentState.id;
              var map_id = mblut[div_id];
              if (map_id && map_id.startsWith("Map_")){ mblut[map_id].invalidateSize(); }
              if (map_id && map_id.startsWith("handsontable_")){ mblut[map_id].refreshDimensions();}
              if (map_id && map_id.startsWith("plotly_")){ 
                  Plotly.relayout(div_id, { 
                      width:  document.getElementById(div_id).clientWidth,
                      height: document.getElementById(div_id).clientHeight
                  });
                  console.log(div_id + ' relayout');
              }
          });
      });
    } else { console.log('mapbook GoldenLayout already initialized.');}
  // end
}

  return init;
});


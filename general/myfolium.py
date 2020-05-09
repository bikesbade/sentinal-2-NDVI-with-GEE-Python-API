# import Google earth engine module
import ee
# Import libraries.
import folium
from folium import plugins



 # Define a method for displaying Earth Engine image tiles on a folium map.

def add_ee_layer(self, ee_object, vis_params, name):
        
    try:    
        # display ee.Image()
        if isinstance(ee_object, ee.image.Image):    
            map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)

        # display ee.ImageCollection()
        elif isinstance(ee_object, ee.imagecollection.ImageCollection):    
            ee_object_new = ee_object.mosaic()
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)

        # display ee.Geometry()
        elif isinstance(ee_object, ee.geometry.Geometry):    
            folium.GeoJson(
            data = ee_object.getInfo(),
            name = name,
            overlay = True,
            control = True
            ).add_to(self)

        # display ee.FeatureCollection()
        elif isinstance(ee_object, ee.featurecollection.FeatureCollection):  
            ee_object_new = ee.Image().paint(ee_object, 0, 2)
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)
        
    except:
        print("Could not display {}".format(name))

        
        
 

class foliumInitialize:
    # The init method or constructor  
    def __init__(self, location,zoom_start,height):  
            
        # Instance Variable  
        self.location = location
        self.zoom_start = zoom_start
        self.height = height
    
    def Initialize(self):
        folium.Map.add_ee_layer = add_ee_layer
        return folium.Map(location=self.location, zoom_start=self.zoom_start, height=self.height)


# Class for pulgins  
class pluginsTools:     
        
    # The init method or constructor  
    def __init__(self, my_map):  
            
        # Instance Variable  
        self.my_map = my_map              
    
    # Add a layer control panel to the map.
    def addLayerControl(self):
        self.my_map.add_child(folium.LayerControl())

    #fullscreen
    def addFullscreen(self):
        plugins.Fullscreen().add_to(self.my_map)

    #GPS
    def addLocateControl(self):
        plugins.LocateControl().add_to(self.my_map)

    #mouse position
    def addMousePosition(self):
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(self.my_map)


    #Measure Tool
    def addMeasureControl(self):
        plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(self.my_map)
        

    def addDrawTool(self):
        plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(self.my_map)     


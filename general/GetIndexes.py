# import Google earth engine module
import ee
import geetools

# get indexes
def getNDVI(image):
    
    # Normalized difference vegetation index (NDVI)
    ndvi = image.normalizedDifference(['nir','red']).rename("ndvi")
    image = image.addBands(ndvi)
  
    return(image)



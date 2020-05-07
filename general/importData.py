# import Google earth engine module
import ee
import geetools
#Authenticate the Google earth engine with google account
ee.Initialize()


inBands = ee.List(['QA60','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12']);
outBands = ee.List(['QA60','blue','green','red','re1','re2','re3','nir','re4','waterVapor','cirrus','swir1','swir2']);
 
CloudCoverMax = 20

def importData(studyArea,startDate,endDate):
 
    # Get Sentinel-2 data
    s2s =(ee.ImageCollection('COPERNICUS/S2')
          .filterDate(startDate,endDate)
          .filterBounds(studyArea)
          .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',CloudCoverMax))
          .filter(ee.Filter.lt('CLOUD_COVERAGE_ASSESSMENT',CloudCoverMax)))
    
    def scaleBands(img):
        prop = img.toDictionary()
        t = img.select(['QA60','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B10','B11','B12']).divide(10000)
        t = t.addBands(img.select(['QA60'])).set(prop).copyProperties(img,['system:time_start','system:footprint'])
        return ee.Image(t)
    
    
    s2s = s2s.map(scaleBands)
    s2s = s2s.select(inBands,outBands)
   
    
    return s2s

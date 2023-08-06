import os
import numpy as np
from osgeo import gdal
from glob import glob


def ARVI(landsat_dir, arvi_out):
    # Create list with file names
    red = glob(landsat_dir + "/*B4.tif")
    nir = glob(landsat_dir + "/*B5.tif")
    blue = glob(landsat_dir + "/*B2.tif")

    # Open with gdal & create numpy arrays
    gdal.UseExceptions()
    gdal.AllRegister()
    np.seterr(divide='ignore', invalid='ignore')
    NIR_path = gdal.Open(os.path.join(landsat_dir, nir[0]))
    nir_band = NIR_path.GetRasterBand(1).ReadAsArray().astype(np.float32)
    red_path = gdal.Open(os.path.join(landsat_dir, red[0]))
    red_band = red_path.GetRasterBand(1).ReadAsArray().astype(np.float32)
    blue_path = gdal.Open(os.path.join(landsat_dir, blue[0]))
    blue_band = blue_path.GetRasterBand(1).ReadAsArray().astype(np.float32)
    snap = gdal.Open(os.path.join(landsat_dir, red[0]))

    # Perform Calculation
    arvi = ((nir_band - (2 * red_band) + blue_band) / (nir_band + (2 * red_band) + blue_band))

    # Save Raster
    if os.path.exists(arvi_out):
        raise IOError('ARVI raster already created')
    if not os.path.exists(arvi_out):
        driver = gdal.GetDriverByName('GTiff')
        metadata = driver.GetMetadata()
        shape = arvi.shape
        dst_ds = driver.Create(arvi_out, xsize=shape[1], ysize=shape[0], bands=1, eType=gdal.GDT_Float32)
        proj = snap.GetProjection()
        geo = snap.GetGeoTransform()
        dst_ds.SetGeoTransform(geo)
        dst_ds.SetProjection(proj)
        dst_ds.GetRasterBand(1).WriteArray(arvi)
        dst_ds.FlushCache()
        dst_ds = None

    return arvi, print('ARVI created.')

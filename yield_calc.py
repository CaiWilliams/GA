from yield_model import *
import os
import pandas as pd

def calulate_yield_setup(location):
    irradiance_dir = os.path.join(os.getcwd(),'Yield','Locations',location,location+'_Irradiance.csv')
    weather_dir = os.path.join(os.getcwd(),'Yield','Locations',location,location+'_weather_clean.csv')
    lat_lon = pd.read_csv(os.path.join(os.getcwd(),'Yield','Locations','Lat_Lon.csv'),index_col=0)
    lat_lon = lat_lon[lat_lon.index == location]
    latitude = lat_lon['Latitude'].values[0]
    longitude = lat_lon['Longitude'].values[0]


    Data = Copernicus(irradiance_dir)
    Data.convert_time()
    Data.irradiation_components()

    RandomLoc = Farm(latitude, longitude, 0, 0.3)
    RandomLoc.load_weather_csv_2(weather_dir)

    RandomLoc_Sun = Sun(RandomLoc, Data)
    RandomLoc_Sun.timing()
    RandomLoc_Sun.heliocentric_properties()
    RandomLoc_Sun.geocentric_lat_long()
    RandomLoc_Sun.nutatiion_in_longitude_and_obliquity()
    RandomLoc_Sun.true_obliquity()
    RandomLoc_Sun.apparent_sun_longitude()
    RandomLoc_Sun.apparent_sideral_time_GreenWich()
    RandomLoc_Sun.geocentric_sun_right_ascension()
    RandomLoc_Sun.geocentric_declenation()
    RandomLoc_Sun.observer_hour_angle()
    RandomLoc_Sun.equation_of_time()
    RandomLoc_Sun.topocentric_sun_right_ascension()
    RandomLoc_Sun.topocentirc_sun_zenith()
    RandomLoc_Sun.topocentric_sun_azimuth()
    RandomLoc_Sun.air_mass()
    RandomLoc_Sun.clearness()

    tilt = (latitude * 0.87) + 3.1
    ModuleLoc = Module(0, tilt, RandomLoc, RandomLoc_Sun)
    ModuleLoc.Angle_Of_Incident()
    ModuleLoc.Beam_Irradiance()
    ModuleLoc.Diffuse_Irradiance()
    # ModuleLoc.Perez_Diffuse_Irradiance()
    ModuleLoc.Reflected_Irradiance()
    ModuleLoc.Total_Irradiance()
    ModuleLoc.Temperature(48)

    return ModuleLoc

def calculate_yield(ModuleLoc, coefficeints_filename):

    coeff_dir =os.path.join(os.getcwd(),'Yield_Coefficients',coefficeints_filename)
    Power = Huld(ModuleLoc, coeff_dir, 1000, 25, 300)
    Power.load_coefficients()
    Power.normalised_irradiance_and_Temperature()
    Power.module_power()
    return Power.power*(1-0.14)

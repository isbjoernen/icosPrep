#!/usr/bin/env python

from dataclasses import dataclass, field
from numpy import  ndarray, linspace #,  unique
from typing import List
#from loguru import logger
#from cartopy.io import shapereader
#from shapely.geometry import Point
#from shapely.ops import unary_union
#from typing import List, Union, Tuple
#from shapely.prepared import prep
#import xarray as xr
#from numpy.typing import NDArray
from numpy import pi,  zeros,  float64,  sin, diff,  arange




        

@dataclass
class Grid:
    lon0 : float = None
    lon1 : float = None
    lat0 : float = None
    lat1 : float = None
    dlon : float = None
    dlat : float = None
    nlon : int = None
    nlat : int = None
    latb : ndarray = field(default=None, repr=False, compare=False)
    latc : ndarray = field(default=None, repr=False, compare=False)
    lonb : ndarray = field(default=None, repr=False, compare=False)
    lonc : ndarray = field(default=None, repr=False, compare=False)
    radius_earth : float = field(default=6_378_100.0, repr=False)

    def __post_init__(self):
        """
        Ensure that all variables are set. The region can be initialized:
        - by specifying directly lat/lon coordinates (set type to b if these are boundaries)
        - by specifying lonmin, lonmax and dlon (and same in latitude)
        - by specifying lonmin, dlon and nlon (and sams in latitude)
        """

        # Set the longitudes first
        if self.dlon is None :
            if self.lonc is not None :
                self.dlon = self.lonc[1] - self.lonc[0]
            elif self.lonb is not None :
                self.dlon = self.lonb[1] - self.lonb[0]
            elif self.lon0 is not None and self.lon1 is not None and self.nlon is not None :
                self.dlon = (self.lon1 - self.lon0)/self.nlon
            # logger.debug(f"Set {self.dlon = }")

        if self.lon0 is None:
            if self.lonb is not None :
                self.lon0 = self.lonb.min()
            elif self.lonc is not None :
                self.lon0 = self.lonc.min() - self.dlon / 2
            # logger.debug(f"Set {self.lon0 = }")

        if self.nlon is None :
            if self.lonc is not None :
                self.nlon = len(self.lonc)
            elif self.lonb is not None :
                self.nlon = len(self.lonb) - 1
            elif self.lon0 is not None and self.lon1 is not None and self.dlon is not None :
                nlon = (self.lon1 - self.lon0) / self.dlon
                assert abs(nlon - round(nlon)) < 1.e-7, f'{nlon}, {self.lon1=}, {self.lon0=}, {self.dlon=}'
                self.nlon = round(nlon)

        # At this stage, we are sure to have at least dlon, lonmin and nlon, so use them only:`
        if self.lon1 is None :
            self.lon1 = self.lon0 + self.nlon * self.dlon

        if self.lonb is None :
            self.lonb = linspace(self.lon0, self.lon1, self.nlon + 1)

        if self.lonc is None :
            self.lonc = linspace(self.lon0 + self.dlon/2., self.lon1 - self.dlon/2., self.nlon)

        # Repeat the same thing for the latitudes:
        if self.dlat is None :
            if self.latc is not None :
                self.dlat = self.latc[1] - self.latc[0]
            elif self.lonb is not None :
                self.dlat = self.latb[1] - self.latb[0]
            elif self.lat0 is not None and self.lat1 is not None and self.nlat is not None :
                self.dlat = (self.lat1 - self.lat0)/self.nlat

        if self.lat0 is None:
            if self.latb is not None :
                self.lat0 = self.latb.min()
            elif self.latc is not None :
                self.lat0 = self.latc.min() - self.dlat / 2

        if self.nlat is None :
            if self.latc is not None :
                self.nlat = len(self.latc)
            elif self.latb is not None :
                self.nlat = len(self.latb) - 1
            elif self.lat0 is not None and self.lat1 is not None and self.dlat is not None :
                nlat = (self.lat1 - self.lat0) / self.dlat
                assert abs(nlat - round(nlat)) < 1.e-7
                self.nlat = round(nlat)

        # At this stage, we are sure to have at least dlon, lonmin and nlon, so use them only:
        if self.lat1 is None :
            self.lat1 = self.lat0 + self.nlat * self.dlat

        if self.latb is None :
            self.latb = linspace(self.lat0, self.lat1, self.nlat + 1)

        if self.latc is None :
            self.latc = linspace(self.lat0 + self.dlat/2., self.lat1 - self.dlat/2., self.nlat)

#        self.area = self.calc_area()

        self.round()

    def round(self, decimals=5):
        """
        Round the coordinates
        """
        self.latc = self.latc.round(decimals)
        self.latb = self.latb.round(decimals)
        self.lonc = self.lonc.round(decimals)
        self.lonb = self.lonb.round(decimals)
        self.lon0 = round(self.lon0, decimals)
        self.lat0 = round(self.lat0, decimals)
        self.lon1 = round(self.lon1, decimals)
        self.lat1 = round(self.lat1, decimals)

    @property
    def area(self) -> ndarray :
        return self.calc_area()

    @property
    def extent(self) -> List[float]:
        return [self.lon0, self.lon1, self.lat0, self.lat1]

    def calc_area(self):
        dlon_rad = self.dlon * pi / 180.
        area = zeros((self.nlat+1, self.nlon), float64)
        lats = ( pi / 180. ) * self.latb
        for ilat, lat in enumerate(lats):
            area[ilat, :] = self.radius_earth**2 * dlon_rad * sin(lat)
        return diff(area, axis=0)


    @property
    def indices(self):
        return arange(self.area.size)

    @property
    def shape(self):
        return (self.nlat, self.nlon)

    def __getitem__(self, item):
        """
        Enables reading the attributes as dictionary items.
        This enables constructing methods that can take indifferently a Grid or dict object.
        """
        return getattr(self, item)

    def __le__(self, other):
        return (self.lon0 >= other.lon0) & (self.lon1 <= other.lon1) & (self.lat0 >= other.lat0) & (self.lat1 <= other.lat1)

    def __lt__(self, other):
        return (self.lon0 > other.lon0) & (self.lon1 < other.lon1) & (self.lat0 > other.lat0) & (self.lat1 < other.lat1)


def grid_from_rc(ymlContents, name=None):
    try:
        lat0=ymlContents['run']['region']['lat0']  # 33.0
        lat1=ymlContents['run']['region']['lat1']   #73.0
        lon0=ymlContents['run']['region']['lon0']  # -15.0
        lon1=ymlContents['run']['region']['lon1']   #35.0
    except:
        lat0=float(33.0)
        lat1=float(73.0)
        lon0=float(-15.0)
        lon1=float(35.0)
    try:
        dlat=ymlContents['run']['region']['dlat']  # 0.25
        dlon=ymlContents['run']['region']['dlon']  # 0.25
    except:
        dlat=float(0.25)
        dlon=float(0.25)
    try:
        nlat=ymlContents['run']['region']['nlat']  # 0.25
        nlon=ymlContents['run']['region']['nlon']  # 0.25
    except:
        nlat=int(160)
        nlon=int(200)
    #lon0 = rcf.rcfGet(f'{pfx0}lon0', default=rcf.rcfGet(f'{pfx1}lon0', default=None))
    #lon1 = rcf.rcfGet(f'{pfx0}lon1', default=rcf.rcfGet(f'{pfx1}lon1', default=None))
    #dlon = rcf.rcfGet(f'{pfx0}dlon', default=rcf.rcfGet(f'{pfx1}dlon', default=None))
    #nlon = rcf.rcfGet(f'{pfx0}nlon', default=rcf.rcfGet(f'{pfx1}nlon', default=None))
    #lat0 = rcf.rcfGet(f'{pfx0}lat0', default=rcf.rcfGet(f'{pfx1}lat0', default=None))
    #lat1 = rcf.rcfGet(f'{pfx0}lat1', default=rcf.rcfGet(f'{pfx1}lat1', default=None))
    #dlat = rcf.rcfGet(f'{pfx0}dlat', default=rcf.rcfGet(f'{pfx1}dlat', default=None))
    #nlat = rcf.rcfGet(f'{pfx0}nlat', default=rcf.rcfGet(f'{pfx1}nlat', default=None))
    return Grid(lon0=lon0, lat0=lat0, lon1=lon1, lat1=lat1, dlon=dlon, dlat=dlat, nlon=nlon, nlat=nlat)


def extractt(s, entries):
    val=None
    for entry in entries:
        if (s in entry):
            idx= entry.find(':')
            try:
                val=float(entry[idx+1:])
                break
            except:
                pass
    return(val)
    
def str2grid(gridStr) :
    #   grid: ${Grid:{lon0:-15.000,lat0:33.000,lon1:35.000,lat1:73.000,dlon:0.25000, dlat:0.25000}}
    idx = gridStr.find('lon0')    
    s=gridStr[idx:-2]
    entries=s.split(',')
    flon0=extractt('lon0', entries)
    flon1=extractt('lon1', entries)
    flat0=extractt('lat0', entries)
    flat1=extractt('lat1', entries)
    fdlon=extractt('dlon', entries)
    fdlat=extractt('dlat', entries)
    if(flon0 is None):
        flon0=float(-15.0)
    if(flon1 is None):
        flon1=float(35.0)
    if(flat0 is None):
        flat0=float(33.0)
    if(flat1 is None):
        flat1=float(73.0)
    if(fdlon is None):
        fdlon=float(0.25)
    if(fdlat is None):
        fdlat=float(0.25)
    nlon=int(((flon1 - flon0)/fdlon) + 0.5)
    nlat=int(((flat1 - flat0)/fdlon) + 0.5)
    grid = Grid(lon0=flon0,  lon1=flon1, dlon=fdlon, nlon=nlon, lat0=flat0, lat1=flat1, dlat=fdlat, nlat=nlat)
    return(grid)
    
    
    

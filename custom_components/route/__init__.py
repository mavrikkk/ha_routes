"""The route component."""

import os
from shutil import copyfile

import logging
import voluptuous as vol
from homeassistant.core import callback
from homeassistant.const import (CONF_TOKEN, CONF_TIME_ZONE, CONF_DEVICES)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType, HomeAssistantType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "route"

CONF_NUMBER_OF_DAYS = 'days'
DEFAULT_NUMBER_OF_DAYS = 10
CONF_MIN_DST = 'mindst'
DEFAULT_MIN_DST = 0.1

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema(
               {vol.Optional(CONF_NUMBER_OF_DAYS, default=DEFAULT_NUMBER_OF_DAYS): cv.positive_int, 
                vol.Optional(CONF_MIN_DST, default=DEFAULT_MIN_DST): cv.small_float, 
                vol.Required(CONF_TIME_ZONE): cv.string, 
                vol.Required(CONF_TOKEN): cv.string,
                vol.Required(CONF_DEVICES): vol.All(cv.ensure_list,),
                })}, extra=vol.ALLOW_EXTRA,)





async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:

    try:
        mindistance = config[DOMAIN][CONF_MIN_DST]
        numberofdays = config[DOMAIN][CONF_NUMBER_OF_DAYS]
        timezone = config[DOMAIN][CONF_TIME_ZONE]
        token = config[DOMAIN][CONF_TOKEN]
        devices = config[DOMAIN][CONF_DEVICES]
        haddr = config["http"]["base_url"]
        myroute = Route(hass, mindistance, numberofdays, timezone, token, devices, haddr)
    except:
        _LOGGER.error("Check your config")
        return False
    myroute.createFiles()
    return True





class Route:

    def __init__(self, hass, mindistance, numberofdays, timezone, token, devices, haddr):
        self.hass = hass
        self._mindistance = mindistance
        self._numberofdays = numberofdays
        self._timezone = timezone
        self._token = token
        self._devices = devices
        self._haddr = haddr

    def createFiles(self):
        curr_dir = os.getcwd()
        dirExists = os.path.exists(curr_dir + '/www/' + DOMAIN)
        if not dirExists:
            os.mkdir(curr_dir + '/www/' + DOMAIN)
        copyfile(curr_dir + '/custom_components/' + DOMAIN + '/index.html', curr_dir + '/www/' + DOMAIN + '/index.html')
        copyfile(curr_dir + '/custom_components/' + DOMAIN + '/route.html', curr_dir + '/www/' + DOMAIN + '/route.html')
        
        with open(curr_dir + '/www/' + DOMAIN + '/route.html', 'r') as file :
            filedata = file.read()
        filedata = filedata.replace('number_of_days_variable', str(self._numberofdays))
        filedata = filedata.replace('time_zone_variable', "'" + self._timezone + "'")
        filedata = filedata.replace('access_token_variable', self._token)
        filedata = filedata.replace('haddr_variable', "'" + self._haddr + "'")
        filedata = filedata.replace('minimal_distance_variable', str(self._mindistance))
        devices_var = '['
        for device in self._devices:
            devices_var = devices_var + "'" + device + "',"
        if devices_var == '[':
            devices_var = '[]'
        else:
            devices_var = devices_var[:-1] + ']'
        filedata = filedata.replace('array_of_devices_variable', devices_var)
        with open(curr_dir + '/www/' + DOMAIN + '/route.html', 'w') as file:
            file.write(filedata)

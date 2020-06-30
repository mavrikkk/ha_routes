"""The route component."""

import os
from datetime import datetime
from datetime import timedelta
from shutil import copyfile
from aiohttp import web

import logging
import voluptuous as vol
from homeassistant.core import callback
from homeassistant.const import (CONF_TOKEN, CONF_TIME_ZONE, CONF_DEVICES)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.components.http import HomeAssistantView
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.dispatcher import async_dispatcher_send

_LOGGER = logging.getLogger(__name__)

DOMAIN = "route"

SUPPORTED_DOMAINS = ["sensor"]

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
    hass.data[DOMAIN] = {}
    myconfig = {
        "mindst": config[DOMAIN][CONF_MIN_DST],
        "numofd": config[DOMAIN][CONF_NUMBER_OF_DAYS],
        "tz": config[DOMAIN][CONF_TIME_ZONE],
        "token": config[DOMAIN][CONF_TOKEN],
        "devs": config[DOMAIN][CONF_DEVICES],
        "haddr": config["http"]["base_url"],
    }

    sensors_gps = hass.data[DOMAIN]["sensors_gps"] = SensorsGps(hass,myconfig)

    try:
        await sensors_gps.update()
    except:
        _LOGGER.warning("Error creating sensors")
        return False

    async_track_time_interval(hass, sensors_gps.async_update, timedelta(seconds=60))

    for platform in SUPPORTED_DOMAINS:
        hass.async_create_task(async_load_platform(hass, platform, DOMAIN, {}, config))

    try:
        hass.http.register_view(Route(hass, myconfig))
        hass.components.frontend.async_register_built_in_panel(
            "iframe",
            "Routes",
            "mdi:routes",
            "myroute",
            {"url": "/route/route.html"},
            require_admin=False,
        )
    except:
        _LOGGER.error("Error creating panel")
        return False

    return True





class Route(HomeAssistantView):
    url = r"/route/{requested_file:.+}"
    name = "route"
    requires_auth = False

    def __init__(self, hass, myconfig):
        self.hass = hass
        self._cfg = myconfig
        self.createFiles()

    async def get(self,request,requested_file):
        try:
            curr_dir = os.getcwd()
            path = curr_dir + '/custom_components/' + DOMAIN + '/route_temp.html'
            return web.FileResponse(path)
        except:
            return web.Response(status=404)

    def createFiles(self):
        try:
            curr_dir = os.getcwd()
            pathdomain = curr_dir + '/custom_components/' + DOMAIN
            with open(pathdomain + '/route.html', 'r') as file:
                filedata = file.read()
            filedata = filedata.replace('number_of_days_variable', str(self._cfg["numofd"]))
            filedata = filedata.replace('time_zone_variable', "'" + self._cfg["tz"] + "'")
            filedata = filedata.replace('access_token_variable', self._cfg["token"])
            filedata = filedata.replace('haddr_variable', "'" + self._cfg["haddr"] + "'")
            filedata = filedata.replace('minimal_distance_variable', str(self._cfg["mindst"]))
            devices_var = '['
            for device in self._cfg["devs"]:
                entity_domain = device.split('.')[0]
                fullname = device
                friendly_name = ''
                if self.hass.states.get(device) != None:
                    friendly_name = self.hass.states.get(device).attributes['friendly_name']
                if friendly_name == '':
                    friendly_name = device
                if entity_domain == 'device_tracker':
                    fullname = 'sensor.virtual_'+device.replace(".", "_")
                devices_var = devices_var + "['" + friendly_name + "', '" + fullname + "'],"
            if devices_var == '[':
                devices_var = '[]'
            else:
                devices_var = devices_var[:-1] + ']'
            filedata = filedata.replace('array_of_devices_variable', devices_var)
            with open(pathdomain + '/route_temp.html', 'w') as file:
                file.write(filedata)
        except:
            _LOGGER.error("coudnt copy files")



class SensorsGps:

    def __init__(self, hass, mycfg):
        self.hass = hass
        self.states = {}
        self._cfg = mycfg
        self._devs = self._cfg["devs"]



    async def update(self):
        self.getDeviceTrackers()



    async def async_update(self, now, **kwargs) -> None:
        try:
            await self.update()
        except:
            _LOGGER.warning("Update failed")
            return
        async_dispatcher_send(self.hass, DOMAIN)



    def getDeviceTrackers(self):
        timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for device in self._devs:
            entity_domain = device.split('.')[0]
            if entity_domain == "device_tracker":
                lat = 0
                lon = 0
                if self.hass.states.get(device) != None:
                    lat = self.hass.states.get(device).attributes['latitude']
                    lon = self.hass.states.get(device).attributes['longitude']
                self.states[device]=[timenow,lat,lon]

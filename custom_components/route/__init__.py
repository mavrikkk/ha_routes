"""The route component."""

import os
import datetime
from shutil import copyfile
from aiohttp import web

import logging
import voluptuous as vol
from homeassistant.core import callback
from homeassistant.const import (CONF_TOKEN, CONF_TIME_ZONE, CONF_DEVICES)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.components.http import HomeAssistantView

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
        myconfig = {
            "mindst": config[DOMAIN][CONF_MIN_DST],
            "numofd": config[DOMAIN][CONF_NUMBER_OF_DAYS],
            "tz": config[DOMAIN][CONF_TIME_ZONE],
            "token": config[DOMAIN][CONF_TOKEN],
            "devs": config[DOMAIN][CONF_DEVICES],
            "haddr": config["http"]["base_url"],
        }
        hass.http.register_view(Route(hass, myconfig))
        hass.components.frontend.async_register_built_in_panel(
            "iframe",
            "route",
            "mdi:routes",
            "route",
            {"url": "/route/route.html"},
            require_admin=False,
        )
    except:
        _LOGGER.error("Check your config")
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
                devices_var = devices_var + "'" + device + "',"
            if devices_var == '[':
                devices_var = '[]'
            else:
                devices_var = devices_var[:-1] + ']'
            filedata = filedata.replace('array_of_devices_variable', devices_var)
            with open(pathdomain + '/route_temp.html', 'w') as file:
                file.write(filedata)
        except:
            _LOGGER.error("coudnt copy files")

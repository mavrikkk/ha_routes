#!/usr/local/bin/python3
# coding: utf-8

import time
import requests
import json
import math

import logging

from datetime import datetime
from datetime import timedelta

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_ID = 'entityid'
CONF_SITE = 'haddr'
CONF_TOKEN = 'token'
CONF_NAME = 'name'

DEFAULT_NAME = 'Route'

SCAN_INTERVAL = timedelta(seconds=300)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ID): cv.string,
    vol.Required(CONF_SITE): cv.string,
    vol.Required(CONF_TOKEN): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):

    name = config.get(CONF_NAME)
    myid = config.get(CONF_ID)
    haddr = config.get(CONF_SITE)
    token = config.get(CONF_TOKEN)

    add_devices([MyRoute(name, myid, haddr, token)])
    
    
    
class MyRoute(Entity):

    def __init__(self, name, myid, haddr, token):
        self._name = name
        self._myid = myid
        self._haddr = haddr
        self._token = token
        self._data = '[]'
        self._last_run = None
        self.putInfoTo()

    def getInfoFrom(self):
        dayBegin = time.strftime("%Y-%m-%dT00:00:00+04:00")
        header = {'Authorization': 'Bearer ' + self._token, 'content-type': 'application/json'}
        response = requests.get(self._haddr + '/api/history/period/' + dayBegin + '?filter_entity_id=' + self._myid, headers=header)
        data = response.json()[0]
        if data != None and data != '' and len(data) > 0:
            self._data = self.getCoordinates(data)
            if self._data != '':
                self._last_run = time.strftime("%Y.%m.%d-%H:%M")    
                
    def putInfoTo(self):
        cfgdir = '/home/homeassistant/.homeassistant'
        datenow = str(time.strftime('%Y.%m.%d-%H:%M:%S'))
        try:
            f = open(cfgdir + '/www/route/route.html', 'w')
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("<meta charset='utf-8'>\n")
            f.write("<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate' />\n")
            f.write("<meta http-equiv='Pragma' content='no-cache' />\n")
            f.write("<meta http-equiv='Expires' content='0' />\n")
            f.write("<title>Сегодняшний маршрут</title>\n")
            f.write("<link rel='stylesheet' href='https://unpkg.com/leaflet@1.4.0/dist/leaflet.css' integrity='sha512-puBpdR0798OZvTTbP4A8Ix/l+A4dHDD0DGqYW6RQ+9jxkRFclaxxQb/SJAWZfWAkuyeQUytO7+7N4QKrDh+drA==' crossorigin=''/>\n")
            f.write("<script src='https://unpkg.com/leaflet@1.4.0/dist/leaflet.js' integrity='sha512-QVftwZFqvtRNi0ZyCtsznlKSWOStnDORoefr1enyq5mVL4tmKB3S/EnC3rRJcxCPavG10IcrVGSmPh6Qw5lwrg==' crossorigin=''></script>\n")
            f.write("<script type='text/javascript' src='leaflet.polylineDecorator.js'></script>")
            f.write("<style>html, body, #map {width: 95%; height: 95%; margin-top: 2%; margin-left: 2.5%;}</style>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("<div id='map'></div>\n")
            f.write("<script type='text/javascript'>\n")
            f.write("massiv = " + self._data + ";\n")
            f.write("var mymap = L.map('map').setView([55.755826,37.617], 12);\n")
            f.write("L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?{foo}', {foo: 'bar', attribution: \"Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>\"}).addTo(mymap);\n")
            f.write("if (massiv.length > 0) {\n")
            f.write("for (var i=0; i<massiv.length; i++) {\n")
            f.write("var marker = L.marker(massiv[i]).addTo(mymap);\n")
            f.write("marker.bindTooltip((i+1).toString());}\n")
            f.write("var polyline = L.polyline(massiv, {color: 'red', weight: 2, opacity: 0.5}).addTo(mymap);\n")
            f.write("mymap.fitBounds(polyline.getBounds());\n")
            f.write("polyline.remove();}\n")
            f.write("if (massiv.length > 1) {\n")
            f.write("line = massiv[0];\n")
            f.write("for (var i=1; i<massiv.length; i++) {\n")
            f.write("var polyline = L.polyline([line, massiv[i]], {color: 'red', weight: 2, opacity: 0.7}).addTo(mymap);\n")
            f.write("var arrowHead = L.polylineDecorator(polyline, {patterns: [{offset: '100%', repeat: 0, symbol: L.Symbol.arrowHead({pixelSize: 12, polygon: false, pathOptions: {stroke: true, opacity: 0.7, color: 'red',weight: 2}})}]}).addTo(mymap);\n")
            f.write("line = massiv[i];}}\n")
            f.write("</script>\n")
            f.write("</body>\n")
            f.write("</html>\n")
            f.close()
            
            f = open(cfgdir + '/www/route/index.html', 'w')
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("<meta charset='utf-8'>\n")
            f.write("<meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate' />\n")
            f.write("<meta http-equiv='Pragma' content='no-cache' />\n")
            f.write("<meta http-equiv='Expires' content='0' />\n")
            f.write("<title>Сегодняшний маршрут</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("<script type='text/javascript'>\n")
            f.write("window.onload = function(){\n")
            f.write("var el = document.createElement('iframe');\n")
            f.write("document.body.appendChild(el);\n")
            f.write("el.id = 'iframe';\n")
            f.write("el.style.width = '100%';\n")
            f.write("el.style.height = '100%';\n")
            f.write("el.style.border = 'none';\n")
            f.write("el.style.position = 'absolute';\n")
            f.write("el.src = 'route.html?datetime=' + (new Date()).getTime() + Math.floor(Math.random() * 1000000);\n")
            f.write("};</script>\n")
            f.write("</body>\n")
            f.write("</html>\n")
            f.close()
        except:
            _LOGGER.error('coudnt create file')
            
    def getCoordinates(self, data):
        arr = []
        for stroke in data:
            try:
                lat = float(stroke['attributes']['latitude'])
                lon = float(stroke['attributes']['longitude'])
            except:
                lat = 0
                lon = 0
            if lat != 0 and lon != 0:
                arr.append([lat,lon])
        if len(arr) > 0:
            latA = arr[0][0]
            lonA = arr[0][1]
            arr1 = '[[' + str(latA) + ',' + str(lonA) + '],'
            for obj in arr:
                latB = obj[0]
                lonB = obj[1]
                if latA != latB and lonA != lonB:
                    dst = self.getDistance(latA, lonA, latB, lonB)
                    if dst > 0.1:
                        arr1 = arr1 + '[' + str(latB) + ',' + str(lonB) + '],'
                        latA = obj[0]
                        lonA = obj[1]
            arr1 = arr1[:-1] + ']'
        else:
            arr1 = '[]'
        return arr1

    def getDistance(self, latA, lonA, latB, lonB):
        dst = 0
        try:
            latRadA = math.radians(latA)
            lonRadA = math.radians(lonA)
            latRadB = math.radians(latB)
            lonRadB = math.radians(lonB)
            x = latRadB - latRadA
            y = (lonRadB-lonRadA)*math.cos((latRadB+latRadA)*0.5)
            dst = 6371*math.sqrt(x*x+y*y)
        except:
            _LOGGER.error('couldnt get distance')
        return dst
        
    #for HASS
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._last_run

    def update(self):
        self.getInfoFrom()
        self.putInfoTo()

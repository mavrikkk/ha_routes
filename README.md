# ha_routes
This integration allows you to display the history of today's movements (call it a route or directions) on the map of your HomeAssistant using the Leaflet library

<b>How it works:</b>
<p>Every n seconds (I have configured for 300) the module makes a query (throw official REST API) to the history of the selected "device_tracker" object. The output is an array of coordinates for a certain period of time. This array is passed through the distance filter: if the distance between the previous and current point is less than 50 meters, then the current point is discarded. After that two files are generated ("index.html" and "route.html") in the HomeAssistant's "www" folder. The "index.html" file contains a call to the "route.html" file with a random, dynamically generated parameter, which allows you to always request the current version of the "route.html" file from the server, not cached data. The "route.html" file contains all useful methods and calls.</p>

<b>A few words about security:</b>
<p>All files in the "www" directory of HomeAssistant are public: any file in the "www" directory can be opened in any browser without any authorization, knowing the direct link. In our case, this link is: "http://your_address_homeassistant/local/route/index.html".For more security, you can configure a reverse proxy in front of HomeAssistant service and set the authorization in it. Configuration of most popular web-servers as reverse proxy are on the <a href=https://www.home-assistant.io/docs/ecosystem/nginx>official page</a>. 
After setting up a reverse proxy, you need to add authorization for the necessary pages. This is an independent authorization that is not related to the authorization of the HomeAssistant itself.</p>

<b>Installation:</b>
<p>Place the "route" folder to "config_folder_homeassistant/custom_components/route", do not forget about the rights. If it does not exist, create the folder "config_folder_homeassistant/www" and grant the corresponding rights to it.</p>

<b>Configuration:</b>
<p>Add the following lines in the "configuration.yaml" file:</p>
<pre><code>
sensor:
  - platform: route
    name: route
    entityid: your_device_tracker_entity_id
    haddr: your_address_homeassistant
    token: your_long_life_token
</code></pre>
<p>here "your_device_tracker_entity_id" is the ID of your device_tracker, "your_address_homeassistant" is the external address of your HomeAssistant, "your_long_life_token" is the access token previously received in the frontend of HomeAssistant to use REST API.</p>

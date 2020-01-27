[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# ha_routes
<p>Интеграция позволяет отображать историю сегодняшних перемещений (назовем это маршрутами или направлениями) на карте в вашем HomeAssistant, используя библиотеку Leaflet</p>
<p>This integration allows you to display the history of today's movements (call it a route or directions) on the map of your HomeAssistant using the Leaflet library</p>

<p><b>РУССКИЙ:</b></p>
<p><b>1. Как это работает</b></p>
<p>Каждые n секунд (по умолчанию я выбрал 300) модуль делает запрос (через официальный REST API) к истории выбранного "device_tracker" объекта. На выходе получаем массив координат за выбранный период. Полученный массив прогоняем через фильтр расстояний: если расстояние между предыдущей и текущей точками меньше 50 метров, то текущая точка отбрасывается. После этого генерируются два файла ("index.html" и "route.html") в директории "www". "index.html" содержит вызов файла "route.html" со случайным, динамически генерируемым параметром, что позволяет всегда получать текущую версию файла "route.html" с сервера, без кеширования данных. "route.html" использует библиотеку <a href='https://leafletjs.com/download.html'>Leaflet</a> для отображения карты и маршрута, а также библиотеку <a href='https://github.com/bbecquet/Leaflet.PolylineDecorator'>Leaflet.PolylineDecorator</a> для указания направления движения.</p>

<p><b>2. Немного о безопасности</b></p>
<p>Все файлы в директории "www" публичные: любой файл в директории "www" может быть открыт в любом браузером любым пользователем безо всякой авторизации по прямой ссылке. В данном случае ссылка такая: "http://your_address_homeassistant/local/route/index.html".  Для безопасноти можно поднять реверсивный прокси и поместить службу HomeAssistant за ним, а затем настроить авторизацию уже в нем. Настройка наиболее популярных веб-серверов в качестве реверсивных прокси находятся на <a href=https://www.home-assistant.io/docs/ecosystem/nginx>официальной странице</a>. После настройки реверсивного прокси нужно добавить авторизацию на нужные страницы. Это будет независимая авторизация, никак не связанная с ваторизацией в самом HomeAssistant.</p>

<p><b>3. Установка</b></p>
<p>Содержимое папки "route" скопировать в директорию "config_folder_homeassistant/custom_components/route".</p>

<p><b>4. Настройка</b></p>
<p>Добавьте в ваш файл конфигурации "configuration.yaml" следующие строки:</p>
<pre><code>
sensor:
  - platform: route
    name: route
    haddr: 'your_ha_address'
    entityid: your_device_tracker_entity_id
    timezone: 'your_timezone'
    token: your_long_life_token
</code></pre>
<p>здесь "your_ha_address" - это base_url вашего HA, "your_device_tracker_entity_id" - это ID вашего устройства device_tracker, "your_address_homeassistant" - внешний адрес вашего HomeAssistant, 'your_timezone' - это часовой пояс, например '+03:00', "your_long_life_token" - предварительно полученный во фронтенде HomeAssistant токен доступа для использования REST API.</p>

<p><b>5. TODO</b></p>
<p>- добавить гибкую настройку периода в sensor.py (сейчас задан сегодняшний маршрут)</p>
<p>- мультимаршруты (несколько маршрутов от разных устройств)</p>
<p>- поправить перевод в README.md</p>

<p><b>BAD ENGLISH:</b></p>
<p><b>1. How it works</b></p>
<p>Every n seconds (I have configured for 300) the module makes a query (throw official REST API) to the history of the selected "device_tracker" object. The output is an array of coordinates for a certain period of time. This array is passed through the distance filter: if the distance between the previous and current point is less than 50 meters, then the current point is discarded. After that two files are generated ("index.html" and "route.html") in the HomeAssistant's "www" folder. The "index.html" file contains a call to the "route.html" file with a random, dynamically generated parameter, which allows you to always request the current version of the "route.html" file from the server, not cached data. The "route.html" file use <a href='https://leafletjs.com/download.html'>Leaflet</a> library for draw the map and route and also use <a href='https://github.com/bbecquet/Leaflet.PolylineDecorator'>Leaflet.PolylineDecorator</a> library to draw the direction of movement.</p>

<p><b>2. A few words about security</b></p>
<p>All files in the "www" directory of HomeAssistant are public: any file in the "www" directory can be opened in any browser without any authorization, knowing the direct link. In our case, this link is: "http://your_address_homeassistant/local/route/index.html".For more security, you can configure a reverse proxy in front of HomeAssistant service and set the authorization in it. Configuration of most popular web-servers as reverse proxy are on the <a href=https://www.home-assistant.io/docs/ecosystem/nginx>official page</a>. 
After setting up a reverse proxy, you need to add authorization for the necessary pages. This is an independent authorization that is not related to the authorization of the HomeAssistant itself.</p>

<p><b>3. Installation</b></p>
<p>Place the "route" folder to "config_folder_homeassistant/custom_components/".</p>

<p><b>4. Configuration</b></p>
<p>Add the following lines in the "configuration.yaml" file:</p>
<pre><code>
sensor:
  - platform: route
    name: route
    haddr: 'your_ha_address'
    entityid: your_device_tracker_entity_id
    timezone: 'your_timezone'
    token: your_long_life_token
</code></pre>
<p>here "your_ha_address" - base_url of HA, "your_device_tracker_entity_id" is the ID of your device_tracker, "your_address_homeassistant" is the external address of your HomeAssistant, 'your_timezone' is your timezone, for example '+03:00', "your_long_life_token" is the access token previously received in the frontend of HomeAssistant to use REST API.</p>

<p><b>5. TODO</b></p>
<p>- add period configuration in sensor.py (now is today route)</p>
<p>- multiroutes (few routes from different devices)</p>
<p>- edit English translate in README.md</p>

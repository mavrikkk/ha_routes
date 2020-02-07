[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# ha_routes
<p>Интеграция позволяет отображать историю сегодняшних перемещений (назовем это маршрутами или направлениями) на карте в вашем HomeAssistant, используя библиотеку Leaflet, а также плагин <a href='https://github.com/bbecquet/Leaflet.PolylineDecorator'>leaflet.polylineDecorator.js</a></p>
<p>This integration allows you to display the history of today's movements (call it a route or directions) on the map of your HomeAssistant using the Leaflet library and <a href='https://github.com/bbecquet/Leaflet.PolylineDecorator'>leaflet.polylineDecorator.js</a></p>

<p><b>РУССКИЙ:</b></p>
<p><b>1. Немного о безопасности</b></p>
<p>Все файлы в директории "www" публичные: любой файл в директории "www" может быть открыт в любом браузером любым пользователем безо всякой авторизации по прямой ссылке. В данном случае ссылка такая: "http://your_address_homeassistant/local/route/index.html".  Для безопасноти можно поднять реверсивный прокси и поместить службу HomeAssistant за ним, а затем настроить авторизацию уже в нем. Настройка наиболее популярных веб-серверов в качестве реверсивных прокси находятся на <a href=https://www.home-assistant.io/docs/ecosystem/nginx>официальной странице</a>. После настройки реверсивного прокси нужно добавить авторизацию на нужные страницы. Это будет независимая авторизация, никак не связанная с ваторизацией в самом HomeAssistant.</p>

<p><b>2. Установка</b></p>
<p>Содержимое папки "route" скопировать в директорию "config_folder_homeassistant/custom_components/route".</p>

<p><b>3. Настройка</b></p>
<p>Добавьте в ваш файл конфигурации "configuration.yaml" следующие строки:</p>
<pre><code>
route:
  days: num_days
  mindst: your_min_dst
  time_zone: your_timezone
  token: your_long_life_token
  devices:
    - your_device_tracker_entity_id1
    - your_device_tracker_entity_id2
</code></pre>
<p>здесь "num_days" - это количество дней, для выбора из истории, "your_device_tracker_entity_id" - это ID ваших устройств device_tracker, "your_min_dst" - минимальная дистанция между точками, для отображения на карте, 'your_timezone' - это часовой пояс, например '+03:00', "your_long_life_token" - предварительно полученный во фронтенде HomeAssistant токен доступа для использования REST API.</p>

<p><b>4. TODO</b></p>
<p>- поправить перевод в README.md</p>

<p><b>BAD ENGLISH:</b></p>
<p><b>1. A few words about security</b></p>
<p>All files in the "www" directory of HomeAssistant are public: any file in the "www" directory can be opened in any browser without any authorization, knowing the direct link. In our case, this link is: "http://your_address_homeassistant/local/route/index.html".For more security, you can configure a reverse proxy in front of HomeAssistant service and set the authorization in it. Configuration of most popular web-servers as reverse proxy are on the <a href=https://www.home-assistant.io/docs/ecosystem/nginx>official page</a>. 
After setting up a reverse proxy, you need to add authorization for the necessary pages. This is an independent authorization that is not related to the authorization of the HomeAssistant itself.</p>

<p><b>2. Installation</b></p>
<p>Place the "route" folder to "config_folder_homeassistant/custom_components/".</p>

<p><b>3. Configuration</b></p>
<p>Add the following lines in the "configuration.yaml" file:</p>
<pre><code>
route:
  days: num_days
  mindst: your_min_dst
  time_zone: your_timezone
  token: your_long_life_token
  devices:
    - your_device_tracker_entity_id1
    - your_device_tracker_entity_id2
</code></pre>
<p>here "num_days" is number of days to choose from in history, here "your_min_dst" is minimal distance between two points on map, here "your_device_tracker_entity_id" is the ID of your device_tracker, 'your_timezone' is your timezone, for example '+03:00', "your_long_life_token" is the access token previously received in the frontend of HomeAssistant to use REST API.</p>

<p><b>4. TODO</b></p>
<p>- edit English translate in README.md</p>

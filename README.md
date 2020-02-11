[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# Routes integration

<p>Интеграция позволяет отображать историю перемещений (назовем это маршрутами или направлениями) на карте в вашем HomeAssistant, используя библиотеку Leaflet, а также плагин <a href='https://github.com/bbecquet/Leaflet.PolylineDecorator'>leaflet.polylineDecorator.js</a></p>
<p>This integration allows you to display the history of movements (call it a route or directions) on the map of your HomeAssistant using the Leaflet library and <a href='https://github.com/bbecquet/Leaflet.PolylineDecorator'>leaflet.polylineDecorator.js</a></p>

Что нового:

2020/02/07 Теперь можно задавать список из нескольких устройств, а также выбирать дату

2020/02/11 Теперь на каждой точке указаны дата и время в этой точке

What's new:

2020/02/07 now you can choose more than 1 device and choose date

2020/02/11 now you can see the time on every point

<p><b>РУССКИЙ:</b></p>
<p><b>1. Немного о безопасности</b></p>
<p>Все файлы в директории "www" публичные: любой файл в директории "www" может быть открыт в любом браузером любым пользователем безо всякой авторизации по прямой ссылке. В данном случае ссылка такая: "http://your_address_homeassistant/local/route/index.html".  Для безопасноти можно поднять реверсивный прокси и поместить службу HomeAssistant за ним, а затем настроить авторизацию уже в нем. Настройка наиболее популярных веб-серверов в качестве реверсивных прокси находятся на <a href=https://www.home-assistant.io/docs/ecosystem/nginx>официальной странице</a>. После настройки реверсивного прокси нужно добавить авторизацию на нужные страницы. Это будет независимая авторизация, никак не связанная с ваторизацией в самом HomeAssistant.</p>

<p><b>2. Установка</b></p>
<p>Содержимое папки "route" скопировать в директорию "config_folder_homeassistant/custom_components/route".</p>

<p><b>3. Настройка device_tracker</b></p>
<p>API homeassistant устроен так, что позволяет получать историю только при изменении состояний. Так как состоянием у device_tracker является расположение в какой либо зоне или "not_home", то и координаты будут не все, а только те, которые зафиксированы при смене состояний. Чтобы этого избежать созданим в HA новый template sensor, у которого атрибуты будут скопированы у нужного device_tracker, а состоянием будет last_updated. Таким образом мы получим всю историю перемещений.</p>
<pre><code>
sensor:
  - platform: template
    sensors:
      my_sensor_name:
        value_template: >-
            {{states.your_device_tracker_id.last_updated}}
        attribute_templates:
          latitude: >-
              {{state_attr('your_device_tracker_id','latitude')}}
          longitude: >-
              {{state_attr('your_device_tracker_id','longitude')}}
</code></pre>
<p>здесь your_device_tracker_id - нужный вам трекер, а my_sensor_name - имя вновь создаваемого сенсора</p>

<p><b>4. Настройка</b></p>
<p>Добавьте в ваш файл конфигурации "configuration.yaml" следующие строки:</p>
<pre><code>
route:
  days: num_days
  mindst: your_min_dst
  time_zone: your_timezone
  token: your_long_life_token
  devices:
    - your_sensor_entity_id1
    - your_sensor_entity_id2
</code></pre>
<p>здесь "num_days" - это количество дней, для выбора из истории, "your_sensor_entity_id" - это ID ваших устройств template sensor, "your_min_dst" - минимальная дистанция между точками, для отображения на карте, 'your_timezone' - это часовой пояс, например '+03:00', "your_long_life_token" - предварительно полученный во фронтенде HomeAssistant токен доступа для использования REST API.</p>

<p><b>BAD ENGLISH:</b></p>

<p><b>1. A few words about security</b></p>
<p>All files in the "www" directory of HomeAssistant are public: any file in the "www" directory can be opened in any browser without any authorization, knowing the direct link. In our case, this link is: "http://your_address_homeassistant/local/route/index.html".For more security, you can configure a reverse proxy in front of HomeAssistant service and set the authorization in it. Configuration of most popular web-servers as reverse proxy are on the <a href=https://www.home-assistant.io/docs/ecosystem/nginx>official page</a>. 
After setting up a reverse proxy, you need to add authorization for the necessary pages. This is an independent authorization that is not related to the authorization of the HomeAssistant itself.</p>

<p><b>2. Installation</b></p>
<p>Place the "route" folder to "config_folder_homeassistant/custom_components/".</p>

<p><b>3. Configure the device_tracker</b></p>
<p>The homeassistant API is designed to receive history only when state is change. Since the state of device_tracker is location in some zone or "not_home", then not all coordinates will be, but only those that were fixed when the states changed. You only seem to be able to get list of state change locations (when moving from zones). To avoid this, create a new template sensor in HA, in which the attributes will be copied from the desired device_tracker, and the state will be last_updated. So we get the whole history of movements.</p>
<pre><code>
sensor:
  - platform: template
    sensors:
      my_sensor_name:
        value_template: >-
            {{states.your_device_tracker_id.last_updated}}
        attribute_templates:
          latitude: >-
              {{state_attr('your_device_tracker_id','latitude')}}
          longitude: >-
              {{state_attr('your_device_tracker_id','longitude')}}
</code></pre>
<p>here is your_device_tracker_id - your device tracker id and my_sensor_name - sensor name</p>

<p><b>4. Configuration</b></p>
<p>Add the following lines in the "configuration.yaml" file:</p>
<pre><code>
route:
  days: num_days
  mindst: your_min_dst
  time_zone: your_timezone
  token: your_long_life_token
  devices:
    - your_sensor_entity_id1
    - your_sensor_entity_id2
</code></pre>
<p>here "num_days" is number of days to choose from in history, here "your_min_dst" is minimal distance between two points on map, here "your_sensor_entity_id" is the ID of your template sensor, 'your_timezone' is your timezone, for example '+03:00', "your_long_life_token" is the access token previously received in the frontend of HomeAssistant to use REST API.</p>

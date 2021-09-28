[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# Routes integration

<p>Интеграция позволяет отображать историю перемещений (назовем это маршрутами или направлениями) на карте в вашем HomeAssistant, используя библиотеку Leaflet, а также плагин <a href='https://github.com/bbecquet/Leaflet.PolylineDecorator'>leaflet.polylineDecorator.js</a></p>
<p>This integration allows you to display the history of movements (call it a route or directions) on the map of your HomeAssistant using the Leaflet library and <a href='https://github.com/bbecquet/Leaflet.PolylineDecorator'>leaflet.polylineDecorator.js</a></p>

Что нового:

2021/09/28 Добавил параметр внешнего адреса, так как base_url в новых версиях нет. После установки ОБЯЗАТЕЛЬНО почистите кеш браузера!

2020/06/30 Поддержка последних версий HA. После установки ОБЯЗАТЕЛЬНО почистите кеш браузера!

2020/05/07 В список можно добавлять как sensor так и device_tracker. В том случае, если вы добавили для отслеживания device_tracker в системе автоматически создастся виртуальный сенсор. ВНИМАНИЕ! Убедитесь, что все нужные сенсоры (в том числе и виртуальные) записывают историю в БД.

2020/02/07 Теперь можно задавать список из нескольких устройств, а также выбирать дату

2020/02/11 Теперь на каждой точке указаны дата и время в этой точке

2020/02/12 Боковая панель создается автоматически. Теперь компонент защищен авторизацией HA

What's new:

2021/09/28 Add 'haddr' parameter istead of 'base_url'. Please, clean browser cache after installation!

2020/06/30 Support for last HA versions. Please, clean browser cache after installation!

2020/02/07 now you can choose more than 1 device and choose date

2020/02/11 now you can see the time on every point

2020/02/12 The side panel creates automatically. Now the component is secured by HA authority

<p><b>РУССКИЙ:</b></p>

<p><b>1. Установка</b></p>
<p>Содержимое папки "route" скопировать в директорию "config_folder_homeassistant/custom_components/route".</p>

<p><b>2. Настройка device_tracker</b></p>
<p>API homeassistant устроен так, что позволяет получать историю только при изменении состояний. Так как состоянием у device_tracker является расположение в какой либо зоне или "not_home", то и координаты будут не все, а только те, которые зафиксированы при смене состояний. Чтобы этого избежать необходжимо создать в HA новый sensor, у которого атрибуты будут скопированы у нужного device_tracker, а состоянием будет last_updated. Это происходит автоматически. Вам нужно лишь добавить нужный device_tracker в конфигурационный файл</p>

<p><b>3. Настройка</b></p>
<p>Добавьте в ваш файл конфигурации "configuration.yaml" следующие строки:</p>
<pre><code>
route:
  haddr: your_ha_address
  days: num_days
  mindst: your_min_dst
  time_zone: your_timezone
  token: your_long_life_token
  devices:
    - your_sensor_entity_id1
    - your_device_tracker_entity_id1
</code></pre>
<p>здесь "your_ha_address" - внешний адрес вашего HA, "num_days" - это количество дней, для выбора из истории, "your_sensor_entity_id" - это ID ваших sensor, "your_device_tracker_entity_id" - это ID ваших device_tracker, "your_min_dst" - минимальная дистанция между точками, для отображения на карте, 'your_timezone' - это часовой пояс, например '+03:00', "your_long_life_token" - предварительно полученный во фронтенде HomeAssistant токен доступа для использования REST API.
ВНИМАНИЕ. Для правильной работы интеграции убедитесь, что в конфигурации HA правильно заполнен параметр base_url</p>

<p><b>BAD ENGLISH:</b></p>

<p><b>1. Installation</b></p>
<p>Place the "route" folder to "config_folder_homeassistant/custom_components/".</p>

<p><b>2. Configure the device_tracker</b></p>
<p>The homeassistant API is designed to receive history only when state is change. Since the state of device_tracker is location in some zone or "not_home", then not all coordinates will be, but only those that were fixed when the states changed. You only seem to be able to get list of state change locations (when moving from zones). To avoid this, it is neccecary to create a new sensor in HA, in which the attributes will be copied from the desired device_tracker, and the state will be last_updated. This happens automatically. You only need to add the neccecary device_tracker to the configuration file.</p>

<p><b>3. Configuration</b></p>
<p>Add the following lines in the "configuration.yaml" file:</p>
<pre><code>
route:
  haddr: your_ha_address
  days: num_days
  mindst: your_min_dst
  time_zone: your_timezone
  token: your_long_life_token
  devices:
    - your_sensor_entity_id1
    - your_device_tracker_entity_id1
</code></pre>
<p>here "your_ha_address" is your homeasssistant address, "num_days" is number of days to choose from in history, here "your_min_dst" is minimal distance between two points on map, here "your_sensor_entity_id" is the ID of your template sensor, "your_device_tracker_entity_id" is the ID of your device_tracker, 'your_timezone' is your timezone, for example '+03:00', "your_long_life_token" is the access token previously received in the frontend of HomeAssistant to use REST API. ATTENTION. Make sure the base_url parameter is correctly configured in the HA configuration.yaml</p>

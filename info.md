**Description (Описание)**
<p>This integration allows you to display the history of movements on the map of your HomeAssistant (Интеграция позволяет отображать историю перемещений на карте в вашем HomeAssistant)</p>

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

**pre installation instructions**

<p>The homeassistant API is designed to receive history only when state is change. Since the state of device_tracker is location in some zone or "not_home", then not all coordinates will be, but only those that were fixed when the states changed. You only seem to be able to get list of state change locations (when moving from zones). To avoid this, it is neccecary to create a new sensor in HA, in which the attributes will be copied from the desired device_tracker, and the state will be last_updated. This happens automatically. You only need to add the neccecary device_tracker to the configuration file. ATTENTION. Make sure the base_url parameter is correctly configured in the HA configuration.yaml (API homeassistant устроен так, что позволяет получать историю только при изменении состояний. Так как состоянием у device_tracker является расположение в какой либо зоне или "not_home", то и координаты будут не все, а только те, которые зафиксированы при смене состояний. Чтобы этого избежать нужно создать в HA новый sensor, у которого атрибуты будут скопированы у нужного device_tracker, а состоянием будет last_updated. Это происходит автоматически. Вам нужно лишь добавить нужный device_tracker в конфигурационный файл. ВНИМАНИЕ. Для правильной работы интеграции убедитесь, что в конфигурации HA правильно заполнен параметр base_url) </p>

**installation instructions:**

```yaml
route:
  days: num_days
  mindst: your_min_dst
  time_zone: your_timezone
  token: your_long_life_token
  devices:
    - your_device_tracker_entity_id1
    - your_sensor_entity_id1
```

**Configuration variables:**  
  
key | description  
:--- | :---  
**days (Option)** | is number of days to choose from in history (это количество дней, для выбора из истории)
**mindst (Option)** | is minimal distance between two points on map (минимальная дистанция между точками, для отображения на карте)
**time_zone (Required)** | is your timezone, for example '+03:00' (ваш часовой пояс, например '+03:00')
**token (Required)** | is the access token previously received in the frontend of HomeAssistant to use REST API (предварительно полученный во фронтенде HomeAssistant токен доступа для использования REST API)
**devices (Required)** | the HA entityid's of your device_trackers or sensors(это ID ваших устройств, за которыми будете наблюдать)

**Screenshots (very blurred!!!)**

![example][exampleimg]



***

[exampleimg]: map.jpeg

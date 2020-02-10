**Description (Описание)**
<p>This integration allows you to display the history of movements on the map of your HomeAssistant (Интеграция позволяет отображать историю перемещений на карте в вашем HomeAssistant)</p>

What's new:

2020/02/07 now you can choose more than 1 device and choose date

Что нового:

2020/02/07 Теперь можно задавать список из нескольких устройств, а также выбирать дату

**Example configuration.yaml:**

```yaml
route:
  days: num_days
  mindst: your_min_dst
  time_zone: your_timezone
  token: your_long_life_token
  devices:
    - your_device_tracker_entity_id1
    - your_device_tracker_entity_id2
```



**Configuration variables:**  
  
key | description  
:--- | :---  
**days (Option)** | is number of days to choose from in history (это количество дней, для выбора из истории)
**mindst (Option)** | is minimal distance between two points on map (минимальная дистанция между точками, для отображения на карте)
**time_zone (Required)** | is your timezone, for example '+03:00' (ваш часовой пояс, например '+03:00')
**token (Required)** | is the access token previously received in the frontend of HomeAssistant to use REST API (предварительно полученный во фронтенде HomeAssistant токен доступа для использования REST API)
**devices (Required)** | the HA entityid's of your device_tracker's (это ID ваших устройств, за которыми будете наблюдать)
  
  
  
**!!!IMPORTANT!!! after installation instructions**

<p>After installation the map will be at your_address_homeassistant/local/route/index.html. If you wish, you can add it to the HA menu using panel_iframe or to any HA window via the lovelace card “iframe” (После установки карта будет доступна по прямой ссылке: your_address_homeassistant/local/route/index.html. При желании вы можете добавить ее в меню HA с помощью panel_iframe или в любое окно HA через lovelace card “iframe”).</p>

<p>The homeassistant API is designed to receive history only when state is change. Since the state of device_tracker is location in some zone or "not_home", then not all coordinates will be, but only those that were fixed when the states changed. You only seem to be able to get list of state change locations (when moving from zones). To avoid this, create a new template sensor in HA, in which the attributes will be copied from the desired device_tracker, and the state will be last_updated. So we get the whole history of movements. (API homeassistant устроен так, что позволяет получать историю только при изменении состояний. Так как состоянием у device_tracker является расположение в какой либо зоне или "not_home", то и координаты будут не все, а только те, которые зафиксированы при смене состояний. Чтобы этого избежать созданим в HA новый template sensor, у которого атрибуты будут скопированы у нужного device_tracker, а состоянием будет last_updated. Таким образом мы получим всю историю перемещений.)</p>

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

**Screenshots (very blurred!!!)**

![example][exampleimg]



***

[exampleimg]: map.jpeg

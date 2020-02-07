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



**Screenshots (very blurred!!!)**

![example][exampleimg]



***

[exampleimg]: map.jpeg

#Что это?
* Автоматически меняет текущее сетевое размещение (https://support.apple.com/ru-ru/HT202480) в OS X в зависимости от WiFI-сети
* Автоматически монтирует сетевые ресурсы 
* Работает тихо, есть не просит

##Установка
Прописать в ''settings.json'' сетевые размещения (network locations), SSID'ы соотвествующих сетей, точки монтирования сетевых ресурсов. В locations.py изменить путь до settings.json:
 
```python
  config_file = "/путь-до/settings.json"
```

```shell
chmod +x locations.py
cp locations.py /usr/local/bin/locations
cp locations.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/locations.plist
```
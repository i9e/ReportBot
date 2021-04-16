import requests
import config

def get_address_from_coords(coords):
    PARAMS = {
        "apikey":config.API_YA,
        "format":"json",
        "lang":"ru_RU",
        "kind":"house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str
    except Exception as e:
        return "Не удалось получить адрес"
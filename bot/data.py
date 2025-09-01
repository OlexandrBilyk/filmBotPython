import json
from typing import Union

def get_films(name: str = None) -> Union[dict, list[dict]]:
    """
        This function return list of films or film if name is passed
    """
    with open('bot/films.json', 'r') as fh:
        data = json.load(fh)
    if not name:
        return data
    else: 
        for f in data:
            if f['name'] in name.strip():
                return f
def add_film(film: dict) -> None:
    """
    Function that add film in a data
    """
    data = get_films()
    with open('bot/films.json', 'w') as fh:
        data.append(film)
        json.dump(data, fh, indent=4, ensure_ascii=False)
from time import time
from sys import platform
from json import dump, load
from os import makedirs, path

DEFAULT_DATA = {
    "token": None,
    "access_token": None,
    "username": None,
    "aliases": []
}


def get_adequate_config_path():
    if platform == 'darwin':
        # i dont even fucking know or want to know
        return "~/Library/Preferences/ddge/data.json"
    elif 'win' in platform:
        # same with this
        return "%USERPROFILE%\AppData\Local\ddge\data.json"
    else:
        return "~/.config/ddge.json"


DEFAULT_CONFIG_PATH = get_adequate_config_path()


class Storage:
    def __init__(self, file_path: str = DEFAULT_CONFIG_PATH) -> None:
        expanded = path.expanduser(file_path)
        self.file_path = expanded
        if path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.data = load(f)
        else:
            self.data = {**DEFAULT_DATA}
            self.save()

    def save(self):
        dir = path.dirname(self.file_path)
        if dir:
            if not path.exists(dir):
                makedirs(dir)
        with open(self.file_path, 'w') as f:
            dump(self.data, f)

    @property
    def username(self) -> str:
        return self.data['username']

    @property
    def aliases(self) -> list[dict]:
        return self.data['aliases']

    @property
    def token(self) -> str:
        return self.data['token']

    @property
    def access_token(self) -> str:
        return self.data['access_token']

    def remove_alias(self, key_like: str):
        """`key_like` accepts the index, full alias and alias username(the part before @)"""
        ret = None
        for index, alias in enumerate(self.aliases):
            if key_like == str(index):
                ret = self.data['aliases'].pop(index)
                break
            elif key_like == alias['address']:
                ret = self.data['aliases'].pop(index)
                break
            elif key_like.split("@")[0] == alias['address']:
                ret = self.data['aliases'].pop(index)
                break
        if ret:
            self.save()
            return ret
        raise KeyError(f"Didn't find any aliases matching '{key_like}'")

    def add_alias(self, address):
        alias = {
            "address": address,
            "created": int(time())
            }
        self.data['aliases'].append(alias)
        self.save()
        return alias

    def save_credentials(self, token: str, access_token: str, username: str):
        self.data['token'] = token
        self.data['access_token'] = access_token
        self.data['username'] = username
        self.save()

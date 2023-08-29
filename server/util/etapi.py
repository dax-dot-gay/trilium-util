from trilium_py.client import ETAPI
import requests
from typing import Union

class ExtendedETAPI(ETAPI):
    def get_note_content(self, noteId: str) -> Union[str, bytes]:
        url = f'{self.server_url}/etapi/notes/{noteId}/content'
        res = requests.get(url, headers=self.get_header())
        try:
            return res.content.decode('utf-8')
        except UnicodeDecodeError:
            return res.content
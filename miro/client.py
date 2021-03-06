from typing import List

import requests

from miro.objects.base_miro_object import MiroObjectType
from miro.objects.board import Board
from miro.objects.widgets import Widget
from miro.utils import (get_json_or_raise_exception,
                        UnexpectedResponseException, create_widget_by_type)


class MiroApiClient:

    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.auth_header_as_dict = {
            'Authorization': f'Bearer {self.auth_token}'
        }

    def get_all_widgets_by_board_id(self, board_id: str) -> List[Widget]:
        url = f'{self.base_url}/v1/boards/{board_id}/widgets/'
        response = requests.get(url, headers=self.auth_header_as_dict)
        collection_json = get_json_or_raise_exception(response)

        try:
            widgets_json = collection_json['data']
            return [create_widget_by_type(w) for w in widgets_json]
        except Exception as e:
            raise UnexpectedResponseException(cause=e)

    def get_board_by_id(self, board_id: str) -> Board:
        url = f'{self.base_url}/v1/boards/{board_id}'
        response = requests.get(url, headers=self.auth_header_as_dict)
        board_json = get_json_or_raise_exception(response)

        try:
            return Board(
                obj_id=board_json['id'],
                name=board_json['name'],
                description=board_json['description']
            )
        except Exception as e:
            raise UnexpectedResponseException(cause=e)

    def create_board(self, name: str, description: str) -> Board:
        headers = {
            'Content-Type': 'application/json'
        }
        headers.update(self.auth_header_as_dict)

        board_data = {
            'name': name,
            'description': description
        }

        url = f'{self.base_url}/v1/boards'
        response = requests.post(url, json=board_data, headers=headers)

        board_json = get_json_or_raise_exception(response)

        try:
            return Board(
                obj_id=board_json['id'],
                name=board_json['name'],
                description=board_json['description']
            )
        except Exception as e:
            raise UnexpectedResponseException(cause=e)

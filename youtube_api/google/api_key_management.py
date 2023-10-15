from datetime import datetime
import logging
import os
import random
import time
from typing import List

import googleapiclient.discovery
import googleapiclient.errors


class ApiKeyManager:

    def __init__(self,
                 api_keys: List[str] = None,
                 wait_mins: int = 60):
        if api_keys is None:
            api_keys = self.load_keys()
        random.shuffle(api_keys)
        self.api_key_to_exceeded_time = {
            key: datetime(2000, 1, 1) for key in api_keys}
        self.wait_mins = wait_mins

    @staticmethod
    def load_keys(
            keys_dir: str = os.environ['YOUTUBE_API_KEYS_DIR']
    ) -> List[str]:
        keys = []
        for file_name in os.listdir(keys_dir):
            if not file_name.endswith('.key'):
                continue
            file_path = os.path.join(keys_dir, file_name)
            with open(file_path) as f:
                try:
                    key = f.read().strip()
                except Exception as e:
                    print(file_path)
                    raise e
                keys.append(key)
        return keys

    @staticmethod
    def _get_mins_diff(exceeded_time: datetime) -> int:
        diff_secs = (datetime.now() - exceeded_time).total_seconds()
        return int(round(diff_secs / 60, 0))

    def _get_next_available_key(self) -> str | None:
        logging.info('Looking for next available api key...')
        key_diff = [
            {'key': k, 'diff': self._get_mins_diff(t)}
            for k, t in self.api_key_to_exceeded_time.items()]
        for x in key_diff:
            logging.info('Api key "%s" status: reported exceeded %s mins ago.'
                         % (x['key'], x['diff']))
        key_diff = list(reversed(sorted(key_diff, key=lambda x: x['diff'])))
        next_key, diff = key_diff[0]['key'], key_diff[0]['diff']
        if diff < self.wait_mins:
            logging.info(f'No keys expired less than {self.wait_mins} mins '
                         f'ago.')
            return None
        else:
            logging.info(f'Returning new api key "{next_key}".')
            return next_key

    def get_key(self) -> str:
        while True:
            api_key = self._get_next_available_key()
            if not api_key:
                time.sleep(self.wait_mins * 60)
            else:
                return api_key

    def report_quota_exceeded(self, api_key: str) -> None:
        exceeded_time = datetime.now()
        exceeded_time_str = exceeded_time.strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f'Api key "{api_key}" quota reported '
                     f'exceeded at {exceeded_time_str}.')
        self.api_key_to_exceeded_time[api_key] = exceeded_time


class ResourceManager:

    def __init__(self, api_key_manager: ApiKeyManager):
        self.api_key_manager = api_key_manager
        # since getting a resource can involve waiting, only try when asked
        # for a resource
        self.current_api_key = None
        self.current_resource = None

    @staticmethod
    def _get_resource(api_key: str):
        if not api_key:
            api_key = os.environ['API_KEY']
        return googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=api_key)

    def _set_current_resource(self) -> None:
        self.current_api_key = self.api_key_manager.get_key()
        self.current_resource = self._get_resource(self.current_api_key)

    def get_resource(self) -> googleapiclient.discovery.Resource:
        if not self.current_resource:
            self._set_current_resource()
        return self.current_resource

    def report_quota_exceeded(self) -> None:
        self.api_key_manager.report_quota_exceeded(self.current_api_key)
        self.current_api_key = None
        self.current_resource = None

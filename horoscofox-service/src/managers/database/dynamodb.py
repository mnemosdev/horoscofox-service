import boto3
from src.settings import (DYNAMODB_TABLE_NAME, DYNAMODB_REGION)
from src.managers.database.exceptions import InvalidHoroscopeFormat, InvalidHoroscopeAttribute
from datetime import date, datetime
# Get the service resource.
dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_REGION)


class Horoscope:
    _table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    _get_keys = ['sign', 'astrologer', 'date_start']
    _put_keys = ['date_end', 'text']

    def __init__(self):
        pass

    def get(self, keys):
        response = self._table.get_item(Key=keys)
        return response

    def get_item(self, keys, format=None):
        return self.get(keys)['Item']

    def insert(self, item):
        if self._validate_item(item):
            return self._table.put_item(Item=item)
        else:
            error_message = ("Expect " + str(self._get_keys+self._put_keys) +
                             " but i've " + str(item.keys()))
            raise InvalidHoroscopeFormat(error_message)

    def update(self, key, value):
        self._add_value(key, value)

    def delete(self, keys):
        self._table.delete_item(Key=keys)

    def _validate_item(self, item):
        return (self._validate_key_set(list(item.keys()), (self._get_keys + self._put_keys)))

    def _validate_key_set(self, keys, keyset):
        return all(key in keyset for key in keys)

    def _exist_key(self, key):
        return key in self._put_keys or key in self._get_keys

    def _add_value(self, key, value):
        if self._exist_key(key):
            self._table.update_item(
                Key=self._get_keys,
                UpdateExpression=('SET %s  = :val1' % (key)),
                ExpressionAttributeValues={
                    ':val1': value
                }
            )

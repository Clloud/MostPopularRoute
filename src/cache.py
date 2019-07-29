import hashlib
import sys
import os
import pickle

class Cache:
    out_path = (os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
         + '/out')

    @staticmethod
    def generate_key(data):
        """
        :param str data
        :return: str key
        """
        md5 = hashlib.md5()
        md5.update(data.encode(encoding='utf-8'))
        return md5.hexdigest()
        
    @classmethod
    def check(cls, key):
        """
        Check if the specific cache file exists.
        
        :param str key
        :return: boolean value
        """
        files = os.listdir(cls.out_path)
        if key + '.cache' in files:
            return True
        return False

    @classmethod
    def save(cls, key, value):
        """
        Save data to cache file.
        """
        with open(cls.out_path + '/' + key + '.cache', 'wb') as file:
            pickle.dump(value, file)
    
    @classmethod
    def get(cls, key):
        """
        Get data from cache file.

        :param str key
        """
        with open(cls.out_path + '/' + key + '.cache', 'rb') as file:
            value = pickle.load(file)
        return value

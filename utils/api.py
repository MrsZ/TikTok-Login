import threading
import requests
import binascii
import hashlib
import random
import base64
import uuid
import time
import json
import os

from pystyle import Col
from utils.ttencrypt import TTEncrypt
from utils.xlog import XLEncrypt
from utils.gorgon import Gorgon
from utils.solver import PuzzleSolver
from urllib.parse import urlencode


APP = {
    "version_code"  : 160904,
    "sig_hash"      : "aea615ab910015038f73c47e45d21466",
    "version"       : "16.9.4",
    "release_build" : "f05822b_20201014",
    "git_hash"      : "9f888696",
    "aid"           : 1340
}

START = time.time()

class Utils:
    @staticmethod
    def _xor(string):
        encrypted = [hex(ord(c) ^ 5)[2:] for c in string]
        return "".join(encrypted)

    @staticmethod
    def _sig(params: str, body: str = None, cookie: str = None):
        gorgon = Gorgon()
        return gorgon.calculate(params, cookie, body)
    
    @staticmethod
    def _factor(email: str) -> int:
        factor = 1
        if len(email) == 38: factor = 1
        if len(email) == 37: factor = 2
        if len(email) == 36: factor = 3
        if len(email) == 35: factor = 4
        if len(email) == 34: factor = 5
        if len(email) == 33: factor = 6
        if len(email) == 32: factor = 7
        if len(email) == 31: factor = 8
        if len(email) == 30: factor = 9
        if len(email) == 29: factor = 10
        if len(email) == 28: factor = 11
        if len(email) == 27: factor = 12
        if len(email) == 26: factor = 13
        if len(email) == 25: factor = 14
        if len(email) == 24: factor = 15
        if len(email) == 23: factor = 16
        if len(email) == 22: factor = 17
        if len(email) == 21: factor = 18
        if len(email) == 20: factor = 19
        if len(email) == 19: factor = 20
        if len(email) == 18: factor = 21
        if len(email) == 17: factor = 22
        if len(email) == 16: factor = 23
        if len(email) == 15: factor = 24
        if len(email) == 14: factor = 25
        if len(email) == 13: factor = 26
        if len(email) == 12: factor = 27
        if len(email) == 11: factor = 28
        if len(email) == 10: factor = 29
        if len(email) == 9: factor = 30
        if len(email) == 8: factor = 31
        
        return factor
    
    @staticmethod
    def _ttencrypt(body: dict) -> str:
        ttencrypt = TTEncrypt()
        data_formated = json.dumps(body).replace(" ", "")
        return ttencrypt.encrypt(data_formated)
    
    @staticmethod
    def _xlencrypt(body: str) -> str:
        return XLEncrypt().encrypt(body)
    
    @staticmethod
    def _fch(xlog: str):
        xlog = xlog[0:len(xlog) - 21]
        fch_str = binascii.crc32(xlog.encode("utf-8"))
        fch_str = str(fch_str)

        for i in range(len(fch_str), 10):
            fch_str = '0' + fch_str

        return fch_str
    
    @staticmethod
    def sprint(x: str, num: int, msg: str) -> None:
        return '    %s{%s%s%s}%s %s %s[%s%s%s]%s' % (
            Col.purple, Col.reset,
            x, 
            Col.purple, Col.reset,
            num,
            Col.blue, Col.reset,
            msg,
            Col.blue, Col.reset
        )

class Device:
    @staticmethod
    def __openudid() -> str:
        return binascii.hexlify(random.randbytes(8)).decode()
    
    @staticmethod
    def __uuid() -> str:
        return str(uuid.uuid4())
    
    @staticmethod
    def __install_time() -> int:
        return int(round(time.time() * 1000)) - random.randint(13999, 15555)
    
    @staticmethod
    def __ut() -> str:

        return random.randint(100, 500)
    
    @staticmethod
    def __uid() -> int:
        return random.randrange(10000, 10550, 50)

    @staticmethod
    def __ts() -> int:
        return round(random.uniform(1.2, 1.6) * 100000000) * -1

    @staticmethod
    def __cba() -> str:
        return f"0x{random.randbytes(4).hex()}"
    
    @staticmethod
    def __hc() -> str:
        return f"0016777{random.randint(260, 500)}"
    
    @staticmethod
    def __dp() -> str:
        return f"{random.randint(700000000, 900000000)},0,0"
    
    @staticmethod
    def __rom() -> int:
        return str(random.randint(700000000, 799999999))
    
    @staticmethod
    def gen_device() -> dict:
        # removed from preview
        pass
    

class Applog:
    def __init__(self, device: dict or None = None, proxy: str or None = None) -> tuple:
        self.__device = Device.gen_device() if device is None else device
        self.__host   = "log-va.tiktokv.com"
        self.proxies = {'http': f'http://{proxy}', 'http': f'http://{proxy}'} if proxy else None

    def __get_headers(self, params: str, payload: bytes):
        # removed from preview
        pass
    

    def __get_params(self):
        # removed from preview
        pass
    
    
    def __get_payload(self):
        # removed from preview
        pass
    
        
    def register_device(self):
        # removed from preview
        pass
    

class Xlog:
    def __init__(self, proxy: str or None = None):
        self.__device = Applog(proxy = proxy).register_device()
        self.proxies = {'http': f'http://{proxy}', 'http': f'http://{proxy}'} if proxy else None
    
    def _base_payload():
        # removed from preview
        pass
    
    def __get_headers(self, params: str, data: (str or None) = None) -> dict:
        # removed from preview
        pass
    
    def __get_params(self) -> str:
        # removed from preview
        pass
    
    def __get_xlog(self) -> requests.Response:
        # removed from preview
        pass
    
    def __alert_check(self) -> bool:
        # removed from preview
        pass
    
    def __xlog_install(self) -> dict:
        # removed from preview
        pass
    
    def __xlog_coldstart(self, num: int = 1) -> dict:
        # removed from preview
        pass

    def validate_device(self) -> bool:
        # removed from preview
        pass

class Captcha:
    # removed from preview
    pass
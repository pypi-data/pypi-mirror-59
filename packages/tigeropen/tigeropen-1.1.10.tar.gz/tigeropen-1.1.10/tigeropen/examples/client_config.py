# -*- coding: utf-8 -*-
"""
Created on 2018/10/31

@author: gaoan
"""
from tigeropen.common.consts import Language
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key


def get_client_config():
    """
    https://www.itiger.com/openapi/info 开发者信息获取
    :return:
    """
    is_sandbox = False
    client_config = TigerOpenClientConfig(sandbox_debug=is_sandbox)
    client_config.private_key = read_private_key('your private key file path')
    client_config.tiger_id = 'your tiger id'
    client_config.account = 'your account'  # 环球账户
    client_config.standard_account = None  # 标准账户
    client_config.paper_account = None  # 模拟账户
    client_config.language = Language.en_US
    return client_config

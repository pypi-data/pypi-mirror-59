# coding: utf-8
#  连接
import datetime
import threading

from dophon_logger import *

from dophon_db import properties
from dophon_db.mysql import Connection

logger = get_logger(eval(properties.log_types))

"""
连接池
author:CallMeE
date:2018-06-01
"""

logger.inject_logger(globals())

single_pool = None  # 单例模式获取连接池
cluster_pool = None  # 单例模式获取连接池

pool_action_log = {}

lock = threading.Lock()  # 全局线程锁


def record_support(f):
    def inner_method(*args, **kwargs):
        result = f(*args, **kwargs)
        obj_id = id(result)
        pool_action_log[obj_id] = datetime.datetime.now().timestamp()
        return result

    return inner_method


def record_return(f):
    def inner_method(*args, **kwargs):
        obj_id = id(args[1])
        if hasattr(properties, 'db_pool_exe_time') and getattr(properties, 'db_pool_exe_time'):
            logger.debug(
                '用时:' + (datetime.datetime.now().timestamp() - pool_action_log[obj_id]) + '毫秒'
            )
        f(*args, **kwargs)

    return inner_method


def get_pool(conn_kwargs: dict = {}):
    return get_single_pool(conn_kwargs)


def get_single_pool(conn_kwargs: dict = {}):
    global single_pool
    if single_pool:
        return single_pool
    pool = Pool()
    pool.init_pool(properties.pool_conn_num, Connection.Connection, conn_kwargs=conn_kwargs)
    single_pool = pool
    return single_pool


class Pool():
    _size = 0
    cache_conn_kwargs = {}

    # 初始化连接池
    def init_pool(self, num: int, Conn: Connection, conn_kwargs: dict = {}):
        _pool = []
        self._Conn = Conn
        self.cache_conn_kwargs = conn_kwargs
        for item_c in range(num):
            # 遍历定义连接放入连接池
            conn = Conn(**conn_kwargs)
            _pool.append(conn)
        self._pool = _pool
        self._size = num
        return self

    def __init__(self):
        logger.debug(f'初始化连接池 => ({id(self)})')

    # 定义取出连接
    @record_support
    def get_conn(self) -> Connection:
        __pool = self._pool
        if __pool:
            lock.acquire(blocking=True)
            currConn = __pool.pop(0)
            if currConn.test_conn():
                # 连接有效
                # 不作处理
                pass
            else:
                logger.error('连接无效')
                currConn.re_conn()
            lock.release()
            return currConn
        else:
            # 连接数不足则新增连接
            conn = Connection.Connection(**self.cache_conn_kwargs)
            self._pool.append(conn)
            return self.get_conn()

    # 定义归还连接
    @record_return
    def close_conn(self, conn):
        self._pool.append(conn)

    # 定义查询连接池连接数
    def size(self):
        return self._size

    # 定义释放所有连接
    def free_pool(self):
        for conn in self._pool:
            conn.getConnect().close()

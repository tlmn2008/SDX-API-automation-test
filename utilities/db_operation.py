# -*- coding: utf-8 -*-
import pymongo
import sshtunnel

from configurations import config


def query_from_mongodb(db_name, collection_name, query_conditions, columns, conn_info=config.mongo_conn_info):
    """
    在mongodb中查询数据
    :param db_name:
    :param collection_name:
    :param query_conditions:
    :param columns: 指定返回的列。（未生效，待调试）
    :param conn_info:
    :return:
    """
    with sshtunnel.open_tunnel(
            ssh_address_or_host=(config.base_ip, 22),
            ssh_password=config.ssh_root_password,
            ssh_username='root',
            remote_bind_address=(conn_info['host'], conn_info['port']),
            local_bind_address=('0.0.0.0', conn_info['port'])
    ) as tunnel:
        client = pymongo.MongoClient(port=conn_info['port'], username=conn_info['username'],
                                     password=conn_info['passwd'])
        db = client[db_name]
        collection = db[collection_name]
        res = []
        for i in collection.find(query_conditions, columns):
            # res.append(list(i.values()))
            res.append(i)
        # print(res)
        return res


def delete_from_mongodb(db_name, collections_and_conditions, conn_info=config.mongo_conn_info):
    with sshtunnel.open_tunnel(
            ssh_address_or_host=(config.base_ip, 22),
            ssh_password=config.ssh_root_password,
            ssh_username='root',
            remote_bind_address=(conn_info['host'], conn_info['port']),
            local_bind_address=('0.0.0.0', conn_info['port'])
    ) as tunnel:
        client = pymongo.MongoClient(port=conn_info['port'], username=conn_info['username'],
                                     password=conn_info['passwd'])
        db = client[db_name]
        for pair in collections_and_conditions:
            if not isinstance(pair, dict):
                return False
            for collection_name, condition in pair.items():
                collection = db[collection_name]
                res = collection.delete_many(condition)
                print('delete count: {}'.format(res.deleted_count))


def insert_to_mongodb(db_name, collections_and_conditions, conn_info=config.mongo_conn_info):
    with sshtunnel.open_tunnel(
            ssh_address_or_host=(config.base_ip, 22),
            ssh_password=config.ssh_root_password,
            ssh_username='root',
            remote_bind_address=(conn_info['host'], conn_info['port']),
            local_bind_address=('0.0.0.0', conn_info['port'])
    ) as tunnel:
        client = pymongo.MongoClient(port=conn_info['port'], username=conn_info['username'],
                                     password=conn_info['passwd'])
        db = client[db_name]
        for collection_name, insert_condition in collections_and_conditions.items():
            collection = db[collection_name]
            collection.insert_one(insert_condition)



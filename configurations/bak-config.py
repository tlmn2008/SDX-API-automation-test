# -*- coding: utf-8 -*-
import os

############# common #################
# base_ip = "10.150.13.134"
base_ip = "192.168.50.223"
base_port = "80"
protocol = "http"
base_url = "{}://{}:{}/".format(protocol, base_ip, base_port)

ssh_root_user = "root"
ssh_root_password = ")P:?9ol.8ik,"
ssh_port = 22

############# MongoDB #################
mongo_conn_info = {
    'host': '198.168.99.164',
    'port': 27017,
    'username': 'admin',
    'passwd': 'skydata@1229'

}

############# Cephfs #################
ssh_conn_info = {
    'host': base_ip,
    'port': ssh_port,
    'user': ssh_root_user,
    'passwd': ssh_root_password
}

############ user manager #################
user_name = "tengliang"
user_passwd = "abcd1234"

############ image manager #################
jupyter_image_name = "jupyter-notebook-lab_py3.6_cpu"

############ project manager #################


############ file manager #################
# file_url = "\\\\iluvatar.local\\public\\test\\skydiscovery\\sdx base\\skyflow\\"
current_dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
print(current_dir)
file_dir = "test_files"
file_url = "{}/{}/".format(current_dir, file_dir)
file_name = "iris.csv"
ceph_path = '/'  # 文件上传的ceph目录相对地址

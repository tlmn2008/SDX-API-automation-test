# -*- coding: utf-8 -*-
import os

############# common #################
# base_ip = "10.115.1.130"
base_ip = "192.168.50.223"
base_port = "80"
protocol = "http"
base_url = "{}://{}:{}/".format(protocol, base_ip, base_port)

ssh_root_user = "root"
# ssh_root_password = ")P:?9ol.8ik,"
ssh_root_password = "SkyAXE@0920"
ssh_port = 22

############# MongoDB #################
mongo_conn_info = {
    'host': '10.96.0.24',
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
user_name_a = "autotestuserA"
user_passwd_a = "123456"
user_name_b = "autotestuserB"
user_passwd_b = "123456"
user_sysadmin = "sysadmin"
user_passwd_sysadmin = "skydata@1229"
user_name_tmp = "tmpUserA"
user_full_name_tmp = "临时用户A"
user_passwd_tmp = "tmp_user@iluvatar.ai"

user_role_name = "user_role"
admin_role_name = "admin_role"

############ image manager #################
jupyter_image_name = "jupyter-notebook-lab_tensorflow1.14.0_py3.6_cpu"
container_dev_tf114_py36_cpu_image = "container_dev_tensorflow1.14.0_py3.6_cpu"

############ project manager #################
collaborative_user = 'sysadmin' # 协作用户
collaborative_userpwd = 'skydata@1229' # 协作用户密码

############ model manager #################
tf_model_location = "/sdx base/ModelTestSDX/tensorflow_test/mpg/mpg_model"
spark_model_location = '/sdx base/ModelTestSDX/spark_test/test_resource/sparkModel'
tf_model_service_image_name_only_cpu = 'tensorflow_deployment'

############ file manager #################
# file_url = "\\\\iluvatar.local\\public\\test\\skydiscovery\\sdx base\\skyflow\\"
current_dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
file_dir = "test_files"
file_url = "{}/{}/".format(current_dir, file_dir)
file_name = "iris.csv"
# iris_folder文件结构：
# iris_folder
#   iris0(iris0_1.csv+iris0_2.csv+iris0_3.csv)
#   iris1(iris1.csv)
#   iris2(iris2_1.csv+iris2_2.csv)
#   iris3.csv
#   iris4.csv
#   iris5.csv
folder_name = "iris_folder"
# iris_zip.zip文件结构：
# iris /
#    iris1 (iris1.csv)
#    iris2 (iris2.csv + iris3.csv)
zip_file_name = "iris_zip.zip"
ceph_path = '/'  # 文件上传的ceph目录相对地址

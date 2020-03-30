### 基于pytest + requests + allure + (locust)

### 文件结构：
>├── configurations  
>│   ├── config.py  
>│   └── __init__.py  
>├── conftest.py  
>├── utilities  
>│   ├── __init__.py  
>│   ├── logger.py  
>├── logs  
>├── README.md  
>├── send_check  
>│   ├── apis  
>│   │   ├── api_image_m.py  
>│   │   ├── api_project_m.py  
>│   │   ├── ....   
>│   │   └──__init__.py  
>│   ├── __init__.py  
>│   ├── req_send  
>│   │   ├── __init__.py  
>│   │   ├── send_project_m_req.py  
>│   │   ├── send_req.py  
>│   │   └── ....  
>│   └── resp_check  
>│       ├── check_common.py  
>│       ├── check_image_m.py  
>│       ├── ....  
>│       └── __init__.py  
>└── test_cases  
>│    ├── base.py  
>│    ├── __init__.py  
>│    ├── project_manager  
>│    │   ├── __init__.py  
>│    │   └── test_project_creation.py  
>│    │── users_manager  
>│    │   ├── __init__.py  
>│    │   └── test_user_creation.py  
>│    └── .....  

- configurations: 测试所需的数据，如目标机器地址，测试镜像名称等
- utilities：工具类和方法
- send_check：
    1. apis：定义请求。返回各接口请求的模板供用例使用
    2. req_send：发送请求，将单个或多个请求的发送与检查封装后供用例调用。将功能请求模块化成方法，如登录、查询image的uuid、创建项目、创建任务、启动任务等方法，并调用resp_check自动检查。
           当有多个用例都会调用上述方法，可将这些方法再组合入新方法，目的是减少用例中代码、逻辑清晰，并使维护成本降低。
    3. resp_check：检查结果。
- test_cases：用例文件
- logs: 每个测试class生成一个日志，一般一个测试文件只有一个class

#### 测试用例实例：
```
class TestCreateProject(base.Base):
    @classmethod
    def setup_class(cls):
        super(TestCreateProject, cls).setup_class(logger_name='project_creation')
        cls.token = send_user_m_req.get_token_simple()
             
    def setup(self):
        self.clean_data()
    
    def teardown(self):
        pass
           
    def test_case1_create_new_task_and_start(self):
    # case1: 使用创建项目，并使用指定镜像启动任务
    # 获取image的uuid
    image_id = send_image_m_req.get_image_uuid_by_image_name(self.token, config.jupyter_image_name)
    # 创建项目
    project_id = send_project_m_req.create_new_project(self.token, project_name='auto test project 4 task')
    # 创建任务
    task_uuid = send_project_m_req.create_new_task(self.token, task_name='automation task', project_id=project_id,
                                                   task_type='JUPYTER', image_id=image_id, resource_config=None)
    # 启动任务
    started_task_uuid = send_project_m_req.start_task(self.token, task_uuid)
    assert False if task_uuid != started_task_uuid else True
    
    def test_case2_xxx_(self):
    # case2：xxx xxx
        pass
```

#### 说明：
- 测试类中以test_开始的方法为测试用例
- setup_class: 每个测试类执行前执行一次，负责环境和业务初始化，如清理环境，用户登录操作
- setup: 每个用例执行前执行一次
- teardown: 每个用例执行后执行一次
- teardown_class：每个测试类执行后执行一次


#### coding风格：
- JIRA用例号加在测试用例名称中，如test_SKTE_T2495_create_new_project， SKTE-T2495是JIRA用例号，中横线需变成下划线
- 日志用英文，注释用中文。
- 日志每句的首字母大写。
- 测试中创建的任何资源的命名应以小写"autotest_"打头，方便按条件查找清理环境






























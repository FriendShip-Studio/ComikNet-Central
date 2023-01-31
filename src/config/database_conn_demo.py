
# 这是一个配置样例，妥善填写后将其重命名为 database_conn.py

TORTOISE_ORM_CONFIG = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': '',  # 数据库地址
                'port': '',     # 数据库端口
                'user': '',    # 数据库用户名
                'password': '',   # 数据库密码
                'database': '',  # 数据库名
            }
        },
    },
    'apps': {
        'models': {
            'models': ['src.models.database'],
            'default_connection': 'default',
        }
    }
}

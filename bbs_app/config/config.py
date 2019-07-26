import platform
secret_key = 'bbs'
if platform.system() == 'Windows':
    pass
    # database_uri = 'postgresql://postgres:root@127.0.0.1:5432/bbsdb'
    database_uri = 'sqlite:///c:/sqlite temp/bbs.sqlite'
elif platform.system() == 'Linux':
    # database_uri = 'postgresql://postgres:root@bbsdb:5432/postgres'
    database_uri = 'postgresql://postgres:123456@bbsdb:5432/postgres'

    # bbsdb为db容器别名,

    # 使用MySQL数据库
    # database_uri = 'mysql://root:mysql123@bbsdb:3306/mysqldb'

# 格式
# MySQL mysql://username:password@hostname/database
# Postgres postgresql://username:password@hostname/database
# SQLite（Unix） sqlite:////absolute/path/to/database
# SQLite（Windows） sqlite:///c:/absolute/path/to/database
import platform
secret_key = 'bbs'
if platform.system() == 'Windows':
    database_uri = 'postgresql://postgres:root@127.0.0.1:5432/bbsdb'
elif platform.system() == 'Linux':
    # database_uri = 'postgresql://postgres:root@bbsdb:5432/postgres'
    database_uri = 'postgresql://postgres:postgres@bbsdb:5432/postgres'

    # bbsdb为db容器别名,

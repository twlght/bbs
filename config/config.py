import platform
secret_key = 'bbs'
users_img_directory = 'users_img'
allowed_suffix = ['jpg', 'jpeg', 'png', 'gif']
topics_per_page = 40
if platform.system() == 'Windows':
    database_uri = 'postgresql://postgres:root@127.0.0.1:5432/bbsdb'
elif platform.system() == 'Linux':
    database_uri = 'postgresql://postgres:postgres@127.0.0.1:5432/bbsdb'

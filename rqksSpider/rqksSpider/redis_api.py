from redis import StrictRedis, ConnectionPool, Redis
pool = ConnectionPool(host='cloud.renqiukai.com',
                      port=6379, db=0, password='123456')
r_conn = Redis(connection_pool=pool)

from gevent import monkey; monkey.patch_socket()
import gevent
# import redis
import time
import uuid

from rediscluster import StrictRedisCluster

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "xxx-test-redis.wpcvfz.clustercfg.usw1.cache.amazonaws.com", "port": 6379}]

import multiprocessing
import time

def fetch(redis_inst, count):
    start = time.time()
    for i in xrange(0,count):
        redis_inst.set(str(uuid.uuid4()),"rp=auto,ty=Canon MX450 series,note=,pdl=application/octet-stream,qtotal=1,txtvers=1,priority=60,product=(Canon MX450 series),adminurl=http://B13123000000.local.,usb_MFG=Canon,usb_MDL=MX450 series,usb_CMD=,UUID=00000000-0000-1000-8000-180CACB13123,Color=T,Duplex=F,Scan=T,Fax=F,mac=18:0C:AC:B1:31:23")

    end = time.time()
    print("gevent spend %s seconds to set %s keys, speed is %s" % (end-start, count, count*1.0/(end-start)))


def TestProcess(test_count, thread_count):
    #pool = redis.ConnectionPool(host="xxx-test-redis.wpcvfz.clustercfg.usw1.cache.amazonaws.com", port=6379, db=0)
    ## pool = redis.ConnectionPool(host="10.206.131.20", port=6379, db=0)
    #redis_inst = redis.StrictRedis(connection_pool=pool)
    redis_inst = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True, max_connections=2000)
    start = time.time()
    threads = []
    for i in range(0,thread_count):
        threads.append(gevent.spawn(fetch, redis_inst, test_count))

    for thread in threads:
        thread.join()

    end = time.time()
    print("Porcess spend %s seconds, speed is %s" % (end-start, thread_count*test_count*1.0/(end-start)))


        
        
if __name__ == '__main__':
    start = time.time()
    processes = []
    test_process_count = 1 # 3
    test_thread_count = 60 # 8
    test_count = 10000
    for i in range(0, test_process_count):
        p = multiprocessing.Process(target = TestProcess, args = (test_count,test_thread_count))
        processes.append(p)

    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
    
    end = time.time()
    print("Total spend %s seconds, speed is %s" % (end-start, test_process_count*test_thread_count*test_count*1.0/(end-start)))

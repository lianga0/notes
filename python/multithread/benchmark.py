#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import signal
import logging
import argparse
import threading
from common import *
from multiprocessing import Pool, TimeoutError
from concurrent.futures import ThreadPoolExecutor

logging.getLogger().setLevel(logging.INFO)
ThreadLock = threading.Lock()

TYPE_CRC = "crc"
TYPE_MD5 = "md5"
TYPE_CRC_MD5 = "crc&md5"
FILTER_HASH_TYPE = TYPE_CRC

SuccessCount = 0
FailCount = 0
SkipCount = 0
ErrorCount = 0
MaxSendRequestCount = sys.maxsize
ThreadNumber = 10
ThreadLocal = threading.local()


class NoMoreRecordException(Exception):
    pass


class NoNeedHandleRecordException(Exception):
    pass


def handle_ps_line(line: bytes, session: requests.Session = None) -> bool:
    global MaxSendRequestCount
    ps = json.loads(line)
    if not isinstance(ps, dict):
        raise NoNeedHandleRecordException()
    if FILTER_HASH_TYPE == TYPE_CRC:
        if "signature" in ps and "result" in ps and "common_filter_crc" in ps["signature"] and \
                "full_crc" in ps["signature"] and "size" in ps["signature"] and ps["signature"]["common_filter_crc"] \
                and ps["signature"]["full_crc"]:
            with ThreadLock:
                MaxSendRequestCount -= 1
                cur_remain_count = MaxSendRequestCount
            if cur_remain_count < 0:
                raise NoMoreRecordException()
            virus = query_crc_only(ps["signature"]["common_filter_crc"], ps["signature"]["full_crc"],
                                   ps["signature"]["size"], session)
            if virus != ps["result"]:
                logging.info(
                    f'common_crc: {ps["signature"]["common_filter_crc"]}, full_crc: {ps["signature"]["full_crc"]}, size: {ps["signature"]["size"]}, result: {ps["result"]}, ",server: {virus}')
                return False
            else:
                return True
            pass
        else:
            raise NoNeedHandleRecordException()
        pass
    pass


def handler_line(line: bytes):
    global ErrorCount
    global SuccessCount
    global FailCount
    global SkipCount
    if hasattr(ThreadLocal, 'session'):
        http_session = ThreadLocal.session
    else:
        http_session = requests.Session()
        ThreadLocal.session = http_session
    pass
    try:
        match = handle_ps_line(line, http_session)
        if match:
            with ThreadLock:
                SuccessCount += 1
            pass
        else:
            with ThreadLock:
                FailCount += 1
            pass
    except AssertionError:
        with ThreadLock:
            ErrorCount += 1
        pass
    except NoNeedHandleRecordException:
        with ThreadLock:
            SkipCount += 1
        pass
    except NoMoreRecordException:
        pass
    except requests.ConnectionError:
        with ThreadLock:
            ErrorCount += 1
        pass
    except Exception as ee:
        import traceback
        traceback.print_exc()
        logging.debug("unknown exception ", ee)
        pass
    time.sleep(0)


def handler(filename: str, begin_offset: int, end_offset: int, max_http_request_count: int,
            thread_num: int, filter_type: str):
    global ErrorCount
    global SuccessCount
    global FailCount
    global SkipCount
    global MaxSendRequestCount
    global ThreadNumber
    global FILTER_HASH_TYPE
    MaxSendRequestCount = max_http_request_count
    ThreadNumber = thread_num
    FILTER_HASH_TYPE = filter_type
    pool = ThreadPoolExecutor(max_workers=thread_num)
    semaphore = threading.BoundedSemaphore(thread_num)
    file = open(filename, 'rb')
    if begin_offset > 0:
        file.seek(begin_offset - 1, os.SEEK_SET)
        line = file.read(1)
        if line != b"\n":  # 分到的逻辑块不是一行开头，跳过这个半行
            file.readline()
        pass
    pass
    start_time = time.time_ns()
    while file.tell() < end_offset:
        line = file.readline()
        if not line:  # 防止设置错文件结尾长度，或文件读取中文件长度被修改
            break
        semaphore.acquire()
        future = pool.submit(handler_line, line)
        future.add_done_callback(lambda _: semaphore.release())
        with ThreadLock:
            if MaxSendRequestCount < 0:
                break
            pass
        pass
    pool.shutdown(wait=True, cancel_futures=False)

    end_time = (time.time_ns() - start_time) / 1000. / 1000. / 1000.
    print("process id: ", os.getpid(), ", SuccessCount: ", SuccessCount, ", SuccessRate: ", SuccessCount / end_time,
          ", ProcessRate: ", (SuccessCount + FailCount) / end_time,
          ", FailCount: ", FailCount, ", SkipCount: ", SkipCount, ", ErrorCount: ", ErrorCount, sep="")


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="ps.json")
    parser.add_argument("-p", "--process", default=3, type=int, help="running process count")
    parser.add_argument("-n", "--number", default=ThreadNumber, type=int, help="each process running thread count")
    parser.add_argument("-m", "--max", default=100, type=int, help="each process max send http request count")
    parser.add_argument("-t", "--type", default="md5", choices=(TYPE_CRC, TYPE_MD5, TYPE_CRC_MD5))
    args = parser.parse_args()
    process_number = int(args.process)
    thread_number = int(args.number)
    max_request_count = int(args.max)
    filter_hash_type = args.type
    file_name = args.file
    file_size = os.path.getsize(file_name)
    print("process file: ", file_name, ", size is : ", file_size, sep="")
    assert process_number > 0
    each_process_block_size = file_size // process_number
    assert each_process_block_size > 0
    eachProcessArgs = [[file_name, i * each_process_block_size, (i + 1) * each_process_block_size, max_request_count,
                        thread_number, filter_hash_type] for i in range(process_number)]
    eachProcessArgs[-1][2] = file_size  # 修正一下最后一个进程结束文件位置，因为除法为整除
    with Pool(process_number, init_worker) as p:
        r = p.starmap_async(handler, eachProcessArgs)
        while True:
            try:
                allProcessResult = r.get(2)
                if len(allProcessResult) == process_number:
                    p.close()
                    print("process id: ", os.getpid(), " all task is finish", sep="")
                    break
            except KeyboardInterrupt:
                print("Caught KeyboardInterrupt, terminating workers")
                p.terminate()
                break
            except TimeoutError:
                # print(".", end="", flush=True)
                pass
            except Exception as e:
                print("process id: ", os.getpid(), "incurs exception: ", e, type(e))
            pass
        pass

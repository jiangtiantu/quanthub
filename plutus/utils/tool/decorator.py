import time
import tracemalloc
from functools import wraps

import dill
from apscheduler.schedulers.background import BlockingScheduler

from plutus.utils.tool.logger import log_record

dill.settings["recurse"] = True


def trace_memory(func, logfile: str = __file__):
    """
    To track memory usage during decorated function.
    :param func:
    :param logfile:
    :return:
    """

    @wraps(func)
    def tracing(*args, **kwargs):
        logger = log_record(logfile, "memory")
        tracemalloc.start()
        current_, peak_ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        logger.info(
            f"Before function memory usage {current_ / 1e6}MB; Peak: {peak_ / 1e6}MB"
        )
        tracemalloc.start()
        res = func(*args, **kwargs)
        current_, peak_ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        logger.info(
            f"After function memory usage {current_ / 1e6}MB; Peak: {peak_ / 1e6}MB"
        )
        return res

    return tracing


def sched_job(scheduler: BlockingScheduler, logger: log_record = None, **sched_kwargs):
    """
    将程序添加到任务计划
    :param scheduler:
    :param logger:
    :param sched_kwargs:
    :return:
    """

    def func_wrapper(func):
        if logger is not None:
            logger.info(
                f"Register cron job for {func.__name__} with params: {sched_kwargs}"
            )

        @wraps(func)
        def __function(*args, **kwargs):
            scheduler.add_job(func, **sched_kwargs, args=args, kwargs=kwargs)

        return __function

    return func_wrapper


def run_once(func):
    """
    只运行一次的装饰器
    :param func:
    :return:
    """

    def wrapper(*args, **kw):
        if not wrapper.has_run:
            func(*args, **kw)
            wrapper.has_run = True

    wrapper.has_run = False
    return wrapper


def cal_run_time(func):
    """
    计算程序运行时间,并记录日志
    :param func:
    :return:
    """

    def wrapper(*args, **kw):
        start_time = time.time()
        func(*args, **kw)
        end_time = time.time()
        log_record(__file__, "run_time").info(
            f"current Function [{func.__name__}] run time is [{end_time - start_time}] s "
        )

    return wrapper

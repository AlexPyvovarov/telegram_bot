import logging


def async_log_function_call(func):
   """Декоратор для логування викликів асинхронних функцій"""


   async def wrapper(*args, **kwargs):


       logger = logging.getLogger(__name__)
       msg = f"Відбувся виклик функції '{func.__name__}'"
       logger.info(msg=msg)
       return await func(*args, **kwargs)


   return wrapper
# import logging

# class InitializeCustomLogger:
#     def __init__(self, classname, level=None):
#         if not level:
#             level = logging.INFO
#         self.logger = logging.getLogger(classname)
#         self.logger.setLevel(level)
#         # create console handler and set level
#         ch = logging.StreamHandler()
#         ch.setLevel(level)
#         # create formatter
#         formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         # add formatter to ch
#         ch.setFormatter(formatter)
#         # add ch to logger
#         self.logger.addHandler(ch)
#
#     def debug(self, message=None):
#         if message:
#             return self.logger.debug(message)
#
#     def info(self, message=None):
#         if message:
#             return self.logger.info(message)
#
#     def warning(self, message=None):
#         if message:
#             return self.logger.warning(message)
#
#     def error(self, message=None):
#         if message:
#             return self.logger.error(message)
#
#     def critical(self, message=None):
#         if message:
#             return self.logger.critical(message)

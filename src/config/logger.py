from config.loggerManager.log_handler import LogHandler

log_handler = LogHandler()

log_handler.configure_level(file="TRACE", cmd="TRACE")
log_handler.configure_file(path=".log", rotation="5 MB")
log_handler.configure_log_display(colorize=True)

log = log_handler.get_logger()

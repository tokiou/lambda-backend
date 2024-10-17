import colorlog
import logging
from logging.handlers import RotatingFileHandler


# Configuración del handler de color
handler = colorlog.StreamHandler()
# Define la ruta completa del archivo de log
log_file_path = "logs/lambda.log"


# Configuración del handler de archivo con rotación
file_handler = RotatingFileHandler(log_file_path, maxBytes=10**6,
                                   backupCount=5)
file_handler.setFormatter(logging.Formatter(
   '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   datefmt='%Y-%m-%d %H:%M:%S'
))


handler.setFormatter(colorlog.ColoredFormatter(
   '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   datefmt='%Y-%m-%d %H:%M:%S',
   log_colors={
       'DEBUG': 'cyan',
       'INFO': 'green',
       'WARNING': 'yellow',
       'ERROR': 'red',
       'CRITICAL': 'bold_red',
   }
))
# Configuración del logger
logger = logging.getLogger('lambda-logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(file_handler)

import os


LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'fmt': '%(asctime)s %(levelname)s %(module)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'maxBytes': 1024 * 1024,
            'backupCount': 3,
            'filename': os.path.abspath('rotation.log'),
            'encoding': 'utf-8'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
}

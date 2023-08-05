"""
The Adversarial Robustness Toolbox (ART).
"""
import logging
import logging.config

# Project Imports
from art import attacks
from art import classifiers
from art import defences
from art import metrics
from art import poison_detection
from art import wrappers

# Semantic Version
__version__ = "1.1.0"

# pylint: disable=C0103

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'std': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M'
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.NullHandler',
        },
        'test': {
            'class': 'logging.StreamHandler',
            'formatter': 'std',
            'level': logging.INFO
        }
    },
    'loggers': {
        'art': {
            'handlers': ['default']
        },
        'tests': {
            'handlers': ['test'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

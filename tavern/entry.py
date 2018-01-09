import logging

from tavern.config import get_config
from tavern.core import run


def main():
    vargs = get_config()

    if vargs.pop("debug"):
        log_level = "DEBUG"
    else:
        log_level = "INFO"

    # Basic logging config that will print out useful information
    log_cfg = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "{asctime:s} [{levelname:s}]: ({name:s}:{lineno:d}) {message:s}",
                "style": "{",
            },
        },
        "handlers": {
            "to_stdout": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "tavern": {
                "handlers": [
                ],
                "level": log_level,
            }
        }
    }

    log_loc = vargs.pop("log_to_file")

    if log_loc:
        log_cfg["handlers"].update({
            "to_file": {
                "class": "logging.FileHandler",
                "filename": log_loc,
                "formatter": "default",
            }
        })

        log_cfg["loggers"]["tavern"]["handlers"].append("to_file")

    if vargs.pop("stdout"):
        log_cfg["loggers"]["tavern"]["handlers"].append("to_stdout")

    logging.config.dictConfig(log_cfg)

    exit(not run(vargs['infile'], vargs['global_vars']))

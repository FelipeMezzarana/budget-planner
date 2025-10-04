# Third party
import structlog

# Local
from ..utils.constants import LOGGING_LEVEL


def get_logger(name: str, logging_level: int = LOGGING_LEVEL):
    """Return configured logger."""

    logger = structlog.get_logger(name)
    # the logger is only created "when it's needed". Enforce that:
    logger.new()
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(LOGGING_LEVEL),
    )
    logger = logger.bind(__name__=name)

    return logger

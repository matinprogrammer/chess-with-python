from utils.log import core_logger


class MoveStatus:
    def __init__(self):
        core_logger.info("MoveStatus initialised")

    def __str__(self):
        return str("move_status")
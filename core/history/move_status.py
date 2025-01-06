from utils.log import core_logger


class MoveStatus:
    # good move: !
    # perfect move: !!
    # bad move: ?
    # too bad: ??
    # interesting: ?!
    # suspicious: !?
    def __init__(self):
        core_logger.info("MoveStatus initialised")

    def __str__(self):
        return str("move_status")
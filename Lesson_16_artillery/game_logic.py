import shells
import tanks
from constants import *


class GameRound:
    def __init__(self, canvas, difficulty=1):
        assert difficulty < 10
        self.canvas = canvas

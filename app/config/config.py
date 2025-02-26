# -*- coding: utf-8 -*-
""" Configuration. """

import os
from dotenv import load_dotenv

load_dotenv()

GAMESTATE: str = os.getenv('DEFAULT_GAMESTATE', 'gamestate')
LOG_PARSE: str = os.getenv('DEFAULT_LOG_PARSE', 'gamestate_parsed')

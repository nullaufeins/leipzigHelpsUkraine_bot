#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from src.thirdparty.code import *;
from src.thirdparty.config import *;
from src.thirdparty.system import *;
from src.thirdparty.types import *;

from src.core.env import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'Secret',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES Secret
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclass
class SecretDefault():
    token: str = field(default='', repr=False);

class Secret(SecretDefault):
    def __init__(self, path: Optional[str] = None, fname: str = '.env'):
        '''
        Reads bot token from environment OR .env file.

        NOTE:
        - in docker containers: token loaded to environment and .env file does not exist
        - locally .env file should exist and token not loaded to environment.
        '''
        super().__init__();
        try:
            if 'TOKEN' in os.environ:
                self.token = os.environ['TOKEN'];
            else:
                load_dotenv(dotenv_path=path or os.getcwd());
                env = dotenv_values(fname);
                self.token = get_env_string(env, key='TOKEN');
        except:
            raise KeyError('TOKEN not loaded to environment!');
        return;

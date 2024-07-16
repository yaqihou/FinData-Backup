
from pathlib import Path

class DBConfig:

    DB_NAME: str = (Path.home() / 'Dropbox' / '66-DBs' / 'FinDB.db').absolute().as_posix()

    LOGGER_NAME = 'db-utils'


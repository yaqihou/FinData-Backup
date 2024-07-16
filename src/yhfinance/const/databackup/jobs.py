from dataclasses import dataclass
import datetime as dt
from typing import Optional
from enum import Enum

from .tasks import BaseTask, DownloadSwitch
from ..tickers import TickerType, Period, Interval, HistoryExtraOptions

@dataclass
class UserConfig:
    ticker_name: str
    ticker_type: TickerType
    # ticker_sect: ""

    tasks: list[BaseTask]
    notes: str = ""


class JobStatus(Enum):

    INIT = 0
    SUCCESS = 1
    SUCCESS_PULL = 2
    FAIL = 3


@dataclass(kw_only=True)
class JobSetup:

    # Basic setup - related with Ticker 
    ticker_name: str
    ticker_type: TickerType

    # Run setup - extra information
    run_datetime: dt.datetime 
    run_intraday_version: int
    task: BaseTask 
    download_switch: int = DownloadSwitch.ALL

    # History Arguments
    # NOTE - similar info in task field as well,
    #        but below are parsed from task to be used directly
    interval: Interval = Interval.DAY
    period: Optional[Period] = None
    start: Optional[dt.date | str | int] = None
    end: Optional[dt.date | str | int] = None
    history_extra_options: HistoryExtraOptions = HistoryExtraOptions()

    # Download setup
    download_full_text_news: bool = False

    @property
    def run_date(self) -> dt.date:
        return self.run_datetime.date()

    def __post_init__(self):
        # Only need to check if download history data
        if self.download_switch & DownloadSwitch.HISTORY:
            if self.period is None:
                assert self.end is not None and self.start is not None
            else:
                assert self.end is None and self.start is None
    
    def get_history_args(self) -> dict:

        args = {
            'interval': self.interval.value,
            **self.history_extra_options.to_dict()
        }

        if self.period is not None:
            args['period'] = self.period.value
        else:
            args['period'] = None
            args['start'] = self.start
            args['end'] = self.end

        return args

    @property
    def history_args(self) -> dict:
        return self.get_history_args()

    @property
    def history_range(self) -> str:
        if self.period is None:
            return f"{self.start} to {self.end}"
        else:
            return f"period of {self.period.value}"

    @property
    def metainfo(self) -> dict:
        ret = {
            'ticker_name'          : self.ticker_name,
            'ticker_type'          : self.ticker_type.value,
            'run_date'             : self.run_date,
            'run_datetime'         : self.run_datetime,
            'run_intraday_version' : self.run_intraday_version,
            'task_name'            : self.task.name
        }

        assert set(self.get_metainfo_cols()) == set(ret.keys())

        return ret

    @classmethod
    def get_metainfo_cols(cls) -> list[str]:
        return [
            'ticker_name',
            'ticker_type',
            'run_date',
            'run_datetime',
            'run_intraday_version',
            'task_name'
        ]
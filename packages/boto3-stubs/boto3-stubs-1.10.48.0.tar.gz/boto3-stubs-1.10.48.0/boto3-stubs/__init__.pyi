# pylint: disable=unused-argument,multiple-statements,unused-import
import logging
import sys
import importlib.util
from typing import Any, Optional, Union, overload

import boto3.session
from boto3.session import Session
from botocore.config import Config

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__author__: str
__version__: str

DEFAULT_SESSION: Optional[Session] = None

def setup_default_session(
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    aws_session_token: str = None,
    region_name: str = None,
    botocore_session: str = None,
    profile_name: str = None,
) -> Session: ...
def set_stream_logger(
    name: str = "boto3", level: int = logging.DEBUG, format_string: Optional[str] = None
) -> None: ...
def _get_default_session() -> Session: ...

class NullHandler(logging.Handler):
    def emit(self, record: Any) -> Any:
        pass

try:
    from mypy_boto3.boto3_init import *
except (ImportError, ModuleNotFoundError):
    pass

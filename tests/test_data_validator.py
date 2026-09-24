import sys
from pathlib import Path
import pandas as pd
import pytest

from src.etl_utils.data_validator import (
    validate_columns,
    find_duplicates
)


import os

import pandas as pd

from utils.load import store_to_csv


def test_store_to_csv():

    filename = "test_products.csv"

    df = pd.DataFrame(
        [
            {
                "Title": "Test Product"
            }
        ]
    )

    result = store_to_csv(
        df,
        filename
    )

    assert result is True

    assert os.path.exists(filename)

    os.remove(filename)


def test_store_to_csv_empty():

    df = pd.DataFrame()

    result = store_to_csv(
        df,
        "empty.csv"
    )

    assert result is False

from unittest.mock import patch
import pandas as pd

from utils.load import store_to_postgresql


@patch("utils.load.create_engine")
def test_store_postgresql(mock_engine):

    df = pd.DataFrame(
        [{"Title": "Test"}]
    )

    result = store_to_postgresql(
        df,
        "postgresql://dummy"
    )

    assert result is True
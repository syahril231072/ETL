import pandas as pd

from utils.transform import (
    transform_data,
    transform_to_dataframe
)


def test_transform_to_dataframe():

    data = [
        {
            "Title": "Hoodie"
        }
    ]

    df = transform_to_dataframe(data)

    assert isinstance(df, pd.DataFrame)

    assert len(df) == 1


def test_transform_data_valid():

    raw_data = [
        {
            "Title": "Hoodie",
            "Price": "$100.00",
            "Rating": "Rating: ⭐ 4.8 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = pd.DataFrame(raw_data)

    result = transform_data(df)

    assert not result.empty

    assert result["Price"].iloc[0] == 1600000.0

    assert result["Rating"].iloc[0] == 4.8

    assert result["Colors"].iloc[0] == 3

    assert result["Size"].iloc[0] == "M"

    assert result["Gender"].iloc[0] == "Men"


def test_transform_remove_invalid_data():

    raw_data = [
        {
            "Title": "Unknown Product",
            "Price": "$100.00",
            "Rating": "Invalid Rating",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01"
        }
    ]

    df = pd.DataFrame(raw_data)

    result = transform_data(df)

    assert len(result) == 0


def test_transform_empty_dataframe():

    df = pd.DataFrame()

    result = transform_data(df)

    assert isinstance(result, pd.DataFrame)
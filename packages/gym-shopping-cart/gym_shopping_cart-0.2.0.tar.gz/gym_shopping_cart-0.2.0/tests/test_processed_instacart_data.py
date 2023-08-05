from pathlib import Path
import time

import numpy as np
import pandas as pd
import pytest

from gym_shopping_cart.data.parser import InstacartData

this_dir = Path(__file__).resolve().parent


def test_product_string():
    data = InstacartData(
        gz_file=this_dir / ".." / "gym_shopping_cart" / "data" / "test_data.tar.gz"
    )
    res = data.product_str(34)
    assert isinstance(res, str)
    assert res == "Peanut Butter Cereal"
    with pytest.raises(ValueError):
        data.product_str(99999999999)


def test_parse_instacart_data():
    data = InstacartData(
        gz_file=this_dir / ".." / "gym_shopping_cart" / "data" / "test_data.tar.gz"
    )
    res, _ = data.orders_for_user()
    assert res is not None
    assert isinstance(res, pd.DataFrame)
    assert res.loc[33].shape[0] == data.n_observations()
    assert res.loc[33]["order_dow_3"] == 1
    assert res.loc[33]["order_hour_of_day_12"] == 1
    assert res.loc[1]["days_since_prior_order"] == 0  # NOT nan.
    assert res.loc[2].shape[0] == data.n_observations()
    assert res.loc[2]["order_dow_1"] == 1
    assert res.loc[2]["order_hour_of_day_13"] == 1
    np.testing.assert_almost_equal(
        res.loc[2]["days_since_prior_order"],
        6.0 / InstacartData.MAX_DAYS_SINCE_PRIOR,
        decimal=3,
    )


def test_get_raw_orders():
    data = InstacartData(
        gz_file=this_dir / ".." / "gym_shopping_cart" / "data" / "test_data.tar.gz"
    )
    res = data._raw_orders_for_user()
    assert res is not None
    assert isinstance(res, pd.DataFrame)


def test_chicken_in_right_place():
    chicken_id = 6046
    data = InstacartData(
        gz_file=this_dir / ".." / "gym_shopping_cart" / "data" / "test_data.tar.gz"
    )
    assert data.columns()[chicken_id] == "product_id_6046"
    assert data.product_str(chicken_id) == "Boneless Skinless Chicken Breast"


def test_caching():
    data = InstacartData(
        gz_file=this_dir / ".." / "gym_shopping_cart" / "data" / "test_data.tar.gz",
        cache_data=False,
    )
    start = time.process_time()
    [data._raw_orders_for_user() for i in range(10)]
    total_no_cache = time.process_time() - start

    data = InstacartData(
        gz_file=this_dir / ".." / "gym_shopping_cart" / "data" / "test_data.tar.gz",
        cache_data=True,
    )
    start = time.process_time()
    [data._raw_orders_for_user() for i in range(10)]
    total_cache = time.process_time() - start

    assert total_cache < total_no_cache / 2

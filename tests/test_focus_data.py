from src.harness_ccm_external_data import Focus, HARNESS_FIELDS

import pandas as pd
import numpy as np

SAMPLE_DATA = "focus_sample.csv"

# baseline
test_data = Focus("MyTestPlatform", SAMPLE_DATA)
test_data_length = 1000
test_data_col = 44

test_data.render()
test_data.render_file(f"harness_{SAMPLE_DATA}")


def test_data_load():
    raw_row, raw_col = test_data.billing_content.shape
    assert raw_row == test_data_length
    assert raw_col == test_data_col


def test_focus_data():
    focus_row, focus_col = test_data.harness_focus_content.shape
    assert focus_row == test_data_length
    assert focus_col == len(HARNESS_FIELDS)
    assert (
        test_data.harness_focus_content["EffectiveCost"].sum()
        == test_data.billing_content["EffectiveCost"].sum()
    )


def test_render_data(tmpdir):
    filename = tmpdir.join("output.csv")

    test_data.render_file(filename)
    result_content = pd.read_csv(filename, dtype=str)
    result_row, result_col = result_content.shape

    assert result_row == test_data_length
    assert result_col == len(HARNESS_FIELDS)


# skipping rows
def test_data_load_skip_lines():
    to_skip_lines = 100
    test_data_skip_lines = Focus("MyTestPlatform", SAMPLE_DATA, skip_rows=to_skip_lines)

    raw_row, raw_col = test_data_skip_lines.billing_content.shape
    assert raw_row == test_data_length - to_skip_lines
    assert raw_col == test_data_col


def test_data_load_skip_specific_lines():
    to_skip_specific = [1, 3, 5, 7, 9]
    test_data_skip_specific = Focus(
        "MyTestPlatform", SAMPLE_DATA, skip_rows=to_skip_specific
    )

    raw_row, raw_col = test_data_skip_specific.billing_content.shape
    assert raw_row == test_data_length - len(to_skip_specific)
    assert raw_col == test_data_col


# cost multiplier
def test_data_load_multiply():
    to_multiply = 2
    test_data_skip = Focus("MyTestPlatform", SAMPLE_DATA, cost_multiplier=to_multiply)

    baseline_sum = pd.read_csv(SAMPLE_DATA)["EffectiveCost"].sum()
    test_data_skip.render()

    assert (
        test_data_skip.harness_focus_content["EffectiveCost"].sum()
        == baseline_sum * to_multiply
    )


# custom converters
def test_data_convert():
    test_data_convert = Focus(
        "MyTestPlatform",
        SAMPLE_DATA,
        converters={"BillingAccountId": lambda x: "FakeAccountID"},
    )

    assert (
        test_data_convert.billing_content.iloc[0]["BillingAccountId"] == "FakeAccountID"
    )
    assert (
        test_data_convert.billing_content.iloc[test_data_length - 1]["BillingAccountId"]
        == "FakeAccountID"
    )


# custom converters
def test_data_null_provider(tmpdir):
    filename = tmpdir.join("output.csv")

    test_data_setup = Focus(
        "MyTestPlatform",
        SAMPLE_DATA,
        converters={"ProviderName": lambda _: ""},
    )

    test_data_setup.render_file(filename)

    test_data_provider = Focus(
        "MyTestPlatformTest",
        filename,
    )

    assert (
        test_data_provider.billing_content.iloc[0]["ProviderName"]
        == "MyTestPlatformTest"
    )


def test_data_mapping(tmpdir):
    filename = tmpdir.join("output.csv")
    mapped_col = {"SkuId": "SKU"}
    one_off = pd.read_csv(SAMPLE_DATA, dtype=str)
    one_off.rename(columns=mapped_col).to_csv(filename, index=False)

    test_data_remap = Focus("MyTestPlatform", filename, mapping=mapped_col)

    test_data_remap.render()

    assert len(test_data_remap.harness_focus_content["SkuId"]) == test_data_length


def test_data_mapping_empty(tmpdir):
    test_data_empty = Focus(
        "MyTestPlatform",
        SAMPLE_DATA,
        mapping={},
    )

    assert test_data_empty.render() is not None

    test_data_none = Focus(
        "MyTestPlatform",
        SAMPLE_DATA,
        mapping=None,
    )

    assert test_data_none.render() is not None

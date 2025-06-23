from focus import Focus, HARNESS_FIELDS

import pandas as pd

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
    focus_row, focus_col = test_data.focus_content.shape
    assert focus_row == test_data_length
    assert focus_col == len(HARNESS_FIELDS)
    assert (
        test_data.focus_content["EffectiveCost"].sum()
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
        test_data_skip.focus_content["EffectiveCost"].sum()
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

import math

import pandas as pd

from src.harness_ccm_external_data import Focus, HARNESS_FIELDS

ISO_8601 = "%Y-%m-%dT%H:%M:%SZ"

DATE_COLUMNS = ["BillingPeriodStart", "BillingPeriodEnd", "ChargePeriodStart", "ChargePeriodEnd"]

NON_ISO_DATES = {
    "BillingPeriodStart": "2026-05-01 00:00:00",
    "BillingPeriodEnd": "2026-06-01 00:00:00",
    "ChargePeriodStart": "2026-05-30 00:00:00",
    "ChargePeriodEnd": "2026-05-31 00:00:00",
}

EXPECTED_ISO = {
    "BillingPeriodStart": "2026-05-01T00:00:00Z",
    "BillingPeriodEnd": "2026-06-01T00:00:00Z",
    "ChargePeriodStart": "2026-05-30T00:00:00Z",
    "ChargePeriodEnd": "2026-05-31T00:00:00Z",
}


def _write_sample_csv(path, date_overrides=None):
    defaults = {
        "BillingAccountId": "123",
        "BillingAccountName": "TestAccount",
        "BillingPeriodEnd": "2026-06-01T00:00:00Z",
        "BillingPeriodStart": "2026-05-01T00:00:00Z",
        "ChargeCategory": "Usage",
        "ChargePeriodStart": "2026-05-30T00:00:00Z",
        "ChargePeriodEnd": "2026-05-31T00:00:00Z",
        "ConsumedQuantity": "1.0",
        "EffectiveCost": "10.0",
        "ProviderName": "AWS",
        "ResourceId": "arn:test",
        "RegionName": "us-east-1",
        "ServiceName": "EC2",
        "SubAccountId": "sub-001",
        "SkuId": "SKU-1",
        "SubAccountName": "SubTest",
        "Tags": "",
    }
    if date_overrides:
        defaults.update(date_overrides)
    pd.DataFrame([defaults]).to_csv(path, index=False)


# _normalize_date static method


def test_normalize_date_already_iso8601():
    value = "2026-05-01T00:00:00Z"
    assert Focus._normalize_date(value) == value


def test_normalize_date_already_iso8601_with_time():
    value = "2024-09-18T22:30:00Z"
    assert Focus._normalize_date(value) == value


def test_normalize_date_space_separator():
    assert Focus._normalize_date("2026-05-01 00:00:00") == "2026-05-01T00:00:00Z"


def test_normalize_date_space_separator_with_time():
    assert Focus._normalize_date("2024-09-18 22:30:45") == "2024-09-18T22:30:45Z"


def test_normalize_date_t_without_z():
    assert Focus._normalize_date("2026-05-01T00:00:00") == "2026-05-01T00:00:00Z"


def test_normalize_date_date_only():
    assert Focus._normalize_date("2026-05-01") == "2026-05-01T00:00:00Z"


def test_normalize_date_empty_string():
    assert Focus._normalize_date("") == ""


def test_normalize_date_nan():
    result = Focus._normalize_date(float("nan"))
    assert isinstance(result, float) and math.isnan(result)


def test_normalize_date_pandas_nat():
    assert pd.isna(Focus._normalize_date(pd.NaT))


def test_normalize_date_unrecognized_format():
    value = "not-a-date"
    assert Focus._normalize_date(value) == value


def test_normalize_date_output_is_valid_iso8601():
    from datetime import datetime

    result = Focus._normalize_date("2026-01-15 08:30:00")
    dt = datetime.strptime(result, ISO_8601)
    assert dt.year == 2026
    assert dt.month == 1
    assert dt.day == 15
    assert dt.hour == 8
    assert dt.minute == 30


# normalize_dates constructor option


def test_dates_normalized_when_enabled(tmpdir):
    csv_path = str(tmpdir.join("sample.csv"))
    _write_sample_csv(csv_path, NON_ISO_DATES)

    focus = Focus("AWS", "Test", csv_path, normalize_dates=True)

    for col, expected in EXPECTED_ISO.items():
        assert focus.billing_content.iloc[0][col] == expected


def test_dates_not_normalized_by_default(tmpdir):
    csv_path = str(tmpdir.join("sample.csv"))
    _write_sample_csv(csv_path, NON_ISO_DATES)

    focus = Focus("AWS", "Test", csv_path)

    for col, original in NON_ISO_DATES.items():
        assert focus.billing_content.iloc[0][col] == original


def test_dates_not_normalized_when_disabled(tmpdir):
    csv_path = str(tmpdir.join("sample.csv"))
    _write_sample_csv(csv_path, NON_ISO_DATES)

    focus = Focus("AWS", "Test", csv_path, normalize_dates=False)

    for col, original in NON_ISO_DATES.items():
        assert focus.billing_content.iloc[0][col] == original


def test_already_iso_dates_unchanged_when_normalized(tmpdir):
    csv_path = str(tmpdir.join("sample.csv"))
    _write_sample_csv(csv_path)

    focus = Focus("AWS", "Test", csv_path, normalize_dates=True)

    for col, expected in EXPECTED_ISO.items():
        assert focus.billing_content.iloc[0][col] == expected


def test_normalize_does_not_affect_non_date_columns(tmpdir):
    csv_path = str(tmpdir.join("sample.csv"))
    _write_sample_csv(csv_path, NON_ISO_DATES)

    focus = Focus("AWS", "Test", csv_path, normalize_dates=True)
    row = focus.billing_content.iloc[0]

    assert row["BillingAccountName"] == "TestAccount"
    assert row["ServiceName"] == "EC2"
    assert row["RegionName"] == "us-east-1"
    assert float(row["EffectiveCost"]) == 10.0


def test_normalize_dates_present_in_rendered_output(tmpdir):
    csv_path = str(tmpdir.join("sample.csv"))
    output_path = str(tmpdir.join("output.csv"))
    _write_sample_csv(csv_path, NON_ISO_DATES)

    focus = Focus("AWS", "Test", csv_path, normalize_dates=True)
    focus.render()
    focus.render_file(output_path)

    result = pd.read_csv(output_path, dtype=str)
    for col, expected in EXPECTED_ISO.items():
        assert result.iloc[0][col] == expected


def test_normalize_works_with_mixed_date_formats(tmpdir):
    csv_path = str(tmpdir.join("sample.csv"))
    _write_sample_csv(csv_path, {
        "BillingPeriodStart": "2026-05-01 00:00:00",
        "BillingPeriodEnd": "2026-06-01T00:00:00Z",
        "ChargePeriodStart": "2026-05-30T00:00:00",
        "ChargePeriodEnd": "2026-05-31",
    })

    focus = Focus("AWS", "Test", csv_path, normalize_dates=True)
    row = focus.billing_content.iloc[0]

    assert row["BillingPeriodStart"] == "2026-05-01T00:00:00Z"
    assert row["BillingPeriodEnd"] == "2026-06-01T00:00:00Z"
    assert row["ChargePeriodStart"] == "2026-05-30T00:00:00Z"
    assert row["ChargePeriodEnd"] == "2026-05-31T00:00:00Z"

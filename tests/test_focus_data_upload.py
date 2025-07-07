from src.harness_ccm_external_data import Focus

from os import getenv
from datetime import datetime

SAMPLE_DATA = "focus_sample.csv"


def test_data_provider():
    test_data = Focus(
        "MyTestPlatform",
        "Test",
        SAMPLE_DATA,
        harness_account_id=getenv("HARNESS_ACCOUNT_ID"),
        harness_platform_api_key=getenv("HARNESS_PLATFORM_API_KEY"),
    )

    assert test_data._create_provider() is not None
    assert test_data.provider_uuid is not None

    assert test_data._delete_provider() is True
    assert test_data.provider_uuid is None


def test_data_upload():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    may_data = Focus(
        "Testing Upload",
        timestamp,
        "focus_sample_2025_05.csv",
        converters={
            "BillingPeriodStart": lambda _: "2025-5-01 00:00:00",
            "BillingPeriodEnd": lambda _: "2025-6-01 00:00:00",
        },
        harness_account_id=getenv("HARNESS_ACCOUNT_ID"),
        harness_platform_api_key=getenv("HARNESS_PLATFORM_API_KEY"),
    )

    assert may_data.upload() is True

    june_data = Focus(
        "Testing Upload",
        timestamp,
        "focus_sample_2025_06.csv",
        converters={
            "BillingPeriodStart": lambda _: "2025-6-01 00:00:00",
            "BillingPeriodEnd": lambda _: "2025-7-01 00:00:00",
        },
        provider_uuid=may_data.provider_uuid,
        harness_account_id=getenv("HARNESS_ACCOUNT_ID"),
        harness_platform_api_key=getenv("HARNESS_PLATFORM_API_KEY"),
    )

    assert june_data.upload() is True

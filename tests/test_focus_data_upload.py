from src.harness_ccm_external_data import Focus

from os import getenv
from datetime import datetime
import random

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
    billing_account_id = random.randint(100000000000, 999999999999)

    may_data = Focus(
        "Testing Upload",
        timestamp,
        SAMPLE_DATA,
        cost_multiplier=random.uniform(1.0, 2.0),
        converters={
            "BillingPeriodStart": lambda _: "2025-5-01T00:00:00",
            "BillingPeriodEnd": lambda _: "2025-6-01T00:00:00",
            "BillingAccountId": lambda _: billing_account_id,
            "BillingAccountName": lambda _: "Billing Account Name",
            "SubAccountId": lambda _: random.randint(100000000000, 999999999999),
            "SubAccountName": lambda _: "Sub Account Name",
        },
        harness_account_id=getenv("HARNESS_ACCOUNT_ID"),
        harness_platform_api_key=getenv("HARNESS_PLATFORM_API_KEY"),
    )

    assert may_data.upload() is not None

    june_data = Focus(
        "Testing Upload",
        timestamp,
        SAMPLE_DATA,
        cost_multiplier=random.uniform(1.0, 2.0),
        converters={
            "BillingPeriodStart": lambda _: "2025-6-01T00:00:00",
            "BillingPeriodEnd": lambda _: "2025-7-01T00:00:00",
            "BillingAccountId": lambda _: billing_account_id,
            "BillingAccountName": lambda _: "Billing Account Name",
            "SubAccountId": lambda _: random.randint(100000000000, 999999999999),
            "SubAccountName": lambda _: "Sub Account Name",
        },
        provider_uuid=may_data.provider_uuid,
        harness_account_id=getenv("HARNESS_ACCOUNT_ID"),
        harness_platform_api_key=getenv("HARNESS_PLATFORM_API_KEY"),
    )

    assert june_data.upload() is not None

from pandas._testing import iloc
from src.harness_ccm_external_data import Focus, HARNESS_FIELDS

TEST_DATA = [
    [
        1234567890123,
        "SunBird",
        "2025-6-01 00:00:00",
        "2025-5-01 00:00:00",
        "Usage",
        "2024-09-18 22:00:00",
        "2024-09-18 23:00:00",
        2.0,
        0.0,
        "AWS",
        "arn:ats:sqs:us-test-2:347410479675:mibelllmel-i-032l64f2065481b12",
        "US West (Oregon)",
        "Amazon Simple Queue Service",
        51738928782,
        "G95FST5FTYV3JSRX",
        "Atlas Nimbus",
    ],
    [
        1234567890124,
        "SunBird2",
        "2025-6-01 00:00:00",
        "2025-5-01 00:00:00",
        "Usage",
        "2024-09-30 22:00:00",
        "2024-09-30 23:00:00",
        0.00200749,
        0.0,
        "AWS",
        "arn:ats:emastilmoalfamanling:us-test-2:586597448978:moalfamanler/app/tungsten-lonbmuenle-amf/l365455f461l4e4a",
        "US West (Oregon)",
        "Elastic Load Balancing",
        43883916739,
        "2ETY8Y426S4237JU",
        "Zenith Eclipse",
        '{"application": "BrightLensMatrix", "environment": "dev", "business_unit": "ViennaAI"}',
    ],
]


def test_base_df():
    empty_df = Focus.create_dataset()
    assert empty_df is not None
    assert empty_df.empty
    assert set(HARNESS_FIELDS).issubset(set(empty_df.columns))


def test_passing_df():
    df = Focus.create_dataset(TEST_DATA)
    test = Focus("MyTestPlatform", "Test", df)

    test.load_and_convert_data()

    assert set(HARNESS_FIELDS).issubset(set(test.billing_content.columns))

    test.convert_fields()

    assert test.harness_focus_content is not None
    assert not test.harness_focus_content.empty
    assert set(HARNESS_FIELDS).issubset(set(test.harness_focus_content.columns))
    assert test.harness_focus_content.iloc[1]["BillingAccountName"] == TEST_DATA[1][1]

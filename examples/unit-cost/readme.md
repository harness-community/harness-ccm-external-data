# unit cost

to visualize "unit cost" in harness we can use external data to ingest units into Harness wich can then be visualized in the tool alongside cloud costs

## buiding data

in this example we will build unit data using python, but this can be done using a CSV as well

we will fill in "nonsense" data for most fields, you can add in real data for those fields if you "unit" data is specific to some account/service/application/ect

```python
from src.harness_ccm_external_data import Focus
from os import getenv

data = [
    [
        # BillingAccountId
        100000000000,
        # BillingAccountName
        "UnitCost",
        # BillingPeriodEnd
        "2025-6-01 00:00:00",
        # BillingPeriodStart
        "2025-5-01 00:00:00",
        # ChargeCategory
        "Unit",
        # ChargePeriodStart
        "2025-6-01 00:00:00",
        # ChargePeriodEnd
        "2025-5-01 00:00:00",
        # ConsumedQuantity
        1.0,
        # EffectiveCost
        0.0,
        # ProviderName
        "AWS",
        # ResourceId
        "Users",
        # RegionName
        "UnitCost",
        # ServiceName
        "Users",
        # SubAccountId
        100000000000,
        # SkuId
        "UnitCost",
        # SubAccountName
        "UnitCost",
        # Tags
        "{}",
    ]
]

my_data = Focus(
    provider="Unit Cost",
    data_source="Unit Cost",
    source=Focus.create_dataset(data),
    harness_account_id=getenv("HARNESS_ACCOUNT_ID"),
    harness_platform_api_key=getenv("HARNESS_PLATFORM_API_KEY"),
)

my_data.upload()
```

at this point the unit data is available in harness

we can now create a dashboard to take our cost cost for the units, divide it by the number of units (defined in our uploaded data) to get a unit cost


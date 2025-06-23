from typing import Dict, Sequence
from collections import defaultdict

import pandas as pd

HARNESS_FIELDS = [
    "BillingAccountId",
    "BillingAccountName",
    "BillingPeriodEnd",
    "BillingPeriodStart",
    "ChargeCategory",
    "ChargePeriodStart",
    "ChargePeriodEnd",
    "ConsumedQuantity",
    "EffectiveCost",
    "ProviderName",
    "ResourceId",
    "RegionName",
    "ServiceName",
    "SubAccountId",
    "SkuId",
    "SubAccountName",
    "Tags",
]

file_limit = 20000000


class Focus:
    def __init__(
        self,
        platform: str,
        filename: str,
        mapping: Dict[str, str] = {x: x for x in HARNESS_FIELDS},
        seperator: str = ",",
        skip_rows: int | Sequence[int] = None,
        cost_multiplier: float = 1.0,
        validate: bool = True,
    ):
        self.platform = platform
        self.mapping = mapping
        self.cost_multiplier = cost_multiplier
        self.focus_content: pd.DataFrame = None

        # restrict fields to ones supported by ccm
        # allow disabling verification for instances when the platform moves faster than the code
        if validate:
            for field in mapping.copy():
                if field not in HARNESS_FIELDS:
                    print(
                        f"WARNING: Field {field} is not a recognized harness focus field. Will be ignored"
                    )
                    del mapping[field]

        cost_multiplier_func = lambda x: pd.to_numeric(x) * cost_multiplier
        self.billing_content = pd.read_csv(
            filename,
            sep=seperator,
            engine="python",
            skiprows=skip_rows,
            converters={"EffectiveCost": cost_multiplier_func},
        )

    def render(self) -> pd.DataFrame:
        self.focus_content = pd.DataFrame()
        for focus_field, source_field in self.mapping.items():
            if source_field in self.billing_content.columns:
                self.focus_content[focus_field] = self.billing_content[source_field]
            else:
                # Default value for missing columns
                self.focus_content[focus_field] = source_field
        return self.focus_content

    def render_file(self, filename: str):
        if self.focus_content.empty:
            self.render().to_csv(filename, index=False)
        else:
            self.focus_content.to_csv(filename, index=False)

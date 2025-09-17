from typing import Dict, Sequence, Optional
import hashlib
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

from .focus_data import Focus

MONGODB_ATLAS_MAPPING = {
    "BillingAccountId": "Organization ID",
    "BillingAccountName": "Organization Name",
    "BillingPeriodEnd": "Date",
    "BillingPeriodStart": "Date",
    "ChargeCategory": "Note",
    "ChargePeriodStart": "Usage Date",
    "ChargePeriodEnd": "Date",
    "ConsumedQuantity": "Quantity",
    "EffectiveCost": "Amount",
    "ResourceId": "Cluster",
    "RegionName": "Region",
    "ServiceName": "SKU",
    "SubAccountId": "Project ID",
    "SkuId": "SKU",
    "SubAccountName": "Project Name",
}


class MongoDBAtlas(Focus):
    def __init__(
        self,
        provider: str,
        data_source: str,
        source: str | pd.DataFrame,
        provider_type: str = "CUSTOM",
        invoice_period: str = "MONTHLY",
        provider_uuid: str = None,
        mapping: Dict[str, str] = {},
        separator: str = ",",
        skip_rows: int | Sequence[int] = 5,
        cost_multiplier: float = 1.0,
        converters: Dict[str, callable] = {},
        additional_columns: Dict[str, str] = {},
        validate: bool = True,
        harness_platform_api_key: str = None,
        harness_account_id: str = None,
    ):
        super().__init__(
            provider,
            data_source,
            source,
            provider_type,
            invoice_period,
            provider_uuid,
            MONGODB_ATLAS_MAPPING | mapping,
            separator,
            skip_rows,
            cost_multiplier,
            converters,
            additional_columns,
            validate,
            harness_platform_api_key,
            harness_account_id,
        )

    def convert_fields(self) -> pd.DataFrame:
        super().convert_fields()

        # create resource id using Cluster/Replica Set/Config Server/Application
        self.harness_focus_content["ResourceId"] = self.billing_content[
            self.billing_content.columns[10:14]
        ].apply(lambda x: "/".join(x.dropna().astype(str)), axis=1)

        # Take individual tag columns and combine them into the focus_data format dictionary.
        self.harness_focus_content["Tags"] = self.billing_content[
            self.billing_content.columns[19:]
        ].apply(
            lambda x: {
                key.split("/")[1]: str(value)
                for key, value in x.to_dict().items()
                if not pd.isna(value)
            },
            axis=1,
        )

        self.harness_focus_content["BillingPeriodStart"] = self.harness_focus_content[
            "BillingPeriodStart"
        ].apply(
            lambda x: datetime.strptime(x, "%m/%d/%Y")
            .replace(day=1)
            .strftime("%Y-%m-%dT00:00:00")
        )

        self.harness_focus_content["BillingPeriodEnd"] = self.harness_focus_content[
            "BillingPeriodEnd"
        ].apply(
            lambda x: (
                datetime.strptime(x, "%m/%d/%Y").replace(day=1)
                + relativedelta(months=1)
            ).strftime("%Y-%m-%dT00:00:00")
        )

        self.harness_focus_content["ChargePeriodStart"] = self.harness_focus_content[
            "ChargePeriodStart"
        ].apply(
            lambda x: datetime.strptime(x, "%m/%d/%Y")
            .replace(day=1)
            .strftime("%Y-%m-%dT%H:%M:%S")
        )

        self.harness_focus_content["ChargePeriodEnd"] = self.harness_focus_content[
            "ChargePeriodEnd"
        ].apply(
            lambda x: (
                datetime.strptime(x, "%m/%d/%Y") + relativedelta(days=1)
            ).strftime("%Y-%m-%dT%H:%M:%S")
        )

        return self.harness_focus_content

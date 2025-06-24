from os import getenv

from requests import post, delete


class Provider:
    def __init__(
        self,
        datasource: str,
        provider: str,
        provider_type: str = "CUSTOM",
        invoice_period: str = "MONTHLY",
        harness_account: str = getenv("HARNESS_ACCOUNT_ID"),
        harness_url: str = getenv("HARNESS_URL"),
        harness_platform_api_key: str = getenv("HARNESS_PLATFORM_API_KEY"),
    ):
        self.datasource = datasource
        self.provider = provider
        self.provider_type = provider_type
        self.invoice_period = invoice_period
        self.harness_account = harness_account
        self.harness_url = harness_url
        self.harness_platform_api_key = harness_platform_api_key

        # load in uuid if provider already exists, otherwise create one
        if existing_providers := [
            x
            for x in Provider.get_providers(
                self.harness_account,
                self.harness_url,
                self.harness_platform_api_key,
            )
            if x["providerName"] == self.provider
        ]:
            self.uuid = existing_providers.pop()["uuid"]
        else:
            self.create()

    def create(self):
        """
        Create a new external data provider
        """

        resp = post(
            f"https://{self.harness_url}/gateway/ccm/api/externaldata/provider",
            headers={"x-api-key": self.harness_platform_api_key},
            params={
                "routingId": self.harness_account,
                "accountIdentifier": self.harness_account,
            },
            json={
                "externalDataProvider": {
                    "name": self.datasource,
                    "providerType": self.provider_type,
                    "providerName": self.provider,
                    "invoicePeriod": self.invoice_period,
                }
            },
        )

        resp.raise_for_status()

        self.uuid = resp.json()["data"]["uuid"]

        return self.uuid

    def delete(self):
        resp = delete(
            f"https://{self.harness_url}/gateway/ccm/api/externaldata/provider/{self.uuid}",
            headers={"x-api-key": self.harness_platform_api_key},
            params={
                "routingId": self.harness_account,
                "accountIdentifier": self.harness_account,
            },
        )

        resp.raise_for_status()

        self.uuid = None

    def get_providers(
        harness_account: str = getenv("HARNESS_ACCOUNT_ID"),
        harness_url: str = getenv("HARNESS_URL"),
        harness_platform_api_key: str = getenv("HARNESS_PLATFORM_API_KEY"),
    ):
        """
        Get all external data providers in an account
        Currently no support for search
        """

        resp = post(
            f"https://{harness_url}/gateway/ccm/api/externaldata/provider/list",
            headers={"x-api-key": harness_platform_api_key},
            params={"routingId": harness_account, "accountIdentifier": harness_account},
            json={},
        )

        resp.raise_for_status()

        return resp.json()["data"]

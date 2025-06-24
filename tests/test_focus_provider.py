from src.harness_ccm_external_data import Provider


def test_create_delete_provider():
    provider = Provider(
        datasource="Python",
        provider="PyLib Test",
    )

    assert provider.uuid is not None

    provider_dup = Provider(
        datasource="Python",
        provider="PyLib Test",
    )

    assert provider_dup.uuid == provider.uuid

    provider.delete()

    assert provider.uuid is None

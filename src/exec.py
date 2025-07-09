from harness_ccm_external_data import Focus

from os import getenv
from json import loads
from sys import exit


def write_outputs(outputs: dict[str, str]):
    """
    write key value outputs to a local file to be rendered in the plugin step

    args:
        outputs (dict[str, str]): string to string mappings
    """

    output_file = open(getenv("DRONE_OUTPUT"), "a")

    for k, v in outputs.items():
        output_file.write(f"{k}={v}\n")

    output_file.close()


if __name__ == "__main__":
    # if we are being used as a drone plugin, prefix env with   PLUGIN_
    if getenv("DRONE_OUTPUT"):
        print("Running in drone/harness, using PLUGIN_")
        prefix = "PLUGIN_"
    else:
        prefix = ""

    if not (provider := getenv(f"{prefix}PROVIDER")):
        print("Must pass provider name via PROVIDER")
        exit(1)

    if not (data_source := getenv(f"{prefix}DATA_SOURCE")):
        print("Must pass data source via DATA_SOURCE")
        exit(1)

    if not (provider_type := getenv(f"{prefix}PROVIDER_TYPE")):
        print("Must pass provider type via PROVIDER_TYPE")
        exit(1)

    if not (invoice_period := getenv(f"{prefix}INVOICE_PERIOD")):
        print("Must pass invoice period via INVOICE_PERIOD")
        exit(1)

    if not (filename := getenv(f"{prefix}CSV_FILE")):
        print("Must pass csv name via CSV_FILE")
        exit(1)

    mapping = loads(getenv(f"{prefix}MAPPING", "{}"))

    if not (skip_rows := getenv(f"{prefix}SKIP_ROWS")):
        skip_rows = None

    if not (cost_multiplier := getenv(f"{prefix}COST_MULTIPLIER")):
        cost_multiplier = None

    if not (validate := bool(getenv(f"{prefix}VALIDATE"))):
        validate = True

    focus = Focus(
        provider=provider,
        data_source=data_source,
        provider_type=provider_type,
        invoice_period=invoice_period,
        filename=filename,
        mapping=mapping,
        skip_rows=skip_rows,
        cost_multiplier=cost_multiplier,
        validate=validate,
        harness_platform_api_key=getenv(f"{prefix}HARNESS_PLATFORM_API_KEY"),
        harness_account_id=getenv(f"{prefix}HARNESS_ACCOUNT_ID"),
    )

    if destination_file := getenv(f"{prefix}RENDER_FILE"):
        focus.render_file(destination_file)
        if prefix:
            write_outputs({"output_file": destination_file})

    if upload := getenv(f"{prefix}UPLOAD"):
        result = focus.upload()
        if prefix:
            write_outputs({"uploaded": str(result).lower()})

    print(focus)

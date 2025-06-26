from harness_ccm_external_data import Focus, HARNESS_FIELDS

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
    # if we are being used as a drone plugin, prefix env with SETTING_
    if getenv("DRONE_OUTPUT"):
        prefix = "SETTING_"
    else:
        prefix = ""

    provider = getenv(f"{prefix}PROVIDER")
    if not provider:
        print("Must pass provider name via PROVIDER")
        exit(1)

    filename = getenv(f"{prefix}CSV_FILE")
    if not filename:
        print("Must pass csv name via CSV_FILE")
        exit(1)

    mapping = loads(getenv(f"{prefix}MAPPING", "{}"))

    skip_rows = getenv(f"{prefix}SKIP_ROWS")

    cost_multiplier = getenv(f"{prefix}COST_MULTIPLIER")
    if cost_multiplier:
        cost_multiplier = int(cost_multiplier)

    validate = bool(getenv(f"{prefix}VALIDATE"))

    focus = Focus(
        provider=provider,
        filename=filename,
        mapping=mapping,
        skip_rows=skip_rows,
        cost_multiplier=cost_multiplier,
        validate=validate,
    )

    if destination_file := getenv(f"{prefix}RENDER_FILE"):
        focus.render_file(destination_file)
        if prefix:
            write_outputs({"output_file": destination_file})

    print(focus)

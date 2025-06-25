from harness_ccm_external_data import Focus, HARNESS_FIELDS

from os import getenv
from json import loads
from sys import exit

if __name__ == "__main__":

    provider = getenv("PROVIDER")
    if not provider:
        print("Must pass provider name via PROVIDER")
        exit(1)

    filename = getenv("CSV_FILE")
    if not filename:
        print("Must pass csv name via CSV_FILE")
        exit(1)

    mapping = loads(getenv("MAPPING", "{}"))

    skip_rows = getenv("SKIP_ROWS")

    cost_multiplier = getenv("COST_MULTIPLIER")
    if cost_multiplier:
        cost_multiplier = int(cost_multiplier)

    validate = bool(getenv("VALIDATE"))

    focus = Focus(
        provider=provider,
        filename=filename,
        mapping=mapping,
        skip_rows=skip_rows,
        cost_multiplier=cost_multiplier,
        validate=validate,
    )

    if destination_file := getenv("RENDER_FILE"):
        focus.render_file(destination_file)
    
    print(focus)

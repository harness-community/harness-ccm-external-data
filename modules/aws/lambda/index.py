from os import getenv
import json
import logging

import boto3

from harness_ccm_external_data import Focus

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    s3 = boto3.client('s3')

    uploaded_files = []
    failed_files = []

    for record in event["Records"]:
        logging.info(json.dumps(record, indent=2))

        provider = getenv("PROVIDER")
        data_source = getenv("DATA_SOURCE")
        filename = record["s3"]["object"]["key"].split("/")[-1]
        mapping = json.loads(getenv("MAPPING", "{}"))

        s3.download_file(record["s3"]["bucket"]["name"], record["s3"]["object"]["key"], f"/tmp/{filename}")

        focus_data = Focus(
            provider,
            data_source,
            f"/tmp/{filename}",
            mapping=mapping,
            harness_account_id=getenv("HARNESS_ACCOUNT_ID"),
            harness_platform_api_key=getenv("HARNESS_PLATFORM_API_KEY")
        )

        try:
            focus_data.upload()
            pass
        except Exception as e:
            logging.error(record["s3"]["object"]["key"] + ": " + e)
            failed_files.append(record["s3"]["object"]["key"])
            continue
        
        uploaded_files.append(record["s3"]["object"]["key"])

    return {
        "statusCode": 200 if not failed_files else 400,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"success": uploaded_files, "failure": failed_files})
    }
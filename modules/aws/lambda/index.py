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
        filename = record["s3"]["object"]["key"].split("/")[-1]
        mapping = json.loads(getenv("MAPPING", "{}"))

        s3.download_file(record["s3"]["bucket"]["name"], record["s3"]["object"]["key"], f"/tmp/{filename}")

        focus_data = Focus(
            provider,
            f"/tmp/{filename}",
            mapping=mapping
        )

        destination_filename = f"/tmp/processed_{filename}"

        try:
            focus_data.render_file(destination_filename)
        except Exception as e:
            logging.error(record["s3"]["object"]["key"] + ": " + e)
            failed_files.append(record["s3"]["object"]["key"])
            continue
            
        try:
            # upload file
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
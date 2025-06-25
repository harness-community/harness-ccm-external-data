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

    for record in event["Records"]:
        logging.info(json.dumps(record, indent=2))

        provider = getenv("PROVIDER")
        filename = f'/tmp/{record["s3"]["object"]["key"].split("/")[-1]}'
        mapping = json.loads(getenv("MAPPING"))

        s3.download_file(record["s3"]["bucket"]["name"], record["s3"]["object"]["key"], filename)

        focus_data = Focus(
            provider,
            filename,
            mapping=mapping if mapping else None
        )

        destination_filename = f"/tmp/processed_{filename}"

        focus_data.render_file(destination_filename)

        # upload file
        
        uploaded_files.append(destination_filename)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(uploaded_files)
    }
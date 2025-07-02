import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient

def main(blob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {blob.name}\n"
                 f"Blob Size: {blob.length} bytes")
    # Example: read blob content
    data = blob.read()
    # TODO: Your Python logic here
    logging.info(f"Blob data: {data[:100]}")

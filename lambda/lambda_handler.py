import boto3
from io import BytesIO
from PIL import Image
import os


def lambda_handler(event, context):
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    source_image_key = event["Records"][0]["s3"]["object"]["key"]

    thumbnail_destination_bucket = (
        "s3-trigger-thumbnail-destination-bucket-mnm"
    )
    thumbnail_image_name, thumbnail_image_ext = os.path.splitext(source_image_key)
    thumbnail_image_key = f"{thumbnail_image_name}_thumbnail{thumbnail_image_ext}"

    s3_client = boto3.client("s3")

    # Load and open image from S3
    file_byte_string = s3_client.get_object(Bucket=source_bucket, Key=source_image_key)[
        "Body"
    ].read()
    img = Image.open(BytesIO(file_byte_string))

    # Generate thumbnail
    img.thumbnail((500, 500), Image.ANTIALIAS)

    # Dump and save image to S3
    buffer = BytesIO()
    img.save(buffer, "JPEG")
    buffer.seek(0)

    sent_data = s3_client.put_object(
        Bucket=thumbnail_destination_bucket, Key=thumbnail_image_key, Body=buffer
    )

    if sent_data["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(
            f"Failed to upload image {source_image_key} to bucket {source_bucket}"
        )

    return event

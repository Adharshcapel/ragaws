# import boto3
# from dotenv import load_dotenv
# import os

# load_dotenv()

# # create S3 client
# s3 = boto3.client(
#     "s3",
#     region_name=os.getenv("AWS_DEFAULT_REGION")
# )

# bucket_name = "rag-diet-bucket-adharsh-demo"  # must be unique

# # ✅ Create bucket
# try:
#     s3.create_bucket(
#         Bucket=bucket_name,
#         CreateBucketConfiguration={
#             "LocationConstraint": os.getenv("AWS_DEFAULT_REGION")
#         }
#     )
#     print("✅ Bucket created")
# except Exception as e:
#     print("Bucket may already exist:", e)

# # ✅ Upload file
# file_path = "data/diet.pdf"  # your local path
# s3.upload_file(file_path, bucket_name, "diet.pdf")

# print("✅ File uploaded")
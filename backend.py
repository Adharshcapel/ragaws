import boto3
import os
from dotenv import load_dotenv

load_dotenv()

KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
MODEL_ARN = os.getenv("MODEL_ARN")
REGION = os.getenv("AWS_DEFAULT_REGION")


def query_kb(question):

    # Create Bedrock client only when query is called
    client = boto3.client(
        "bedrock-agent-runtime",
        region_name=REGION
    )

    response = client.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN
            }
        }
    )

    answer = response["output"]["text"]

    sources = []

    try:
        for item in response["citations"]:
            for ref in item["retrievedReferences"]:
                sources.append(ref["content"]["text"])
    except:
        pass

    return answer, sources
import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event=None, context=None):
    aws_region = "us-east-1"

    subject = "Welcome! Please verify your email address"
    sender = "noReply@prod.linqinyun.me"
    recipient = "linqinyun@outlook.com"

    # if event is not None:
    #     email_data = event['Records'][0]["messageAttributes"]
    #     print(email_data)
    #     recipient = email_data['toEmail']['stringValue']
    # else:
    #     recipient = "linqinyun@outlook.com"
    #     # recipient = "846705900@qq.com"

    destination = {
        'ToAddresses': [
            recipient,
        ]
    }

    body_text = """
Amazon SES:

    You are creating your account in our webservice, we are sending this to verify the email you provide is valid.

CSYE6225 webservice team
    """

    charset = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=aws_region)

    try:
        response = client.send_email(
            Destination=destination,
            Message={
                'Body': {
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender
        )

    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])
        print(recipient)

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(response)
    # }


if __name__ == '__main__':
    lambda_handler()

import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event=None, context=None):
    aws_region = "us-east-1"

    subject = "Welcome! Please verify your email address"
    sender = "noReply@prod.linqinyun.me"
    # recipient = "linqinyun@outlook.com"

    if event is not None:
        message = event['Records'][0]['Sns']['Message']
        message = json.loads(message)
        print(message)
        recipient = message["email"]
        token = message["token"]
    else:
        recipient = "linqinyun@outlook.com"
        from uuid import uuid4
        token = uuid4()

    table = boto3.resource('dynamodb', region_name=aws_region).Table('csye6225-token')
    response = table.get_item(Key={"UserId": recipient})
    if "Item" in response.keys():
        item = response['Item']
        if item["sendStatus"] == "sent":
            return
    else:
        return

    destination = {
        'ToAddresses': [
            recipient,
        ]
    }

    link = "https://prod.linqinyun.me/v1/verifyUserEmail?email=%s&token=%s" % (recipient, token)
    body_text = "Dear web service user:\n\n" \
                "\tYou are creating your account in our webservice, " \
                "we are sending this to verify the email you provide is valid.\n" \
                "\tPlease click the link below to complete validation, this link will be expired in 5 minutes.\n" \
                "\t\t %s \n\n" \
                "CSYE6225 Webservice Team" % link
    print(body_text)
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

        item["sendStatus"] = "sent"
        table.put_item(Item=item)


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

from datetime import date, timedelta
from datetime import datetime
import calendar
import os
import boto3
from discord import SyncWebhook

# Create a Boto3 DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the table name
table_name = 'Reminders'

# Define the filter expression
filter_expression = 'DayOfWeek = :day_value AND ReminderTime = :time_value'

my_date = date.today()
day_of_Week = calendar.day_name[my_date.weekday()] 

current_time = datetime.now()
minutes_past_last_30 = current_time.minute % 30
rounded_time = (current_time - timedelta(minutes=minutes_past_last_30)).strftime('%H:%M')

# Define the expression attribute values
expression_attribute_values = {
    ':day_value': {'S': day_of_Week},
    ':time_value': {'S': rounded_time}

}

# Perform the query operation
response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
)

webhook_url = os.environ.get('WEBHOOK_URL')
webhook = SyncWebhook.from_url(webhook_url)
# Process the response
items = response['Items']
for item in items:
    # Process each item in the result
    print(item)
    webhook.send(item['Message']['S'])
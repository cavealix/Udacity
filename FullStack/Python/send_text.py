# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "AC917b9b86cc87183f9742bebc54496bfd"
auth_token = "f16f2ab20ebb9c6d16f9d7743f7f43e4"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+12105109651", from_="+15005550006",
                                     body="In the name of the king")
print message.sid

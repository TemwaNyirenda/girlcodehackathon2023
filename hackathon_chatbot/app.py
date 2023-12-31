import requests
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

import location2
import face_recognition2

app = Flask(__name__)

account_sid = 'ACf6d8437f9d2cfaa8d1960e73b19599f0'
auth_token = '207e2d00c1de53585d9e062830899a93'
client = Client(account_sid, auth_token)

@app.route('/bot', methods=['POST'])
def bot():
    
    # resp = MessagingResponse()
    # msg = resp.message()

    from_number = request.values.get("From").replace("whatsapp:", "")
    media_url = request.form.get('MediaUrl0')
    message = request.form.get('Body')
    

    if media_url:
        r = requests.get(media_url)
        content_type = r.headers['Content-Type']
        username = from_number
        if content_type == 'image/jpeg':
            filename = f'images/{username}/{message}.jpg'
        elif content_type == 'image/png':
            filename = f'images/{username}/{message}.png'
        elif content_type == 'image/gif':
            filename = f'images/{username}/{message}.gif'
        else:
            filename = None
        if filename:
            if not os.path.exists(f'images/{username}'):
                os.mkdir(f'images/{username}')
            with open(filename, 'wb') as f:
                f.write(r.content)
        if username == "+27769193737":
            verified = face_recognition2.compare_faces("images/+27769193737/Beryl_Reg.jpg", filename)
            if (verified) :
                message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + from_number,
                body="You've been verified"
            )
            else: 
                message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + from_number,
                body="We can't verify you"
            )
        else:
            verified = face_recognition2.compare_faces("images/+27677697515/ID.jpg", filename)
            if (verified) :
                message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + from_number,
                body="You've been verified"
            )
            else: 
                message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + from_number,
                body="We can't verify you"
            )

    elif 'Latitude' in request.values.keys() and 'Longitude' in request.values.keys():
        lat = request.values.get('Latitude')
        lon = request.values.get('Longitude')

        volunteer_details = location2.find_volunteer(lat, lon)

        if volunteer_details[0] == "":
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + from_number,
                body="Unfortunately, we haven't found a volunteer\n\
                    We will continue to search"
            )

        else:
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + from_number,
                body="We have found a volunteer:\n\
Their name is " + volunteer_details[0] +\
" and their number is " + volunteer_details[1]
            )

            send_message_volunteer_warrior(volunteer_details, from_number)

        ### reply logic code based on the `lat` and `lon` values will go here

        # msg.body(f'We received these coordinates: ({lat}, {lon})')

  ##      msg.body("We're searching for volunteers")

    else:

        incoming_msg = request.values.get('Body', '')
        print(incoming_msg)

        if "1" in incoming_msg and "2" in incoming_msg:
            message = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:' + from_number,
            body="Sorry, you need to pick a choice.\n\
Hi, how can we help:\n\
1. Do you want more information about us\n\
2. Do you need relocation services"
            )

        elif "2" in incoming_msg:
            message = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:' + from_number,
            body="Please send your location so we can search for a volunteer"
            )

        elif "1" in incoming_msg:
            message = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:' + from_number,
            body="Safe Passage is a revolutionary chatbot that \
aids in you journey to freedom.\n\
We will connect you to a trained volunteer responder \
who will provide guidance, arrange safe transportation, \
and collaborate with accredited service providers, \
including law enforcement and health professionals."
            )

        else:
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + from_number,
                body="Hi, how can we help:\n\
1. Do you want more information about us\n\
2. Do you need relocation services"
            )
        # msg.body('Hello!  This is the Twilio Traffic Bot.  Please share your location to get a live traffic report.')

    # return str(resp)
    # print(message.sid)
    return str(message.sid)



def send_message_volunteer_warrior(volunteer_details, from_number):
    message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:' + volunteer_details[1],
                body="Hi " + volunteer_details[0] +", there is a warrior in need of help\n\
Her number is " + from_number +\
" Please reach out to her"
            )


# message = client.messages.create(
#   from_='whatsapp:+14155238886',
#   to='whatsapp:+27677697515'
# )






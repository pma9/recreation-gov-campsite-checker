import os
import sys
import logging

from enums.emoji import Emoji
from twilio.rest import Client
from dotenv import load_dotenv


def _send_sms(msg):
    # TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
    # should also be set as environment variables
    client = Client()
    message = client.messages.create(
        to=os.getenv("TWILIO_TO_NUMBER"),
        from_=os.getenv("TWILIO_FROM_NUMBER"),
        body=msg,
    )
    logging.info("message sent with sid: " + message.sid)


def generate_availability_strings(stdin):
    available_site_strings = []
    for line in stdin:
        line = line.strip()
        if Emoji.SUCCESS.value in line:
            park_name_and_id = " ".join(line.split(":")[0].split(" ")[1:])
            num_available = line.split(":")[1][1].split(" ")[0]
            s = "{} site(s) available in {}".format(num_available, park_name_and_id)
            available_site_strings.append(s)
    return available_site_strings


def main(stdin):
    load_dotenv()
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    first_line = next(stdin)
    if "Something went wrong" in first_line:
        _send_sms("Recreation.gov checker is broken! Please help :'(")
        sys.exit()

    available_site_strings = generate_availability_strings(stdin)

    if available_site_strings:
        msg = first_line + "\n".join(available_site_strings)
        logging.info(msg)
        _send_sms(msg)
    else:
        logging.info("No campsites available, not sending SMS")
        sys.exit()


if __name__ == "__main__":
    main(sys.stdin)

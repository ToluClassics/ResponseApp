from flask import Flask, request, session
import requests
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
import random, os

from sheets import sheet

app = Flask(__name__)

app.secret_key = "hello world"

@app.route('/endsars', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "new query" not in session:
        session["new query"] = True
        msg.body("-- Welcome to #ENDSARS online report desk --" + 
                    "\n\n What do you want to report? " +
                    "\n\n Press 1 for Medical Issues " +
                    "\n\n Press 2 for Legal Issues " +
                    "\n\n Press 3 for Food and Supplies  " +
                    "\n\n Press 4 for Mental Health Emergencies  " +
                    "\n\n Press any other number for Others  " +
                    "\n\n -- #ENDSARS --")
        return str(resp)

    if incoming_msg in ["1", "2", "3", "4", "5"]:
        if incoming_msg == "1":
            session["emergency_type"] = "Medical Issues"
        elif incoming_msg == "2":
            session["emergency_type"] = "Legal Issues"
        elif incoming_msg == "3":
            session["emergency_type"] = "Food and Supplies"
        elif incoming_msg == "4":
            session["emergency_type"] = "Mental Health Emergencies"
        else:
            session["emergency_type"] = "Others"
        session["tracker"] = "log"
        msg.body("What is your name?")
        return str(resp)

    elif session.get("tracker") == "log":
        if "name" not in session:
            session["name"] = incoming_msg
            msg.body("What is your phone number?")
            return str(resp)
        elif "phone number" not in session:
            session["phone number"] = incoming_msg
            msg.body("What is your location? (e.g Surulere, lagos)")
            return str(resp)
        elif "location" not in session:
            session["location"] = incoming_msg
            msg.body("Please describe the emergency")
            return str(resp)
        elif "emergency" not in session:
            session["emergency"] = incoming_msg
            sheet.insert_row([session["name"], session["phone number"], session["emergency_type"], session["location"], session["emergency"]], 2)
            session.pop("new query")
            session.pop("name")
            session.pop("phone number")
            session.pop("location")
            session.pop("emergency")
            session.pop("emergency_type")
            session.pop("tracker")
            msg.body("Thank you for filling the required information. It will be reviewed in some minutes and our team will attend to it based on priority.")
            return str(resp)

if __name__ == "__main__":
    app.run()
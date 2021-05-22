import flask
from flask import request
from flask_apscheduler import APScheduler
import requests
import datetime
import os
import ast


_global_state_id = 16
_global_district_id = 294
_global_age = 18
_global_dose_number = 1

COWIN_HOST = "https://cdn-api.co-vin.in/api"
INVALID_REQUEST_TEMPLATE = "Invalid {key} provided. {key} should be in lowercase and should not contain whitespaces."
RESPONSE_TEMPLATE = "Successfully updated parameters: " \
                    "StateID - {state}: DistrictID - {district}: Age - {age}: Dose Number - {dose}"

app = flask.Flask(__name__)


@app.route('/v1/vaccine-availability', methods=['PUT'])
def get_vaccine_availability():
    ref_state = request.args.get('state')
    ref_district = request.args.get('district')
    ref_age = request.args.get('age')
    ref_dose_number = request.args.get('dose')

    global _global_age
    _global_age = ref_age
    global _global_dose_number
    _global_dose_number = ref_dose_number

    state_id = get_state_id(ref_state)
    if state_id is None:
        return INVALID_REQUEST_TEMPLATE.format(key="State"), 400

    global _global_state_id
    _global_state_id = state_id

    district_id = get_district_id(state_id, ref_district)
    if district_id is None:
        return INVALID_REQUEST_TEMPLATE.format(key="District"), 400

    global _global_district_id
    _global_district_id = district_id

    return RESPONSE_TEMPLATE.format(
        state=_global_state_id, district=_global_district_id, age=_global_age, dose=_global_dose_number), 200


def get_state_id(ref_state):
    states_raw = requests.get(COWIN_HOST + '/v2/admin/location/states',
                              headers={"Accept": "application/json", "User-Agent": "PostmanRuntime/7.26.8"}).text
    states = ast.literal_eval(states_raw)
    for state in states["states"]:
        if ref_state == state["state_name"].replace(" ", "").lower():
            return state["state_id"]
    return None


def get_district_id(state_id, ref_district):
    districts_raw = requests.get(COWIN_HOST + '/v2/admin/location/districts/' + str(state_id),
                                 headers={"Accept": "application/json", "User-Agent": "PostmanRuntime/7.26.8"}).text
    districts = ast.literal_eval(districts_raw)
    for district in districts['districts']:
        if ref_district == district["district_name"].replace(" ", "").lower():
            return district["district_id"]
    return None


def find_appointments():
    global _global_district_id
    global _global_dose_number
    global _global_age

    print("Fetching vaccination slot details: District: {}, Age: {}, Dose: {}".format(_global_district_id, _global_age, _global_dose_number))
    centers_raw = requests.get(COWIN_HOST + '/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(_global_district_id) +
                           '&date=' + datetime.datetime.now().strftime("%d-%m-%Y"),
                               headers={"Accept": "application/json", "User-Agent": "PostmanRuntime/7.26.8"}).text
    centers = ast.literal_eval(centers_raw)
    for center in centers["centers"]:
        if "sessions" in center:
            for session in center["sessions"]:
                if session["min_age_limit"] <= int(_global_age) and session["available_capacity_dose{}".format(_global_dose_number)] > 0:
                    print("Slot available!")
                    print("Center: " + center["name"])
                    print(", ".join(
                        [center["address"], center["district_name"], center["state_name"], center["pincode"]]))
                    print("Age: " + session["min_age_limit"])
                    print("Available dose capacity: Dose {}:".format(_global_dose_number) + session[
                        "available_capacity_dose{}".format(_global_dose_number)])
                    print("____")
                    beep()


def beep():
    os.system('say "Vaccine slot is available. Book now!"')


class Config(object):
    JOBS = [
        {
            'id': 'Appointment job',
            'func': 'CovidVaccineCustomApi:find_appointments',
            'trigger': 'interval',
            'seconds': 5
        }
    ]
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
app.run()

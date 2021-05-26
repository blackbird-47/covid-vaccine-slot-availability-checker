# COVID-19 Vaccine Slot Availability Checker
[![CodeFactor](https://www.codefactor.io/repository/github/blackbird-47/covid-vaccine-slot-availability-checker/badge)](https://www.codefactor.io/repository/github/blackbird-47/covid-vaccine-slot-availability-checker)

### Regularly checks on vaccine availability via CoWin public APIs

Built on Python(3.8) Flask framework.

#### This application has two components
1. An API that takes in parameters from the user to configure vaccine slot location/age/dose details on the application.
2. The application picks the changes requested by the API in real time and calls CoWin public API to fetch COVID-19 vaccine appointment availability details.

#### Running on Local
1. Clone the repository to your local.
```bash
git clone https://github.com/blackbird-47/covid-vaccine-slot-availability-checker.git
```
2. Change the working directory to ```covid-vaccine-slot-availability-checker```.
```bash
cd covid-vaccine-slot-availability-checker
```
3. Use ```pip``` to install necessary packages through requirements.txt. Packages that will be installed - ```flask```, ```flask_apscheduler```, ```requests```
```bash
pip3 install -r requirements.txt 
```
4. Run the script.
```bash
python3 CovidVaccineCustomApi.py
```

#### Notes
1. On application startup, default behaviour of the app is to fetch KA-BBMP slots for 18 age and 1st dose. This can be updated by an API that the application has exposed - ```PUT http://127.0.0.1:5000/v1/vaccination-parameters?state=karnataka&district=bbmp&dose=1&age=25```
2. The app calls cowin appointment endpoint every 5 seconds (configurable).
3. When a slot is available, an output will be printed in the stdout stream. A voice message will also start to alert the user.
4. This application was developed and tested on MacOS 10.15. It should work on Linux distros except for the text-to-speech command which will need to be updated.
5. Supported parameters that can be configured from the API are - **state, district, age, dose**.

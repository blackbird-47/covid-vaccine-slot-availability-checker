# COVID-19 Vaccine Slot Availability Checker
### Regularly checks on vaccine availability via CoWin public APIs

Built on Python(3.8) Flask framework.

#### This application has two components
1. An API that takes in parameters from the user to configure vaccine slot location/age/dose details on the application.
2. The application picks the changes requested by the API in real time and calls CoWin public API to fetch COVID-19 vaccine appointment availability details.

#### Running on Local
1. Clone the repository to your local.
2. Change the working directory to ```vaccine-slot-availability-checker```
3. Use ```pip``` to install necessary packages through requirements.txt. Packages that will be installed - ```flask```, ```flask_apscheduler```, ```requests```
4. Run the script - ```python CovidVaccineCustomApi.py```


#### Notes
1. On application startup, default behaviour of the app is to fetch KA-BBMP slots for 18 age and 1st dose. This can be updated an API that the application has exposed - ```PUT http://127.0.0.1:5000/v1/vaccine-availability?state=karnataka&district=bbmp&dose=1&age=25```
2. The app calls cowin appointment endpoint every 5 seconds (configurable).
3. When a slot is available, an output will be printed in the stdout stream. A voice message will also start to alert the user.
4. This application was developed and tested on MacOS 10.15. It should work on Linux except for the text-to-speech command which is specific to MacOS.
5. Supported parameters that can be configured from the API are - **state, district, age, dose**.
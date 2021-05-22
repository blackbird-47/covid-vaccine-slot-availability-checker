# COVID-19 Vaccine Slot Availability Checker
### Regularly checks on vaccine availability via CoWin public APIs

Built with Python Flask framework.

#### This application has two components
1. An API that takes in parameters from the user to configure vaccine slot location/age/dose details on the application.
2. The application picks the changes requested by the API in real time and calls CoWin public API to fetch COVID-19 vaccine appointment availability details.

#### Running on Local
1. Clone the repository to your local.
2. Change the working directory ```cd vaccine-slot-availability-checker```
3. Use ```pip``` to install necessary packages - ```flask```, ```flask_apscheduler```, ```requests```
4. Run the file - ```python CovidVaccineCustomApi.py```


#### Notes
1. When the web server is deployed, an API call is needed the first time to set the location/age/dose configuration in the application.
2. The app calls cowin appointment endpoint every 5 seconds (configurable).
3. When a slot is available, an output will be printed in the stdout stream. A voice message will also start to alert the user.
4. This application was developed and tested on MacOS 10.15. It should work on Linux except for the text-to-speech command which is specific to MacOS.
5. Supported parameters that can be configured from the API are - **state, district, age, dose**. State and district query params are mandatory.
# COVID19-Dashboard

This is a repository that contains the files for a COVID19 Dashboard that is deloyed on Heroku. Find the dashboard here:
https://covid19-dashboard1.herokuapp.com

Data sources:
 - John Hopkins University (JHU)
 - Conference of State Bank Supervisors (CSBS)
 - New York Times (NYT)

## Installation

The required modules are outlined below:
```
dash_core_components
dash_html_components
dash
dash.dependencies
pandas
plotly.graph_objects
```

## What it should look like...

<img width="1477" alt="Screenshot 2020-06-11 at 09 52 45" src="https://user-images.githubusercontent.com/49324530/84365766-d6dff880-abc9-11ea-9145-bb0baa186be4.png">

<img width="1477" alt="Screenshot 2020-06-11 at 09 52 53" src="https://user-images.githubusercontent.com/49324530/84365813-e8290500-abc9-11ea-8960-54fd5e74d366.png">

## Next Steps...

Allow the text box to take different inputs. Currently it takes inputs of countries that start with a capital letter and are formatted correctly (e.g. United Kingdom, rather than UK or united kingdom).

Collate China data. Currently data surrounding China is distributed in its regions (e.g. Beijing ).


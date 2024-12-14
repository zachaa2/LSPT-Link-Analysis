# Source code for the Link Analysis module

To startup the app

```uvicorn api:app --host lspt-link-analysis.cs.rpi.edu --port 1200```


To test if the app is up and can be accessed, either use Postman API or curl it using:

```curl -i -X GET http://lspt-link-analysis.cs.rpi.edu:1200/ranking/www.google.com```
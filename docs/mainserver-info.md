### Main server, front-end


* **Installation**  

Specify a base URL for the server ($URL_BASE) without http:// or https://, if not provided, it will be taken as "0.0.0.0" . This change is **required** in order to
avoid connection errors with InfluxDB.    
Specify InfluxDB, MongoDB credentials, defaults are shown in the *.env* file 


By default, the API server is run using 4 threads via gunicorn, but this setting can be changed by the $GTH variable.


```bash
cd ./parser-server
URL_BASE=example.com GTH=6 docker-compose up -d
```

*Note*: The numpy installation may take longer than the other packages. This is especially the case in systems with lower specifications.





* **Connecting a Grafana instance**

[Grafana](http://docs.grafana.org/) is a popular data visualization platform. Although not required at all, it can be used to observe the data entered into InfluxDB.


Grafana will be available at port 3000 of the same server.


To install grafana:

```bash
docker run -d -p 3000:3000 grafana/grafana
```

To login, go to *http://mygrafana.url:3000*. Starting username and password are both *admin*.
Add dashboards to observe the data:


```sql

# Correct API job submission
SELECT * FROM "api_jobs"."autogen"."api_job_submission"

# Failed logins
SELECT * FROM "failed_login"."autogen"."bad_credentials"
# Failed node requests
SELECT * FROM "failed_login"."autogen"."bad_node_requests"
```




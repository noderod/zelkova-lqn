### Main server, front-end


* **Installation**  

Specify a base URL for the server ($URL_BASE) without http:// or https://, if not provided, it will be taken as "0.0.0.0" .  
Specify a Redis password ($REDIS_AUTH), if not provided, it will be taken as "test".
Specify InfluxDB credentials TODO


By default, the API server is run using 4 threads via gunicorn, but this setting can be changed by the $GTH variable.


```bash
cd ./parser-server
URL_BASE=example.com REDIS_AUTH=pass1 GTH=6 docker-compose up -d





```




* **Connecting a Grafana instance**

[Grafana]() is a popular data visualization platform. Although not required at all, it can be used to observe the data entered into InfluxDB.

```bash




```



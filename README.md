# health-check-docker-crontab-dynaconf-logging

Application health check with docker, crontab with python library - dynaconf and logging

#### Docker build image
docker build --rm -t health_checker:latest .

#### Docker Run Command
docker run --rm -it -d -v $HOME/health_checker/logs:/app/logs -v $HOME/health_checker/config:/app --env DOCKER_HOST_IP=<Docker_host or Container IP> --name health_checker health_checker:latest

  ` -v $HOME/health_checker/logs:/app/logs  - volume mount path for redirecting the log files from docker container to docker hosted machine
     where first part before : is path from host machine and part after is path for logs in docker container running.
  `
  
  ` -v $HOME/health_checker/configs:/app  - volume mount path for redirecting the files from docker container to docker hosted machine
     where first part before : is path from host machine and part after is path in docker container running. $HOME expansion is 
     /home/{configured_linux_user}/health_checker/config. Inside of this path, .env would be available.
  `
  
  `
    Under the path - /home/{configured_linux_user}/health_checker/configs of host machine, actual values of environment specific host URLs are mapped.
    For example, EXAMPLE_A_API_HOST=http://localhost:8082 would be mapped in .env
  `

#### Notes to Remember::
1. Currently http requests for the environment **specific URLs are crawled for every 2 minutes**. This can be configurable by changing in **crontab.txt**

   `*/2 * * * * python /app/http_request_executor.py`
   `*/2 * * * * python /app/component_health_check.py`

2. **DOCKER_HOST_IP** value mentioned in **docker run --env** is the docker host ip or docker container ip.

3. **http_request_executor.py** file holds methods related with HTTP Request and Response crawling.

4. **component_health_check.py** file holds methods related with Component Health Check(like S3, SSM, DynamoDB, etc) and Response crawling.

5. Add the python related library in requirements.txt and while building docker, libraries are automatically installed while building your image.

6. **entrypoint.sh** is the entry for starting the docker run and to run the crontab job in background.

7. Generalized host urls, AWS and other other components information are mentioned in **.env**. To run the docker container for specific environment(say dev), 
   then mount the path using docker run using -v flag.
   
8. Python logging mechanism has been implemented for better debugging and troubleshooting. Under running container , log path is /app/logs and mounted volume 
   in host machine is **$HOME/health_checker/logs**.

9. Under **$HOME/health_checker/logs**(assumption - container should be up and running), **3 logs** would be generated. 

10. **cron.log** is to view the status of crontab job ran and sometimes it would hold the stdout/stderr clips if our program didn't ran as per expectations.

11. **component_health_check_datetime.log** would hold the log records specific to component health checks.

12. **http_requester_datetime.log** would hold the log records specific to HTTP/HTTPS REST API calls as well as web application launch URL health checks.

#### Notes to Remember while creating/updating the environment specific URls for Health Check::
1. We are using dynaconf python library for interacting and getting the environment specific variables from .env.

2. For our REST API or WEB APP URI Health Check validation, our script needs URLs in a set of list or dict to perform bulk execution. To accommodate that, dynaconf python library
   provides type casting and lazy values fetching operations. See the below example for reference(https://www.dynaconf.com/envvars/#type-casting-and-lazy-values),
   
   ` If you want to add any new REST API URI, then append the DYNACONF_REST_API_DICTS's dict available`
   
   ` DYNACONF_REST_API_DICTS='@json {
                "EXAMPLE_A_API_HOST": "http://localhost:8082",
                "EXAMPLE_B_API_HOST": "http://localhost:8083",
                "NEW_KEY": "NEW_VALUE"
                }' `
                
   ` If you want to add any new WEB APP URI, then append the DYNACONF_WEB_APPLICATION_URI_DICTS's dict available`
    
   ` DYNACONF_WEB_APPLICATION_URI_DICTS='@json {
                "EXAMPLE_WEB_APP_URI": "http://localhost:8082",
                "NEW_KEY": "NEW_VALUE"
                }' `

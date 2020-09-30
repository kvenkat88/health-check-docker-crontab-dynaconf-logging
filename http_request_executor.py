import logging
from logger import setup_logger
import requests
import json
import os
from datetime import datetime
from dynaconf import settings
#import asyncio,aiohttp

logger = setup_logger('http_request_logger',level=logging.DEBUG)

def parse_env_file_form_dict(env='base'):
    """
    Load the {env}.env file and provide it it as dict
    :param env: env as string. Example values are dev, local, prod, etc
    :return: vars_dict as dict
    """
    cur_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(cur_path, r"./config/{}.env".format(env))

    with open(file_path, 'r') as fh:
        logger.debug("Env file fetched is {}.env".format(env))
        vars_dict = dict(
            tuple(line.split('='))
            for line in fh.readlines() if not line.startswith('#')
        )
    # print("Parsed dict values are {}".format(vars_dict))
    return vars_dict

def url_framer_or_formatter(url, host_name_or_ip):
    """
    URL framer or formatter method to frame the url based upon the host_name or host_ip provided
    :param url: url as string
    :param host_name_or_ip: host_name_or_ip as string
    :return: Url_framed . Eg: from http://localhost:5678 to http://10.1.2.3:5678
    """
    url_framed = "None"

    if "http" in url or "https" in url:
        if ":" in url.split("//")[1]:
            url_framed = url.split("//")[0] +"//" + host_name_or_ip + ":" + url.split("//")[1].split(":")[1]
        else:
            logger.debug("Port is not available in the url provided(i.e url with hostname mapped) - {}, so using the same url".format(url))
            url_framed = url
    else:
        logger.debug("Please provide the valid url with schema like http/https for - {}".format(url))

    return url_framed

# Simple Version using Python Requests Library
def common_http_validator(method=None,url=None,data=None,header=None):
    """
    Method to perform HTTP operations and response fetching
    :param method: Manifest URL/URI supported http request method(GET,PUT,POST,DELETE,HEAD,OPTIONS,PATCH)
    :param url: Manifest URL/URI of the asset/tv entity requested
    :param data: Applicable only POST,PUT,PATCH http method API's
    :param header: http request/response headers pass if any
    :return: http_status_code,response_content,error_message if available
    """
    status_code = 500
    error_msg = None
    response_data = None

    try:
        req = requests.request(method=method,url=url,data=data,headers=header)
        # print req.request.method #Getting the method

    except (requests.RequestException,requests.HTTPError,requests.ConnectionError,requests.Timeout) as e:
        error_msg = 'Connection/Timeout/General Exception: {}'.format(e)

    except Exception as e:
        error_msg = 'Connection/Timeout/General Exception: {}'.format(e)

    else:
        status_code = req.status_code
        response_data = req.content

    return status_code, response_data, error_msg

def response_validator(url_dict, host_name_ip, api_endpoint):
    """
    Common method to valid the HTTP response fetched with url_framer_or_formatter applied
    :param url_dict: url_dict as dict
    :param host_name_or_ip: host_name_or_ip as string
    :param api_endpoint: /healthcheck as string
    :return: NA
    """
    for key, value in url_dict.items():
        url_framed = url_framer_or_formatter(value.strip(),host_name_ip) + api_endpoint
        logger.debug("{} Executing request for {}::{} {}".format("#" * 20, key,url_framed, "#" * 20))
        status_code, response_data, error_msg = common_http_validator(method='GET', url=url_framed)
        if status_code == 200:
            logger.debug("{} ok status obtained with response message as {}".format(status_code,json.loads(response_data)['status']))
        else:
            logger.debug("{} status with response as {} and exception message as {}".format(status_code,response_data,error_msg))

        logger.debug("{} Request execution completed for {}::{} {}".format("#" * 20, key,url_framed, "#" * 20))

# response_validator(parse_env_file_form_dict("dev"),"localhost123", "/healthz")

if __name__ == '__main__':
    """
        1. To exceute the script, issue the below mentioned in command prompt or terminal, 
           Example1 :: python http_request_executor.py 10.1.2.3 -- to run in local
           Example1 :: python http_request_executor.py os.environ["DOCKER_HOST_IP"] -- from docker env and os.environ["DOCKER_HOST_IP"] will have host name info
    """
    try:
        host_info_from_env = os.environ["DOCKER_HOST_IP"]
        logger.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Crawling Start Time in UTC - {} $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$".format(datetime.strftime(datetime.utcnow(), '%m-%d-%Y-T%H:%M:%S')))
        response_validator(settings.REST_API_DICTS, str(host_info_from_env), str("/healthz"))
        logger.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Crawling Stop Time in UTC - {} $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$".format(datetime.strftime(datetime.utcnow(), '%m-%d-%Y-T%H:%M:%S')))
    except Exception as e:
        logger.exception("Uncaught exception occurred")









































## Using asyncio and aiohttp

# async def post_request_fetch_response(url_available):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url=url_available) as response:
#             if response.status == 200:
#                 return response.status, await response.text()
#             else:
#                 return response.status, None

# async def main(url_dict):
#     # tasks = []
#     for key, value in url_dict.items():
#         print("{} Executing request for {} {}".format("#" * 70, key, "#" * 70))
#         status, resp = await post_request_fetch_response(value)
#         print(status, resp)

        ## Below set of code is capture the output/responses as list of tasks executed. Responses would be available at the end only.
        # task = asyncio.ensure_future(post_request_fetch_response(url))
        # tasks.append(task)
        # await asyncio.sleep(0.5)

    # responses = await asyncio.gather(*tasks)
    # print(responses)

# url_dict_items = parse_env_file_form_dict("dev")
#
# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(main(url_dict_items))
# loop.run_until_complete(future)
# print("Pending tasks at exit: %s" % asyncio.all_tasks(loop))
# loop.close()

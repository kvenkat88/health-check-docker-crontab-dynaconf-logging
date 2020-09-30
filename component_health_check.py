import logging
from logger import setup_logger
import redis,certifi
import boto3
from dynaconf import settings
# import traceback, sys

logger = setup_logger('component_health_check_logger',level=logging.DEBUG)

def check_redis_connection():
    """
    Check the Redis connection availability by using /ping api
    :param host: host as string
    :param port: port as int
    :param db: db as int. Redis databases are identified by an integer index, there is no database name
                     and By default there are 16 databases, indexed from 0 to 15.
    :param password: password as string
    :param ssl: ssl as bool
    :return: result string with value
    """
    result = None
    try:
        conn = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB_INDEX,
            password=settings.REDIS_PASSWORD,
            ssl=settings.REDIS_TLS,
            ssl_ca_certs=certifi.where())

        result = conn.ping()
    except Exception as e:
        logger.error('Exception Message:', e)
        result = bool(False)
        logger.exception("Uncaught Exception")
        # exit('Failed to connect, terminating.')

    if result == True:
        logger.debug("conn.ping() response for {} is {}".format(settings.REDIS_HOST,result))
        logger.debug("Ok from redis host - {}".format(settings.REDIS_HOST))
    else:
        logger.debug("conn.ping() response for {} is {}".format(settings.REDIS_HOST, result))
        logger.debug("Failed to connect from redis host - {}".format(settings.REDIS_HOST))

def connect_validate_aws_s3_component_health_check():
    """
    Validate the AWS S3 component health check and return the status
    :param aws_access_key_id: S3_AWS_ACCESS_KEY_ID
    :param aws_secret_access_key: S3_AWS_SECRET_ACCESS_KEY
    :param region_name: S3_AWS_DEFAULT_REGION
    :return: result string with value
    """
    final_status = None

    comp_conn = boto3.client('s3',aws_access_key_id=settings.S3_AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.S3_AWS_SECRET_ACCESS_KEY,
                          region_name=settings.S3_AWS_DEFAULT_REGION)

    try:
        response = comp_conn.list_buckets()

        if (len(response) != 0) and (response is not None):
            if response['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Buckets' in response:

                if response['ResponseMetadata']['HTTPStatusCode'] == 200 and len(response['Buckets']) != 0:
                    final_status = "AWS S3 Health is Up and Running and healthcheck client status code is {} and length of the buckets available is not zero i.e {}".format(response['ResponseMetadata']['HTTPStatusCode'],
                                                                                                                                                                  len(response['Buckets']))
                if response['ResponseMetadata']['HTTPStatusCode'] == 200 and len(response['Buckets']) == 0:
                    final_status = "AWS S3 Health is Up and Running and healthcheck client status code is {} and length of the buckets available is zero".format(response['ResponseMetadata']['HTTPStatusCode'])

                if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    final_status = "AWS S3 Health is not Running and healthcheck client status code is {}".format(response['ResponseMetadata']['HTTPStatusCode'])
                    logger.debug("Response Fetched is \n {}".format(response))
            else:
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    final_status = "AWS S3 Health is Up and Running and healthcheck client status code is {} and bucket list is not available in response".format(response['ResponseMetadata']['HTTPStatusCode'])
                    logger.debug("Response Fetched is \n {}".format(response))

                if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    final_status = "AWS S3 Health is not Running and healthcheck client status code is {}".format(response['ResponseMetadata']['HTTPStatusCode'])
                    logger.debug("Response Fetched is \n {}".format(response))
        else:
            final_status = "AWS S3 that you want to healthcheck is not running or issue fetching the client response.Please have a look!!!"

    except (comp_conn.exceptions.ClientError,Exception) as e:
        logger.error('Exception Message:', e)
        final_status = str(e)
        # Printing full stack trace of exception
        # print(traceback.print_exc())
        logger.exception("Uncaught Exception")
        # logger.error("uncaught exception: %s", traceback.format_exc())

    logger.debug(final_status)

def connect_validate_aws_dynamodb_component_health_check():
    """
    Validate the AWS DynamoDB component health check and return the status
    :param aws_access_key_id: DYNAMODB_AWS_ACCESS_KEY_ID
    :param aws_secret_access_key: DYNAMODB_AWS_SECRET_ACCESS_KEY
    :param region_name: DYNAMODB_AWS_DEFAULT_REGION
    :return: result string with value
    """
    final_status = None

    comp_conn = boto3.client('dynamodb',aws_access_key_id=settings.DYNAMODB_AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.DYNAMODB_AWS_SECRET_ACCESS_KEY,
                          region_name=settings.DYNAMODB_AWS_DEFAULT_REGION)

    try:
        response = comp_conn.list_tables()['TableNames']

        if (len(response) != 0) and (response is not None):
            final_status = "AWS DynanoDB component service is Up and Running and length of the dynamodb table is not zero i.e {}".format(len(response))
        else:
            final_status = "AWS DynanoDB component service is running and length might be zero or tablenames might not be fetched. Please Check!!!"
            logger.debug("Response Fetched is \n {}".format(response))

    except (comp_conn.exceptions.ClientError,Exception) as e:
        logger.error('Exception Message:', e)
        final_status = str(e)
        # Printing full stack trace of exception
        logger.exception("Uncaught Exception")

    logger.debug(final_status)


def connect_validate_aws_ssm_component_health_check():
    """
    Validate the AWS SSM component health check and return the status
    :param aws_access_key_id: SSM_AWS_ACCESS_KEY_ID
    :param aws_secret_access_key: SSM_AWS_SECRET_ACCESS_KEY
    :param region_name: SSM_AWS_DEFAULT_REGION
    :return: result string with value
    """
    final_status = None

    comp_conn = boto3.client('ssm',aws_access_key_id=settings.SSM_AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.SSM_AWS_SECRET_ACCESS_KEY,
                          region_name=settings.SSM_AWS_DEFAULT_REGION)

    try:
        # Returns all Systems Manager (SSM) documents in the current AWS account and Region. You can limit the results of this request by using a filter.
        response = comp_conn.list_documents()
        if (len(response) != 0) and (response is not None):
            if response['ResponseMetadata']['HTTPStatusCode'] == 200 and 'DocumentIdentifiers' in response:
                if response['ResponseMetadata']['HTTPStatusCode'] == 200 and len(response['DocumentIdentifiers']) != 0:
                    final_status = "AWS SSM Agent is Up and Running and healthcheck client status code is {} and length of the DocumentIdentifiers list available is not zero i.e {}".format(response['ResponseMetadata']['HTTPStatusCode'],
                                                                                                                                                             len(response['DocumentIdentifiers']))

                if response['ResponseMetadata']['HTTPStatusCode'] == 200 and len(response['DocumentIdentifiers']) == 0:
                    final_status = "AWS SSM Agent is Up and Running and healthcheck client status code is {} and length of the DocumentIdentifiers list available is zero".format(response['ResponseMetadata']['HTTPStatusCode'])

                if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    final_status = "AWS SSM Agent is not Running and healthcheck client status code is {}".format(response['ResponseMetadata']['HTTPStatusCode'])
                    logger.debug("Response Fetched is \n {}".format(response))
            else:
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    final_status = "AWS SSM Agent is Up and Running and healthcheck client status code is {} and DocumentIdentifiers list is not available in response".format(response['ResponseMetadata']['HTTPStatusCode'])
                    logger.debug("Response Fetched is \n {}".format(response))

                if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    final_status = "AWS SSM Agent is not Running and healthcheck client status code is {}".format(response['ResponseMetadata']['HTTPStatusCode'])
                    logger.debug("Response Fetched is \n {}".format(response))

        else:
            final_status = "AWS SSM Agent that you want to healthcheck is not running or issue fetching the client response.Please have a look!!!"

    except (comp_conn.exceptions.ClientError,Exception) as e:
        logger.error('Exception Message:', e)
        final_status = str(e)
        # Printing full stack trace of exception
        logger.exception("Uncaught Exception")

    logger.debug(final_status)

if __name__ == '__main__':
    check_redis_connection() # Redis Health
    connect_validate_aws_s3_component_health_check() # AWS S3 Health
    connect_validate_aws_dynamodb_component_health_check() # AWS DynamoDB Health
    connect_validate_aws_ssm_component_health_check() # AWS SSM Health
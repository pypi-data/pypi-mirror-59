import larry.s3 as s3
import larry.mturk as mturk
import larry.sqs as sqs
import larry.sts as sts
import larry.sagemaker as sagemaker
import boto3
import larry.utils as utils
import larry.types as types
import json

__version__ = "0.1.4"


def _propagate_session():
    s3.set_session(boto_session=__session)
    mturk.set_session(boto_session=__session)
    sqs.set_session(boto_session=__session)
    sts.set_session(boto_session=__session)
    sagemaker.set_session(boto_session=__session)


# A local instance of the boto3 session to use
__session = boto3.session.Session()
_propagate_session()


def session():
    global __session
    if __session is None:
        __session = boto3.session.Session()
    return __session


def set_session(aws_access_key_id=None,
                aws_secret_access_key=None,
                aws_session_token=None,
                region_name=None,
                profile_name=None,
                boto_session=None):
    """
    Sets the boto3 session for this module to use a specified configuration state.
    :param aws_access_key_id: AWS access key ID
    :param aws_secret_access_key: AWS secret access key
    :param aws_session_token: AWS temporary session token
    :param region_name: Default region when creating new connections
    :param profile_name: The name of a profile to use
    :param boto_session: An existing session to use
    :return: None
    """
    global __session
    __session = boto_session if boto_session is not None else boto3.session.Session(**utils.copy_non_null_keys(locals()))
    _propagate_session()


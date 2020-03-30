# -*- coding: utf-8 -*-
from utilities import logger


def extract_image_uuid_from_image_list(image_list_content:dict, image_name):
    """
    根据image_name从image list的内容中提取uuid
    :param image_list_content: dict
    :param image_name: str
    :return:
    """
    for image_info in image_list_content['data']:
        if image_info['name'] == image_name:
            return image_info['uuid']
    logger.log_debug('Did not find image uuid of image "{}"'.format(image_name))



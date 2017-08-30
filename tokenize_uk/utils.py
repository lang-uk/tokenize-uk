#!env python
# -*- coding: utf-8 -*-
import re


def replace_non_breaking_space(str):
    """
    Replaces non breaking space (ASCII 160, Unicode 0x00A0) with usual space (ASCII 32) to prevent tokenization errors

    :param string: Text
    :type string: str or unicode
    :return: Text
    :rtype: str or unicode
    """
    strs = re.split('\u00A0', str, re.U)
    return ' '.join(strs)

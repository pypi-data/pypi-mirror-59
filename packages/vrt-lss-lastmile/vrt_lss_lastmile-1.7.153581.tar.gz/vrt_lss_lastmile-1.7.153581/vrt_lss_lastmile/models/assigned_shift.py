# coding: utf-8

"""
    VeeRoute.LSS Lastmile

    Программный интерфейс для универсального планирования задач последней мили  # noqa: E501

    OpenAPI spec version: 1.7.153581
    Contact: support@veeroute.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class AssignedShift(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'shift_key': 'str',
        'shift_time': 'TimeWindow'
    }

    attribute_map = {
        'shift_key': 'shift_key',
        'shift_time': 'shift_time'
    }

    def __init__(self, shift_key=None, shift_time=None):  # noqa: E501
        """AssignedShift - a model defined in Swagger"""  # noqa: E501
        self._shift_key = None
        self._shift_time = None
        self.discriminator = None
        self.shift_key = shift_key
        self.shift_time = shift_time

    @property
    def shift_key(self):
        """Gets the shift_key of this AssignedShift.  # noqa: E501

        Ключ смены исполнителя или транспорта  # noqa: E501

        :return: The shift_key of this AssignedShift.  # noqa: E501
        :rtype: str
        """
        return self._shift_key

    @shift_key.setter
    def shift_key(self, shift_key):
        """Sets the shift_key of this AssignedShift.

        Ключ смены исполнителя или транспорта  # noqa: E501

        :param shift_key: The shift_key of this AssignedShift.  # noqa: E501
        :type: str
        """
        if shift_key is None:
            raise ValueError("Invalid value for `shift_key`, must not be `None`")  # noqa: E501

        self._shift_key = shift_key

    @property
    def shift_time(self):
        """Gets the shift_time of this AssignedShift.  # noqa: E501


        :return: The shift_time of this AssignedShift.  # noqa: E501
        :rtype: TimeWindow
        """
        return self._shift_time

    @shift_time.setter
    def shift_time(self, shift_time):
        """Sets the shift_time of this AssignedShift.


        :param shift_time: The shift_time of this AssignedShift.  # noqa: E501
        :type: TimeWindow
        """
        if shift_time is None:
            raise ValueError("Invalid value for `shift_time`, must not be `None`")  # noqa: E501

        self._shift_time = shift_time

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(AssignedShift, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AssignedShift):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

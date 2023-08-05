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


class PossibleEvent(object):
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
        'location_key': 'str',
        'duration': 'int',
        'reward': 'float',
        'time_window': 'TimeWindow'
    }

    attribute_map = {
        'location_key': 'location_key',
        'duration': 'duration',
        'reward': 'reward',
        'time_window': 'time_window'
    }

    def __init__(self, location_key=None, duration=None, reward=None, time_window=None):  # noqa: E501
        """PossibleEvent - a model defined in Swagger"""  # noqa: E501
        self._location_key = None
        self._duration = None
        self._reward = None
        self._time_window = None
        self.discriminator = None
        self.location_key = location_key
        self.duration = duration
        if reward is not None:
            self.reward = reward
        self.time_window = time_window

    @property
    def location_key(self):
        """Gets the location_key of this PossibleEvent.  # noqa: E501

        Ключ локации, в которой возможно данное действие  # noqa: E501

        :return: The location_key of this PossibleEvent.  # noqa: E501
        :rtype: str
        """
        return self._location_key

    @location_key.setter
    def location_key(self, location_key):
        """Sets the location_key of this PossibleEvent.

        Ключ локации, в которой возможно данное действие  # noqa: E501

        :param location_key: The location_key of this PossibleEvent.  # noqa: E501
        :type: str
        """
        if location_key is None:
            raise ValueError("Invalid value for `location_key`, must not be `None`")  # noqa: E501

        self._location_key = location_key

    @property
    def duration(self):
        """Gets the duration of this PossibleEvent.  # noqa: E501

        Время выполнения заявки, минут  # noqa: E501

        :return: The duration of this PossibleEvent.  # noqa: E501
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this PossibleEvent.

        Время выполнения заявки, минут  # noqa: E501

        :param duration: The duration of this PossibleEvent.  # noqa: E501
        :type: int
        """
        if duration is None:
            raise ValueError("Invalid value for `duration`, must not be `None`")  # noqa: E501

        self._duration = duration

    @property
    def reward(self):
        """Gets the reward of this PossibleEvent.  # noqa: E501

        Вознаграждение за выполнение данного заказа  # noqa: E501

        :return: The reward of this PossibleEvent.  # noqa: E501
        :rtype: float
        """
        return self._reward

    @reward.setter
    def reward(self, reward):
        """Sets the reward of this PossibleEvent.

        Вознаграждение за выполнение данного заказа  # noqa: E501

        :param reward: The reward of this PossibleEvent.  # noqa: E501
        :type: float
        """

        self._reward = reward

    @property
    def time_window(self):
        """Gets the time_window of this PossibleEvent.  # noqa: E501


        :return: The time_window of this PossibleEvent.  # noqa: E501
        :rtype: TimeWindow
        """
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        """Sets the time_window of this PossibleEvent.


        :param time_window: The time_window of this PossibleEvent.  # noqa: E501
        :type: TimeWindow
        """
        if time_window is None:
            raise ValueError("Invalid value for `time_window`, must not be `None`")  # noqa: E501

        self._time_window = time_window

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
        if issubclass(PossibleEvent, dict):
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
        if not isinstance(other, PossibleEvent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

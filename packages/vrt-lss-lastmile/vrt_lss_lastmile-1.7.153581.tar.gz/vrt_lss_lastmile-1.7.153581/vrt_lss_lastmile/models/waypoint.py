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


class Waypoint(object):
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
        'latitude': 'float',
        'longitude': 'float',
        'duration': 'int'
    }

    attribute_map = {
        'latitude': 'latitude',
        'longitude': 'longitude',
        'duration': 'duration'
    }

    def __init__(self, latitude=None, longitude=None, duration=0):  # noqa: E501
        """Waypoint - a model defined in Swagger"""  # noqa: E501
        self._latitude = None
        self._longitude = None
        self._duration = None
        self.discriminator = None
        self.latitude = latitude
        self.longitude = longitude
        if duration is not None:
            self.duration = duration

    @property
    def latitude(self):
        """Gets the latitude of this Waypoint.  # noqa: E501

        Широта в градусах  # noqa: E501

        :return: The latitude of this Waypoint.  # noqa: E501
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this Waypoint.

        Широта в градусах  # noqa: E501

        :param latitude: The latitude of this Waypoint.  # noqa: E501
        :type: float
        """
        if latitude is None:
            raise ValueError("Invalid value for `latitude`, must not be `None`")  # noqa: E501

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this Waypoint.  # noqa: E501

        Долгота в градусах  # noqa: E501

        :return: The longitude of this Waypoint.  # noqa: E501
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this Waypoint.

        Долгота в градусах  # noqa: E501

        :param longitude: The longitude of this Waypoint.  # noqa: E501
        :type: float
        """
        if longitude is None:
            raise ValueError("Invalid value for `longitude`, must not be `None`")  # noqa: E501

        self._longitude = longitude

    @property
    def duration(self):
        """Gets the duration of this Waypoint.  # noqa: E501

        Время остановки на точке в минутах  # noqa: E501

        :return: The duration of this Waypoint.  # noqa: E501
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this Waypoint.

        Время остановки на точке в минутах  # noqa: E501

        :param duration: The duration of this Waypoint.  # noqa: E501
        :type: int
        """

        self._duration = duration

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
        if issubclass(Waypoint, dict):
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
        if not isinstance(other, Waypoint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

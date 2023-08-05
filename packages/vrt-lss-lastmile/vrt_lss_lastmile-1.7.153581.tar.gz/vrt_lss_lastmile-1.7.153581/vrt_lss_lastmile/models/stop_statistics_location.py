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


class StopStatisticsLocation(object):
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
        'arrival_duration': 'int',
        'departure_duration': 'int'
    }

    attribute_map = {
        'latitude': 'latitude',
        'longitude': 'longitude',
        'arrival_duration': 'arrival_duration',
        'departure_duration': 'departure_duration'
    }

    def __init__(self, latitude=None, longitude=None, arrival_duration=0, departure_duration=0):  # noqa: E501
        """StopStatisticsLocation - a model defined in Swagger"""  # noqa: E501
        self._latitude = None
        self._longitude = None
        self._arrival_duration = None
        self._departure_duration = None
        self.discriminator = None
        self.latitude = latitude
        self.longitude = longitude
        if arrival_duration is not None:
            self.arrival_duration = arrival_duration
        if departure_duration is not None:
            self.departure_duration = departure_duration

    @property
    def latitude(self):
        """Gets the latitude of this StopStatisticsLocation.  # noqa: E501

        Широта в градусах  # noqa: E501

        :return: The latitude of this StopStatisticsLocation.  # noqa: E501
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this StopStatisticsLocation.

        Широта в градусах  # noqa: E501

        :param latitude: The latitude of this StopStatisticsLocation.  # noqa: E501
        :type: float
        """
        if latitude is None:
            raise ValueError("Invalid value for `latitude`, must not be `None`")  # noqa: E501

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this StopStatisticsLocation.  # noqa: E501

        Долгота в градусах  # noqa: E501

        :return: The longitude of this StopStatisticsLocation.  # noqa: E501
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this StopStatisticsLocation.

        Долгота в градусах  # noqa: E501

        :param longitude: The longitude of this StopStatisticsLocation.  # noqa: E501
        :type: float
        """
        if longitude is None:
            raise ValueError("Invalid value for `longitude`, must not be `None`")  # noqa: E501

        self._longitude = longitude

    @property
    def arrival_duration(self):
        """Gets the arrival_duration of this StopStatisticsLocation.  # noqa: E501

        Время на подъезд\\парковку на локации в минутах  # noqa: E501

        :return: The arrival_duration of this StopStatisticsLocation.  # noqa: E501
        :rtype: int
        """
        return self._arrival_duration

    @arrival_duration.setter
    def arrival_duration(self, arrival_duration):
        """Sets the arrival_duration of this StopStatisticsLocation.

        Время на подъезд\\парковку на локации в минутах  # noqa: E501

        :param arrival_duration: The arrival_duration of this StopStatisticsLocation.  # noqa: E501
        :type: int
        """

        self._arrival_duration = arrival_duration

    @property
    def departure_duration(self):
        """Gets the departure_duration of this StopStatisticsLocation.  # noqa: E501

        Время на отъезд от локации в минутах  # noqa: E501

        :return: The departure_duration of this StopStatisticsLocation.  # noqa: E501
        :rtype: int
        """
        return self._departure_duration

    @departure_duration.setter
    def departure_duration(self, departure_duration):
        """Sets the departure_duration of this StopStatisticsLocation.

        Время на отъезд от локации в минутах  # noqa: E501

        :param departure_duration: The departure_duration of this StopStatisticsLocation.  # noqa: E501
        :type: int
        """

        self._departure_duration = departure_duration

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
        if issubclass(StopStatisticsLocation, dict):
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
        if not isinstance(other, StopStatisticsLocation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

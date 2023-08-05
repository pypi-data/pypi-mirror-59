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


class Box(object):
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
        'key': 'str',
        'mass': 'float',
        'volume': 'float',
        'capacity_x': 'float',
        'capacity_y': 'float',
        'capacity_z': 'float',
        'width': 'float',
        'height': 'float',
        'length': 'float',
        'features': 'list[str]'
    }

    attribute_map = {
        'key': 'key',
        'mass': 'mass',
        'volume': 'volume',
        'capacity_x': 'capacity_x',
        'capacity_y': 'capacity_y',
        'capacity_z': 'capacity_z',
        'width': 'width',
        'height': 'height',
        'length': 'length',
        'features': 'features'
    }

    def __init__(self, key=None, mass=100, volume=100, capacity_x=0, capacity_y=0, capacity_z=0, width=0, height=0, length=0, features=None):  # noqa: E501
        """Box - a model defined in Swagger"""  # noqa: E501
        self._key = None
        self._mass = None
        self._volume = None
        self._capacity_x = None
        self._capacity_y = None
        self._capacity_z = None
        self._width = None
        self._height = None
        self._length = None
        self._features = None
        self.discriminator = None
        if key is not None:
            self.key = key
        self.mass = mass
        if volume is not None:
            self.volume = volume
        if capacity_x is not None:
            self.capacity_x = capacity_x
        if capacity_y is not None:
            self.capacity_y = capacity_y
        if capacity_z is not None:
            self.capacity_z = capacity_z
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if length is not None:
            self.length = length
        if features is not None:
            self.features = features

    @property
    def key(self):
        """Gets the key of this Box.  # noqa: E501

        Ключ отсека, уникальный идентификатор, используется для идентификации размещения грузов по отсекам  # noqa: E501

        :return: The key of this Box.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Box.

        Ключ отсека, уникальный идентификатор, используется для идентификации размещения грузов по отсекам  # noqa: E501

        :param key: The key of this Box.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def mass(self):
        """Gets the mass of this Box.  # noqa: E501

        Максимальная суммарная масса в килограммах  # noqa: E501

        :return: The mass of this Box.  # noqa: E501
        :rtype: float
        """
        return self._mass

    @mass.setter
    def mass(self, mass):
        """Sets the mass of this Box.

        Максимальная суммарная масса в килограммах  # noqa: E501

        :param mass: The mass of this Box.  # noqa: E501
        :type: float
        """
        if mass is None:
            raise ValueError("Invalid value for `mass`, must not be `None`")  # noqa: E501

        self._mass = mass

    @property
    def volume(self):
        """Gets the volume of this Box.  # noqa: E501

        Максимальный суммарная объем в кубических метрах  # noqa: E501

        :return: The volume of this Box.  # noqa: E501
        :rtype: float
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this Box.

        Максимальный суммарная объем в кубических метрах  # noqa: E501

        :param volume: The volume of this Box.  # noqa: E501
        :type: float
        """

        self._volume = volume

    @property
    def capacity_x(self):
        """Gets the capacity_x of this Box.  # noqa: E501

        Максимальная сумма параметра вместимости X в условных единицах  # noqa: E501

        :return: The capacity_x of this Box.  # noqa: E501
        :rtype: float
        """
        return self._capacity_x

    @capacity_x.setter
    def capacity_x(self, capacity_x):
        """Sets the capacity_x of this Box.

        Максимальная сумма параметра вместимости X в условных единицах  # noqa: E501

        :param capacity_x: The capacity_x of this Box.  # noqa: E501
        :type: float
        """

        self._capacity_x = capacity_x

    @property
    def capacity_y(self):
        """Gets the capacity_y of this Box.  # noqa: E501

        Максимальная сумма параметра вместимости Y в условных единицах  # noqa: E501

        :return: The capacity_y of this Box.  # noqa: E501
        :rtype: float
        """
        return self._capacity_y

    @capacity_y.setter
    def capacity_y(self, capacity_y):
        """Sets the capacity_y of this Box.

        Максимальная сумма параметра вместимости Y в условных единицах  # noqa: E501

        :param capacity_y: The capacity_y of this Box.  # noqa: E501
        :type: float
        """

        self._capacity_y = capacity_y

    @property
    def capacity_z(self):
        """Gets the capacity_z of this Box.  # noqa: E501

        Максимальная сумма параметра вместимости Z в условных единицах  # noqa: E501

        :return: The capacity_z of this Box.  # noqa: E501
        :rtype: float
        """
        return self._capacity_z

    @capacity_z.setter
    def capacity_z(self, capacity_z):
        """Sets the capacity_z of this Box.

        Максимальная сумма параметра вместимости Z в условных единицах  # noqa: E501

        :param capacity_z: The capacity_z of this Box.  # noqa: E501
        :type: float
        """

        self._capacity_z = capacity_z

    @property
    def width(self):
        """Gets the width of this Box.  # noqa: E501

        Ширина в метрах  # noqa: E501

        :return: The width of this Box.  # noqa: E501
        :rtype: float
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this Box.

        Ширина в метрах  # noqa: E501

        :param width: The width of this Box.  # noqa: E501
        :type: float
        """

        self._width = width

    @property
    def height(self):
        """Gets the height of this Box.  # noqa: E501

        Высота в метрах  # noqa: E501

        :return: The height of this Box.  # noqa: E501
        :rtype: float
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Box.

        Высота в метрах  # noqa: E501

        :param height: The height of this Box.  # noqa: E501
        :type: float
        """

        self._height = height

    @property
    def length(self):
        """Gets the length of this Box.  # noqa: E501

        Длина в метрах  # noqa: E501

        :return: The length of this Box.  # noqa: E501
        :rtype: float
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Box.

        Длина в метрах  # noqa: E501

        :param length: The length of this Box.  # noqa: E501
        :type: float
        """

        self._length = length

    @property
    def features(self):
        """Gets the features of this Box.  # noqa: E501

        Список возможностей отсека, по которому определяется совместимость с грузом  # noqa: E501

        :return: The features of this Box.  # noqa: E501
        :rtype: list[str]
        """
        return self._features

    @features.setter
    def features(self, features):
        """Sets the features of this Box.

        Список возможностей отсека, по которому определяется совместимость с грузом  # noqa: E501

        :param features: The features of this Box.  # noqa: E501
        :type: list[str]
        """

        self._features = features

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
        if issubclass(Box, dict):
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
        if not isinstance(other, Box):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

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


class UnplannedOrder(object):
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
        'order': 'Order',
        'reason': 'str'
    }

    attribute_map = {
        'order': 'order',
        'reason': 'reason'
    }

    def __init__(self, order=None, reason=None):  # noqa: E501
        """UnplannedOrder - a model defined in Swagger"""  # noqa: E501
        self._order = None
        self._reason = None
        self.discriminator = None
        if order is not None:
            self.order = order
        if reason is not None:
            self.reason = reason

    @property
    def order(self):
        """Gets the order of this UnplannedOrder.  # noqa: E501


        :return: The order of this UnplannedOrder.  # noqa: E501
        :rtype: Order
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this UnplannedOrder.


        :param order: The order of this UnplannedOrder.  # noqa: E501
        :type: Order
        """

        self._order = order

    @property
    def reason(self):
        """Gets the reason of this UnplannedOrder.  # noqa: E501

        Вероятная причина, по которой заказ не запланировался  # noqa: E501

        :return: The reason of this UnplannedOrder.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this UnplannedOrder.

        Вероятная причина, по которой заказ не запланировался  # noqa: E501

        :param reason: The reason of this UnplannedOrder.  # noqa: E501
        :type: str
        """

        self._reason = reason

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
        if issubclass(UnplannedOrder, dict):
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
        if not isinstance(other, UnplannedOrder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

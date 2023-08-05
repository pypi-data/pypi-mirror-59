# coding: utf-8

"""
    VeeRoute.LSS Merchandiser

    Программный интерфейс для планирования работ торговых предствителей.  # noqa: E501

    OpenAPI spec version: 1.7.153581
    Contact: support@veeroute.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class TransportFactor(object):
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
        'transport_type': 'TransportType',
        'speed': 'float'
    }

    attribute_map = {
        'transport_type': 'transport_type',
        'speed': 'speed'
    }

    def __init__(self, transport_type=None, speed=1):  # noqa: E501
        """TransportFactor - a model defined in Swagger"""  # noqa: E501
        self._transport_type = None
        self._speed = None
        self.discriminator = None
        self.transport_type = transport_type
        self.speed = speed

    @property
    def transport_type(self):
        """Gets the transport_type of this TransportFactor.  # noqa: E501


        :return: The transport_type of this TransportFactor.  # noqa: E501
        :rtype: TransportType
        """
        return self._transport_type

    @transport_type.setter
    def transport_type(self, transport_type):
        """Sets the transport_type of this TransportFactor.


        :param transport_type: The transport_type of this TransportFactor.  # noqa: E501
        :type: TransportType
        """
        if transport_type is None:
            raise ValueError("Invalid value for `transport_type`, must not be `None`")  # noqa: E501

        self._transport_type = transport_type

    @property
    def speed(self):
        """Gets the speed of this TransportFactor.  # noqa: E501

        Множитель средней скорости транспорта  # noqa: E501

        :return: The speed of this TransportFactor.  # noqa: E501
        :rtype: float
        """
        return self._speed

    @speed.setter
    def speed(self, speed):
        """Sets the speed of this TransportFactor.

        Множитель средней скорости транспорта  # noqa: E501

        :param speed: The speed of this TransportFactor.  # noqa: E501
        :type: float
        """
        if speed is None:
            raise ValueError("Invalid value for `speed`, must not be `None`")  # noqa: E501

        self._speed = speed

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
        if issubclass(TransportFactor, dict):
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
        if not isinstance(other, TransportFactor):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

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


class TrafficMatrix(object):
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
        'time_window': 'TimeWindow',
        'distance_matrix': 'DistanceMatrix'
    }

    attribute_map = {
        'time_window': 'time_window',
        'distance_matrix': 'distance_matrix'
    }

    def __init__(self, time_window=None, distance_matrix=None):  # noqa: E501
        """TrafficMatrix - a model defined in Swagger"""  # noqa: E501
        self._time_window = None
        self._distance_matrix = None
        self.discriminator = None
        self.time_window = time_window
        self.distance_matrix = distance_matrix

    @property
    def time_window(self):
        """Gets the time_window of this TrafficMatrix.  # noqa: E501


        :return: The time_window of this TrafficMatrix.  # noqa: E501
        :rtype: TimeWindow
        """
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        """Sets the time_window of this TrafficMatrix.


        :param time_window: The time_window of this TrafficMatrix.  # noqa: E501
        :type: TimeWindow
        """
        if time_window is None:
            raise ValueError("Invalid value for `time_window`, must not be `None`")  # noqa: E501

        self._time_window = time_window

    @property
    def distance_matrix(self):
        """Gets the distance_matrix of this TrafficMatrix.  # noqa: E501


        :return: The distance_matrix of this TrafficMatrix.  # noqa: E501
        :rtype: DistanceMatrix
        """
        return self._distance_matrix

    @distance_matrix.setter
    def distance_matrix(self, distance_matrix):
        """Sets the distance_matrix of this TrafficMatrix.


        :param distance_matrix: The distance_matrix of this TrafficMatrix.  # noqa: E501
        :type: DistanceMatrix
        """
        if distance_matrix is None:
            raise ValueError("Invalid value for `distance_matrix`, must not be `None`")  # noqa: E501

        self._distance_matrix = distance_matrix

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
        if issubclass(TrafficMatrix, dict):
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
        if not isinstance(other, TrafficMatrix):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

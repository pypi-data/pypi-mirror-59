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


class DistanceMatrix(object):
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
        'waypoints': 'list[Waypoint]',
        'distances': 'list[MatrixLine]',
        'durations': 'list[MatrixLine]'
    }

    attribute_map = {
        'waypoints': 'waypoints',
        'distances': 'distances',
        'durations': 'durations'
    }

    def __init__(self, waypoints=None, distances=None, durations=None):  # noqa: E501
        """DistanceMatrix - a model defined in Swagger"""  # noqa: E501
        self._waypoints = None
        self._distances = None
        self._durations = None
        self.discriminator = None
        self.waypoints = waypoints
        self.distances = distances
        self.durations = durations

    @property
    def waypoints(self):
        """Gets the waypoints of this DistanceMatrix.  # noqa: E501

        Массив географических точек, между которыми вычислены расстояния и времена  # noqa: E501

        :return: The waypoints of this DistanceMatrix.  # noqa: E501
        :rtype: list[Waypoint]
        """
        return self._waypoints

    @waypoints.setter
    def waypoints(self, waypoints):
        """Sets the waypoints of this DistanceMatrix.

        Массив географических точек, между которыми вычислены расстояния и времена  # noqa: E501

        :param waypoints: The waypoints of this DistanceMatrix.  # noqa: E501
        :type: list[Waypoint]
        """
        if waypoints is None:
            raise ValueError("Invalid value for `waypoints`, must not be `None`")  # noqa: E501

        self._waypoints = waypoints

    @property
    def distances(self):
        """Gets the distances of this DistanceMatrix.  # noqa: E501

        Длины маршрутов между точками. Значения в массиве упорядочены в соответствии с порядком элементов в параметре points.   # noqa: E501

        :return: The distances of this DistanceMatrix.  # noqa: E501
        :rtype: list[MatrixLine]
        """
        return self._distances

    @distances.setter
    def distances(self, distances):
        """Sets the distances of this DistanceMatrix.

        Длины маршрутов между точками. Значения в массиве упорядочены в соответствии с порядком элементов в параметре points.   # noqa: E501

        :param distances: The distances of this DistanceMatrix.  # noqa: E501
        :type: list[MatrixLine]
        """
        if distances is None:
            raise ValueError("Invalid value for `distances`, must not be `None`")  # noqa: E501

        self._distances = distances

    @property
    def durations(self):
        """Gets the durations of this DistanceMatrix.  # noqa: E501

        Массив продолжительностей маршрутов между точками. Значения в массиве упорядочены в соответствии с порядком элементов в параметре points.   # noqa: E501

        :return: The durations of this DistanceMatrix.  # noqa: E501
        :rtype: list[MatrixLine]
        """
        return self._durations

    @durations.setter
    def durations(self, durations):
        """Sets the durations of this DistanceMatrix.

        Массив продолжительностей маршрутов между точками. Значения в массиве упорядочены в соответствии с порядком элементов в параметре points.   # noqa: E501

        :param durations: The durations of this DistanceMatrix.  # noqa: E501
        :type: list[MatrixLine]
        """
        if durations is None:
            raise ValueError("Invalid value for `durations`, must not be `None`")  # noqa: E501

        self._durations = durations

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
        if issubclass(DistanceMatrix, dict):
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
        if not isinstance(other, DistanceMatrix):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

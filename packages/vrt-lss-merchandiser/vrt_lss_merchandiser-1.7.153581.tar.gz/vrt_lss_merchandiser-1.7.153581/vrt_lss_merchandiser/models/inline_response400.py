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


class InlineResponse400(object):
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
        'tracedata': 'TraceData',
        'message': 'str',
        'code': 'int'
    }

    attribute_map = {
        'tracedata': 'tracedata',
        'message': 'message',
        'code': 'code'
    }

    def __init__(self, tracedata=None, message=None, code=None):  # noqa: E501
        """InlineResponse400 - a model defined in Swagger"""  # noqa: E501
        self._tracedata = None
        self._message = None
        self._code = None
        self.discriminator = None
        if tracedata is not None:
            self.tracedata = tracedata
        if message is not None:
            self.message = message
        self.code = code

    @property
    def tracedata(self):
        """Gets the tracedata of this InlineResponse400.  # noqa: E501


        :return: The tracedata of this InlineResponse400.  # noqa: E501
        :rtype: TraceData
        """
        return self._tracedata

    @tracedata.setter
    def tracedata(self, tracedata):
        """Sets the tracedata of this InlineResponse400.


        :param tracedata: The tracedata of this InlineResponse400.  # noqa: E501
        :type: TraceData
        """

        self._tracedata = tracedata

    @property
    def message(self):
        """Gets the message of this InlineResponse400.  # noqa: E501

        Сообщение об ошибке  # noqa: E501

        :return: The message of this InlineResponse400.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this InlineResponse400.

        Сообщение об ошибке  # noqa: E501

        :param message: The message of this InlineResponse400.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def code(self):
        """Gets the code of this InlineResponse400.  # noqa: E501

        Код ошибки  # noqa: E501

        :return: The code of this InlineResponse400.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this InlineResponse400.

        Код ошибки  # noqa: E501

        :param code: The code of this InlineResponse400.  # noqa: E501
        :type: int
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

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
        if issubclass(InlineResponse400, dict):
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
        if not isinstance(other, InlineResponse400):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

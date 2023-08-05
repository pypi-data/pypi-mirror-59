# coding: utf-8

"""
    VeeRoute.LSS Routing

    Программный интерфейс для получения маршрутов и матриц расстояний  # noqa: E501

    OpenAPI spec version: 1.7.153581
    Contact: support@veeroute.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class RouteStep(object):
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
        'polyline': 'RoutePolyline'
    }

    attribute_map = {
        'transport_type': 'transport_type',
        'polyline': 'polyline'
    }

    def __init__(self, transport_type=None, polyline=None):  # noqa: E501
        """RouteStep - a model defined in Swagger"""  # noqa: E501
        self._transport_type = None
        self._polyline = None
        self.discriminator = None
        if transport_type is not None:
            self.transport_type = transport_type
        if polyline is not None:
            self.polyline = polyline

    @property
    def transport_type(self):
        """Gets the transport_type of this RouteStep.  # noqa: E501


        :return: The transport_type of this RouteStep.  # noqa: E501
        :rtype: TransportType
        """
        return self._transport_type

    @transport_type.setter
    def transport_type(self, transport_type):
        """Sets the transport_type of this RouteStep.


        :param transport_type: The transport_type of this RouteStep.  # noqa: E501
        :type: TransportType
        """

        self._transport_type = transport_type

    @property
    def polyline(self):
        """Gets the polyline of this RouteStep.  # noqa: E501


        :return: The polyline of this RouteStep.  # noqa: E501
        :rtype: RoutePolyline
        """
        return self._polyline

    @polyline.setter
    def polyline(self, polyline):
        """Sets the polyline of this RouteStep.


        :param polyline: The polyline of this RouteStep.  # noqa: E501
        :type: RoutePolyline
        """

        self._polyline = polyline

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
        if issubclass(RouteStep, dict):
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
        if not isinstance(other, RouteStep):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

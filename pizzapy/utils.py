from typing import Any, Dict, Union
import requests
import xmltodict

def request_json(url: str, **kwargs: Any) -> Dict[str, Any]:
    """Send a GET request to one of the API endpoints that returns JSON.

    Send a GET request to an endpoint, ideally a URL from the urls module.
    The endpoint is formatted with the kwargs passed to it.

    This will error on an invalid request (requests.Request.raise_for_status()), but will otherwise return a dict.
    """
    formatted_url = url.format(**kwargs)
    response = requests.get(formatted_url)
    response.raise_for_status()
    return response.json() # type: ignore


def request_xml(url: str, **kwargs: Any) -> Dict[str, Any]:
    """Send an XML request to one of the API endpoints that returns XML.

    This is in every respect identical to request_json.
    """
    formatted_url = url.format(**kwargs)
    response = requests.get(formatted_url)
    response.raise_for_status()
    return xmltodict.parse(response.text)


def request_data(url: str, data_type: str = "json", **kwargs: Any) -> Dict[str, Any]:
    """Send a GET request to one of the API endpoints that returns data in the specified format.

    This is a wrapper function for request_json and request_xml to handle both types of requests.

    Args:
        url: The endpoint URL, ideally from the urls module.
        data_type: The type of data expected in the response, either "json" or "xml".
        **kwargs: The keyword arguments to be passed to the endpoint URL.

    Returns:
        A dictionary containing the parsed response data.
    """
    if data_type.lower() == "json":
        return request_json(url, **kwargs)
    elif data_type.lower() == "xml":
        return request_xml(url, **kwargs)
    else:
        raise ValueError("Invalid data_type value. Expected 'json' or 'xml'.")

import httpx


class HttpClient:
    def __init__(self, base_url: str, headers: dict = None):
        """
        Initializes the HttpClient with a base URL and optional headers.

        This constructor sets up the base URL and headers to be used for HTTP requests.

        :param base_url: The base URL for the HTTP client.
        :type base_url: str
        :param headers: Optional dictionary of headers to include with each request.
        :type headers: dict, optional
        """
        self.base_url = base_url
        self.headers = headers or {}

    async def get(self, endpoint: str, params: dict = None) -> dict:
        """
        Sends a GET request to the specified endpoint.

        This method uses an asynchronous HTTP client to send a GET request
        to the specified endpoint with optional query parameters. It raises
        an exception if the response status is not successful.

        :param endpoint: The API endpoint to send the GET request to.
        :type endpoint: str
        :param params: Optional dictionary of query parameters to include in the request.
        :type params: dict, optional
        :return: The JSON response from the server.
        :rtype: dict
        :raises httpx.HTTPStatusError: If the response status code is not 2xx.
        """
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=30
        ) as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()

    async def post(self, endpoint: str, data: dict) -> dict:
        """
        Sends a POST request to the specified endpoint.

        This method uses an asynchronous HTTP client to send a POST request
        to the specified endpoint with the provided data. It raises an
        exception if the response status is not successful.

        :param endpoint: The API endpoint to send the POST request to.
        :type endpoint: str
        :param data: The data to include in the request body.
        :type data: dict
        :return: The JSON response from the server.
        :rtype: dict
        :raises httpx.HTTPStatusError: If the response status code is not 2xx.
        """
        raise NotImplementedError

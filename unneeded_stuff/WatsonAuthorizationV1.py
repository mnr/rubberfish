class AuthorizationV1(WatsonDeveloperCloudService):

    """
    Generates tokens, which can be used client-side to avoid exposing the service credentials.
    Tokens are valid for 1 hour and are sent using the `X-Watson-Authorization-Token` header.
    """
    default_url = "https://stream.watsonplatform.net/authorization/api"

    def __init__(self, url=default_url,
                 username=None, password=None, use_vcap_services=True):
        WatsonDeveloperCloudService.__init__(
            self, 'authorization', url, username, password, use_vcap_services)

    def get_token(self, url):
        """
        Retrieves a temporary access token
        """
        # A hack to avoid url-encoding the url, since the authorization service
        # doesn't work with correctly encoded urls

        parsed_url = urlparse.urlsplit(url)
        parsed_url = parsed_url._replace(path='/authorization/api')
        self.url = urlparse.urlunsplit(parsed_url)

        response = self.request(method='GET', url='/v1/token?url=' + url)
        return response.text

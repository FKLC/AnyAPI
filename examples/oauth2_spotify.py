from oauth2client.client import flow_from_clientsecrets
from requests_oauth2 import OAuth2BearerToken
from anyapi import AnyAPI

flow = flow_from_clientsecrets(
    "client_secrets.json",
    scope="user-read-email",
    redirect_uri="http://localhost/callback",
)

print(flow.step1_get_authorize_url())  # Open url in your browser

code = input("Code: ")  # http://localhost/callback?code={CODE}
credentials = flow.step2_exchange(code)

spotify_api = AnyAPI(
    "https://api.spotify.com/v1",
    default_auth=OAuth2BearerToken(credentials.access_token),
)

print(spotify_api.me.GET().json())

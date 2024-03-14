import os

import flet as ft
from flet.auth.providers import GoogleOAuthProvider

from custom.GoogleCalendarSetup import SCOPES, CREDENTIALS_DATA

DEFAULT_FLET_PATH = ""  
DEFAULT_FLET_PORT = 8550
URL = f"http://127.0.0.1:{DEFAULT_FLET_PORT}"


def main(page: ft.Page):

    CLIENT_ID = '4364081911-7p9a5hega532hlvpsvdu0rvhbh0tbkjt.apps.googleusercontent.com'
    CLIENT_SECRET = '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'

    #if page.platform == ft.PagePlatform.ANDROID:

    #    CLIENT_ID = "4364081911-fu0bokuddedahunisef2595s0co4enbv.apps.googleusercontent.com"

    provider = GoogleOAuthProvider(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_url=f"{URL}/oauth_callback",
        # /oauth_callback /api/oauth/redirect
    )

    def login_click(e):
        page.login(
            provider,
            on_open_authorization_url = lambda url: page.launch_url(url),
        )
        


    def on_login(e):
        print("Login error:", e.error)
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)

    page.on_login = on_login
    page.add(ft.ElevatedButton("Login with GitHub", on_click=login_click))

ft.app(
    target=main, 
    port=DEFAULT_FLET_PORT, 
    view=ft.WEB_BROWSER,
    use_color_emoji=True,
)
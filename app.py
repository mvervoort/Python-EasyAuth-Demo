import os
import requests
import tempfile
import base64
import json

from flask import (Flask, render_template, request, send_from_directory, send_file)

app = Flask(__name__)

offline_access_token = '<default-access-token>'

@app.route('/')
def index():
    # Get the logged-in user name and access-token from the request header
    # See: https://learn.microsoft.com/en-us/azure/app-service/configure-authentication-user-identities
    user_name = request.headers.get("X-MS-CLIENT-PRINCIPAL-NAME")
    access_token = request.headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN") or offline_access_token
    
    # Use the access token to get the user info:
    
    # Option 1: OIDC (Open ID Connect) API
    # See: https://learn.microsoft.com/en-us/entra/identity-platform/userinfo
    oidc_user_info = requests.get(
        "https://graph.microsoft.com/oidc/userinfo",
        headers={ 'Authorization': f"Bearer {access_token}" }).json()

    # Otion 2: MS Graph API
    # See: https://learn.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http
    ms_graph_user_info = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={ 'Authorization': f"Bearer {access_token}" }).json()

    # Decode the access token to get the scope of the token.
    # This gives you an idea of what the user has consented to.
    access_token_payload_base64 = access_token.split('.')[1]
    access_token_payload = json.loads(base64.b64decode(access_token_payload_base64.encode('utf-8') + b'==').decode('utf-8'))
    access_token_scope = access_token_payload['scp'].split(' ')

    return render_template('index.html', 
        user_name = user_name,
        oidc_user_info = oidc_user_info,
        ms_graph_user_info = ms_graph_user_info,
        access_token_payload = access_token_payload,
        access_token_scope = access_token_scope)


@app.route('/profile_photo')
def profile_photo():
    access_token = request.headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN") or offline_access_token
    
    # Download the photo, using the access token for authentication.
    # See: https://learn.microsoft.com/en-us/graph/api/profilephoto-get?view=graph-rest-1.0&tabs=http
    photo = requests.get(
        "https://graph.microsoft.com/v1.0/me/photos/120x120/$value",
        headers={ 'Authorization': f"Bearer {access_token}" },
        stream=True
        )

    # If access is denied, return a default photo    
    if photo.status_code == 401:
        return send_file(
            'static/images/profile-photo-no-access.jpg',
            mimetype='image/jpeg')

    # If the photo is not available, return a default photo
    if photo.status_code == 404:
        return send_file(
            'static/images/profile-photo-not-available.jpg',
            mimetype='image/jpeg')

    photo.raise_for_status();

    # Write the photo to a temp-file
    with tempfile.NamedTemporaryFile(suffix=".jpeg", delete=False) as photo_temp_file:
        for chunk in photo:
            photo_temp_file.write(chunk)

    print(f"Photo downloaded in temp file: {photo_temp_file.name}")
    
    return send_file(
        photo_temp_file.name,
        mimetype='image/jpeg')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
   app.run()

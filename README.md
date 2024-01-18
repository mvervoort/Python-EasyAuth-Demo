# Python-EasyAuth-Demo

A Python demo project demonstrating Azure App Service EasyAuth authentication

## Introduction

This demo project demonstrates how to use the HTTP headers which are injected by the Azure App Service authentication,
also calles 'Easy Auth'.
It will fetch the user name and e-mail address to show on screen.
Next it will also fetch the access-token to use to authenticat towards the MS Graph API to fetch more data.

## Getting started

1. Create a new Azure App Service
    - Name = &lt;my-app-service&gt;
2. Deploy the Python-EasyAuth-Demo app to the App Service.<br>
   Can be done in VS-code with Azure extension, of using CI/CD automation.
3. Create an Application Registration in Microsoft Entra ID (previously known as AAD) with:
   - name = &lt;my-name&gt;-python-auth-demo-app
   - Add platform 'Web' with:
        - Redirect URL = https://&lt;my-app-service&gt;.azurewebsites.net/.auth/login/aad/callback
        - ID token = enabled
   - Supported account types = Current tenant - Single tenant
   - API permissions for 'Microsoft Graph' as 'delegated':
        - email
        - offline_access
        - openid
        - User.Read
        - User.Read.All (only needed to show the photo when using guest accounts)
3. Add an identity provider in the Azure App Service Authentication blade with:
   - Identity provider = Microsoft
   - Tenant type = Workforce
   - App registration = &lt;my-name&gt;-python-auth-demo-app
   - Restrict access = Require authentication
   - Unauthenticated requests = Return HTTP 302 Found (Redirect to identity provider)
   - Token store = Enabled
4. Verify the Azure App Service Authentication is configured like:
   - App Service authentication = Enabled
   - Restrict access = Require authentication
   - Unauthenticated requests = Return HTTP 302 Found (Redirect to identity provider)
   - Redirect to = Microsoft
   - Token store = Enabled
5. Test the web-app
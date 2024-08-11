import config as cr

# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel

# Replace these values with your actual API credentials
client_id = cr.client_id
secret_key = cr.client_secret
# redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
redirect_uri = cr.redirect_uri
response_type = "code"  
state = "sample_state"

# Create a session model with the provided credentials
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)


# Generate the auth code using the session model
response = session.generate_authcode()

# Print the auth code received in the response
print(response)



# auth_code_str = "auth_code="
# auth_code_length = response.find(auth_code_str)
# auth_code_str=response[auth_code_length+len(auth_code_str)]
# print(auth_code_str)



# # The authorization code received from Fyers after the user grants access
# auth_code = "eyJ0eXAi*******.eyJpc3MiOiJhcGkubG9********.r_65Awa1kGdsNTAgD******"

# # Create a session object to handle the Fyers API authentication and token generation
# session = fyersModel.SessionModel(
#     client_id=client_id,
#     secret_key=secret_key, 
#     redirect_uri=redirect_uri, 
#     response_type=response_type, 
#     grant_type=grant_type
# )

# # Set the authorization code in the session object
# session.set_token(auth_code)

# # Generate the access token using the authorization code
# response = session.generate_token()

# # Print the response, which should contain the access token and other details
# print(response)



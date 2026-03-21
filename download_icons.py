import urllib.request
import os

os.makedirs('assets', exist_ok=True)
try:
    urllib.request.urlretrieve('https://img.icons8.com/ios-filled/100/ffffff/dashboard.png', 'assets/dashboard_icon.png')
    urllib.request.urlretrieve('https://img.icons8.com/ios-filled/100/ffffff/folder-invoices.png', 'assets/projects_icon.png')
    urllib.request.urlretrieve('https://img.icons8.com/ios-filled/100/ffffff/user.png', 'assets/freelancer_icon.png')
    print("Icons downloaded successfully.")
except Exception as e:
    print(f"Error downloading: {e}")

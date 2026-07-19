import os
import django
import uuid
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rapidaid_django.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import ScanHistory, Alert

def populate():
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(username='admin')
    if created:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print("Admin user created")

    # Add some scan history
    scans = [
        {
            'detected_issue': 'Skin Inflammation',
            'severity': 'Moderate',
            'confidence': 78.0,
            'first_aid': ["Clean with water", "Apply soothing gel"],
            'red_flags': ["Spreading redness", "Fever"],
            'recommended_action': "Consult a dermatologist",
            'days_ago': 3
        },
        {
            'detected_issue': 'Minor Burn',
            'severity': 'Low',
            'confidence': 91.0,
            'first_aid': ["Cool water for 20 mins", "Cover with sterile wrap"],
            'red_flags': ["Blistering", "Infection"],
            'recommended_action': "Monitor for healing",
            'days_ago': 7
        },
        {
            'detected_issue': 'Deep Cut',
            'severity': 'High',
            'confidence': 95.0,
            'first_aid': ["Apply firm pressure", "Elevate limb"],
            'red_flags': ["Numbness", "Uncontrolled bleeding"],
            'recommended_action': "Go to ER immediately",
            'days_ago': 14
        }
    ]

    for scan_data in scans:
        days_ago = scan_data.pop('days_ago')
        scan = ScanHistory.objects.create(
            user=admin_user,
            **scan_data
        )
        # Manually adjust created_at if needed, but it's auto_now_add
        print(f"Created scan: {scan.detected_issue}")

if __name__ == '__main__':
    populate()

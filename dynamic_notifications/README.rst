=============================
Dynamic Notifications Manager
=============================

**Dynamic Notifications Manager** is an advanced Odoo module that allows users to configure and manage email 
notifications for record creation and state changes. It supports email notifications, ensuring that 
important business updates are never missed.

Key Features
------------
- 🔔 **Custom Notifications:** Set up notifications for specific models and state transitions.
- 📩 **Email:** Supports email notifications.
- 👥 **User-Based Notifications:** Assign specific users to receive email alerts.
- ⚡ **Automated State-Based Alerts:** Trigger notifications when records change state.
- 🎨 **User-Friendly Configuration:** Easily define rules using a selection-based interface.
- 🚀 **Fully Compatible with Odoo 17.0.**

Installation
------------
1. Copy the module to your Odoo **addons** directory.
2. Restart the Odoo server:
   
   .. code-block:: bash

      odoo-bin -c odoo.conf -u dynamic_notifications

3. Enable **Developer Mode** and install the module from **Apps**.

Configuration
-------------
1. Navigate to **Settings → Notifications Configuration**.
2. Create a new notification rule by selecting:
   - The **model** to track.
   - The **state field** and values that trigger notifications.
   - The users to receive alerts.
3. Save and activate the notification rule.

Screenshots
-----------
| **Notification Configuration UI**
| ![Screenshot 1](static/description/images/notification_01.png)

| **In-App Notification Example**
| ![Screenshot 2](static/description/images/notification_02.png)

Support & Contact
-----------------
For support or feature requests, contact:

📧 **Email:** dk.odootech@gmail.com
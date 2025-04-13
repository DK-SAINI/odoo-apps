=========================
Float Time Second Widget
=========================

This module adds a custom widget named **`float_time_second`** to Odoo, allowing users to input and display time in **HH:MM:SS** format for `float` fields. It is useful for attendance tracking, time-based billing, or any feature where precise time entry (including seconds) is required.

Key Features
============

- Custom widget for `float` fields showing time in HH:MM:SS format.
- Supports both input and output with seconds.
- Compatible with Odoo 16 and above.
- Clean, user-friendly input component.
- Fully integrated with Odoo OWL framework.

Installation
============

1. Clone this module into your custom addons directory:

   .. code-block:: bash

      git clone https://github.com/DK-SAINI/odoo-apps.git/float_time_second.git

2. Update the Odoo apps list.
3. Install the module **"Float Time Second Widget"** from the Apps menu.

Usage
=====

1. Add the widget to a float field in your model view like this:

   .. code-block:: xml

      <field name="duration" widget="float_time_second"/>

2. The widget will now render time input as `HH:MM:SS` and convert it to float.


Credits
=======

**Developer:** Dheeraj Chauhan
**Email:** dk.odootech@gmail.com

License
=======

This module is released under the `LGPL-3.0 License <https://www.gnu.org/licenses/lgpl-3.0.html>`_.

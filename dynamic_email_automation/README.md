# Dynamic Email Automation

Inject TO and CC recipients into any email template or chatter notification dynamically, with support for multi-company overrides and global fallbacks.

---

## 🚀 How to Use: Step-by-Step Guide

### Step 1: Access the Configuration
1.  Log in to your Odoo instance as an **Administrator**.
2.  Enable **Developer Mode** (optional, but recommended for advanced settings).
3.  Navigate to **Settings** -> **Technical** -> **Email** -> **Email Automation**.
    *(Alternatively, search for "Email Automation" in the Odoo home search bar).*

### Step 2: Create a New Automation Rule
1.  Click the **New** button to create a rule.
2.  **Rule Name:** Give it a descriptive name (e.g., "Sales Manager CC on Quotations").
3.  **Basic Config:**
    - **Sequence:** If you have multiple rules for the same template, the rule with the lowest sequence number will be processed first.
    - **Company:** 
        - Select a specific company to restrict this rule.
        - **Leave empty** if you want this rule to apply **Globally** to all companies.
    - **Active:** Ensure the toggle is switched on.

### Step 3: Select Target Templates
1.  In the **Target Templates** field, select one or more email templates that this rule should apply to.
2.  *Example:* Select "Sales Order: Confirmation" and "Sales Order: Quotation".

### Step 4: Configure Auto-Recipients
1.  Go to the **Automation Settings** tab.
2.  **Auto TO Emails:** Enter comma-separated email addresses you want to add to the "To" field.
3.  **Auto CC Emails:** Enter comma-separated email addresses you want to add to the "CC" field.
4.  *Note:* The system will automatically remove duplicates and handle formatting.

### Step 5: Save and Verify
1.  Click **Save**.
2.  To verify, go to the record (e.g., a Sales Order) and click **Send by Email**.
3.  The composer will open, and you will see the additional recipients automatically added to the TO or CC fields!

---

## 💡 Key Features and Logic

### 1. Priority Logic (Company vs. Global)
- **Specific Rule:** If a rule is found for the **Current Company**, the system uses it and ignores any Global rules for those specific templates.
- **Global Fallback:** If no company-specific rule exists, the system automatically uses the **Global Rule** (where the company field is empty).

### 2. Recipient Merging
- The system **never overwrites** your existing recipients. 
- It takes the recipients already defined in the template or added manually and **appends** the automated ones.
- Final lists are deduplicated and sorted for a professional appearance.

### 3. Chatter & System Emails
- This module also works for background system notifications and chatter-generated emails as long as they are linked to an Odoo Email Template.

---

## 🛠 Support & Security
- **Multi-Company:** Fully supports Odoo's multi-company environment. Users only see and apply rules for companies they have access to.
- **Logging:** Detailed logs are available in the server log to track which rules are being applied during email generation.

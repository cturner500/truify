# Gmail SMTP Setup Guide

## Overview
To send real email notifications that actually arrive in your inbox, you need to configure Gmail SMTP credentials.

## Setup Instructions

### 1. Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Enable 2-Step Verification if not already enabled

### 2. Generate App Password
1. Go to Google Account → Security → App Passwords
2. Select "Mail" and "Other (Custom name)"
3. Enter "Truify" as the custom name
4. Click "Generate"
5. Copy the 16-character app password (it will look like: xxxx xxxx xxxx xxxx)

### 3. Configure Environment Variables
Create or update your `.env` file in the project root:

```env
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password
```

### 4. Test the Setup
1. Restart your Streamlit app
2. Log in or click "Test Email Notification"
3. Check your email inbox for the notification

## How It Works

- **With Gmail credentials**: Sends real emails via Gmail SMTP
- **Without Gmail credentials**: Falls back to local SMTP for testing

## Troubleshooting

### "Invalid credentials" error
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2-Factor Authentication is enabled
- Check that the App Password is copied correctly (no extra spaces)

### "Less secure app access" error
- Use App Passwords instead of enabling "Less secure app access"
- App Passwords are more secure and recommended by Google

### Email not received
- Check your spam folder
- Verify the email address in `email.csv` is correct
- Make sure the Gmail account has sufficient sending quota

## Security Notes
- Never commit your `.env` file to version control
- App Passwords are more secure than regular passwords
- Consider using a dedicated Gmail account for notifications 
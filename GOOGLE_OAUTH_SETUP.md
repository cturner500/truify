# Google OAuth Setup for Truify.AI

This guide will help you set up Google OAuth authentication for the Truify.AI application.

## Prerequisites

- A Google account
- Access to Google Cloud Console

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "Truify AI")
5. Click "Create"

## Step 2: Enable Google+ API

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google+ API" or "Google+ API v1"
3. Click on it and click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Truify.AI"
   - User support email: Your email
   - Developer contact information: Your email
   - Save and continue through the other sections

4. Create OAuth 2.0 Client ID:
   - Application type: "Web application"
   - Name: "Truify.AI Web Client"
   - Authorized redirect URIs: 
     - For local development: `http://localhost:8501`
     - For production: `https://your-domain.com`
   - Click "Create"

5. Note down the Client ID and Client Secret

## Step 4: Configure Environment Variables

Create a `.env` file in your project root with the following variables:

```env
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_CLIENT_SECRET=your-client-secret-here
GOOGLE_REDIRECT_URI=http://localhost:8501
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Run the Application

```bash
streamlit run code/main.py
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your Client Secret secure
- Use HTTPS in production
- Regularly rotate your OAuth credentials

## Troubleshooting

### Common Issues:

1. **"Invalid redirect URI" error**
   - Make sure the redirect URI in Google Cloud Console matches exactly
   - Check for trailing slashes or protocol differences

2. **"Client ID not found" error**
   - Verify your Client ID is correct
   - Ensure the Google+ API is enabled

3. **"Access denied" error**
   - Check that your Google account has access to the application
   - Verify the OAuth consent screen is properly configured

### For Production Deployment:

1. Update the redirect URI in Google Cloud Console to your production domain
2. Set environment variables on your hosting platform
3. Use HTTPS for all OAuth redirects
4. Consider implementing additional security measures like rate limiting

## Testing

1. Start the application: `streamlit run code/main.py`
2. Navigate to `http://localhost:8501`
3. You should see the login page
4. Click "Sign in with Google"
5. Complete the OAuth flow
6. You should be redirected back to the application and see your user info in the sidebar 
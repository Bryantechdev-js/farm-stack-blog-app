# Email Setup Guide - OTP Delivery

## Overview

The forgot password feature now includes **actual email sending** capability. The system will:

1. Generate a 6-digit OTP
2. Store it in the database with 10-minute expiration
3. Send it to the user's email via SMTP
4. Fall back to console logging if email is not configured

---

## How It Works

### Without Email Configuration (Testing Mode)
```
User requests OTP
    ↓
System generates 6-digit OTP
    ↓
OTP stored in database (10-min expiration)
    ↓
OTP logged to console
    ↓
User copies OTP from console/response
    ↓
User enters OTP in form
```

### With Email Configuration (Production Mode)
```
User requests OTP
    ↓
System generates 6-digit OTP
    ↓
OTP stored in database (10-min expiration)
    ↓
Email sent to user's inbox
    ↓
User receives OTP in email
    ↓
User enters OTP in form
```

---

## Setup Instructions

### Option 1: Gmail (Recommended for Testing)

#### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification"

#### Step 2: Create App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Google will generate a 16-character password
4. Copy this password

#### Step 3: Update .env File
```bash
# backend/.env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
SENDER_EMAIL=your-email@gmail.com
SENDER_NAME=Blog System
```

**Example:**
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=john.doe@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
SENDER_EMAIL=john.doe@gmail.com
SENDER_NAME=Blog System
```

#### Step 4: Restart Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

#### Step 5: Test
1. Go to http://localhost:3000/auth/forgot-password
2. Enter your email
3. Check your inbox for OTP email
4. Enter OTP in form

---

### Option 2: SendGrid (Production Recommended)

#### Step 1: Create SendGrid Account
1. Go to https://sendgrid.com
2. Sign up for free account
3. Verify your email

#### Step 2: Create API Key
1. Go to Settings → API Keys
2. Create new API Key
3. Copy the key

#### Step 3: Update .env File
```bash
# backend/.env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
SENDER_EMAIL=noreply@yourdomain.com
SENDER_NAME=Blog System
```

#### Step 4: Update email.py
Replace the `send_email` function with SendGrid implementation:

```python
import sendgrid
from sendgrid.helpers.mail import Mail

async def send_email(to_email: str, subject: str, body: str) -> bool:
    try:
        sg = sendgrid.SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        email = Mail(
            from_email=SENDER_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=body
        )
        response = sg.send(email)
        return response.status_code == 202
    except Exception as e:
        print(f"[EMAIL] SendGrid Error: {str(e)}")
        raise
```

---

### Option 3: AWS SES (Enterprise)

#### Step 1: Set Up AWS SES
1. Go to AWS Console
2. Navigate to SES
3. Verify email address or domain
4. Create SMTP credentials

#### Step 2: Update .env File
```bash
SMTP_HOST=email-smtp.region.amazonaws.com
SMTP_PORT=587
SMTP_USER=your-ses-username
SMTP_PASSWORD=your-ses-password
SENDER_EMAIL=verified-email@yourdomain.com
SENDER_NAME=Blog System
```

#### Step 3: Restart Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

## Testing Email Sending

### Test 1: Check Console Output
```bash
# Backend console should show:
[EMAIL] OTP generated for user@example.com: 123456
[EMAIL] OTP email sent to user@example.com
```

### Test 2: Check Email Inbox
1. Request OTP
2. Check email inbox
3. Look for email from "Blog System"
4. Copy OTP from email

### Test 3: Verify OTP Works
1. Enter OTP in form
2. Should show "OTP verified!"
3. Proceed to password reset

---

## Email Template

The system sends a professional HTML email:

```html
<html>
    <body style="font-family: Arial, sans-serif;">
        <h2>Password Reset Request</h2>
        <p>You requested to reset your password. Use the OTP below:</p>
        <h1 style="color: #007bff; letter-spacing: 5px;">123456</h1>
        <p>This OTP will expire in 10 minutes.</p>
        <p>If you didn't request this, please ignore this email.</p>
        <hr>
        <p style="color: #666; font-size: 12px;">Do not share this OTP with anyone.</p>
    </body>
</html>
```

---

## Troubleshooting

### Issue: "Failed to send email"
**Solution:**
- Check SMTP credentials in .env
- Verify email is configured correctly
- Check firewall/network settings
- Try with Gmail first (easiest to set up)

### Issue: "Connection refused"
**Solution:**
- Verify SMTP_HOST is correct
- Verify SMTP_PORT is correct (usually 587 for TLS)
- Check internet connection

### Issue: "Authentication failed"
**Solution:**
- Verify SMTP_USER is correct
- Verify SMTP_PASSWORD is correct
- For Gmail, use App Password (not regular password)
- Check if 2FA is enabled

### Issue: "Email not received"
**Solution:**
- Check spam folder
- Verify recipient email is correct
- Check email logs in backend console
- Try sending test email manually

### Issue: "OTP still in console, not in email"
**Solution:**
- Email configuration not set up
- Check .env file for SMTP settings
- Restart backend after updating .env
- Check backend logs for errors

---

## Configuration Reference

### Environment Variables

```bash
# SMTP Configuration
SMTP_HOST=smtp.gmail.com              # SMTP server hostname
SMTP_PORT=587                         # SMTP port (usually 587 for TLS)
SMTP_USER=your-email@gmail.com        # SMTP username
SMTP_PASSWORD=xxxx xxxx xxxx xxxx     # SMTP password or app password
SENDER_EMAIL=your-email@gmail.com     # Email to send from
SENDER_NAME=Blog System               # Display name in email
```

### Supported Email Providers

| Provider | SMTP Host | Port | Notes |
|----------|-----------|------|-------|
| Gmail | smtp.gmail.com | 587 | Use App Password |
| Outlook | smtp-mail.outlook.com | 587 | Use regular password |
| Yahoo | smtp.mail.yahoo.com | 587 | Use app password |
| SendGrid | sendgrid.net | 25/587 | Use API key |
| AWS SES | email-smtp.region.amazonaws.com | 587 | Use SMTP credentials |

---

## Security Best Practices

✅ **Never commit credentials to git**
- Use .env file (already in .gitignore)
- Use environment variables in production

✅ **Use App Passwords**
- Gmail: Use 16-character app password
- Don't use your main password

✅ **Enable TLS**
- Use port 587 with STARTTLS
- Encrypts email transmission

✅ **Rate Limiting**
- Limit OTP requests per email
- Prevent brute force attacks

✅ **OTP Expiration**
- OTP expires after 10 minutes
- Prevents long-term exposure

---

## Production Deployment

### Before Going Live

1. **Set up email service**
   - Choose provider (Gmail, SendGrid, AWS SES)
   - Create account and credentials
   - Test email sending

2. **Update environment variables**
   - Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
   - Set SENDER_EMAIL and SENDER_NAME
   - Use strong, unique credentials

3. **Test email delivery**
   - Request OTP
   - Verify email received
   - Verify OTP works

4. **Monitor email logs**
   - Check backend logs for errors
   - Monitor email delivery rates
   - Set up alerts for failures

5. **Add rate limiting**
   - Limit OTP requests per IP
   - Limit OTP requests per email
   - Implement exponential backoff

---

## Monitoring

### Check Email Logs
```bash
# Backend console shows:
[EMAIL] OTP generated for user@example.com: 123456
[EMAIL] OTP email sent to user@example.com
```

### Monitor Failures
```bash
# Backend console shows errors:
[EMAIL] SMTP Error: Connection refused
[EMAIL] Failed to send email: Authentication failed
```

### Database Monitoring
```javascript
// Check OTP tokens
db.otp_tokens.find()

// Check OTP expiration
db.otp_tokens.find({ expires_at: { $lt: new Date() } })
```

---

## FAQ

### Q: Can I use my regular Gmail password?
**A:** No, you must use an App Password (16 characters). Regular passwords won't work with SMTP.

### Q: How long does OTP last?
**A:** 10 minutes. After that, user must request a new OTP.

### Q: What if email sending fails?
**A:** System falls back to console logging. OTP is still generated and stored. User can copy OTP from console for testing.

### Q: Can I customize the email template?
**A:** Yes, edit the HTML in `send_otp_email()` function in `backend/app/core/email.py`.

### Q: Is email sending required?
**A:** No, it's optional. System works without email (OTP shown in console). Email is recommended for production.

### Q: How do I test without email?
**A:** Don't configure SMTP settings. OTP will be logged to console. Copy OTP from console and enter in form.

---

## Summary

✅ **Email sending is now implemented**
- Supports Gmail, Outlook, Yahoo, SendGrid, AWS SES
- Falls back to console logging if not configured
- Professional HTML email template
- 10-minute OTP expiration

✅ **Easy to set up**
- Just add 6 environment variables
- Restart backend
- Done!

✅ **Production ready**
- Secure SMTP connection
- Error handling
- Logging and monitoring

---

## Next Steps

1. Choose email provider (Gmail recommended for testing)
2. Follow setup instructions for your provider
3. Update .env file with credentials
4. Restart backend
5. Test email sending
6. Deploy to production

---

**Email sending is now ready to use!** 📧

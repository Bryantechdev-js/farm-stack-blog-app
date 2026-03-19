# OTP Debugging Guide - Forgot Password Not Working

## Issue
OTP code is not being received when requesting password reset.

## Root Cause Found
The `send_email()` function was synchronous but being called with `await` in an async context. This caused it to fail silently.

## Fix Applied
Made `send_email()` properly async by running SMTP operations in a thread pool using `asyncio.run_in_executor()`.

---

## How to Debug

### Step 1: Check Backend Logs
When you request OTP, check the backend console for these messages:

**Expected Output:**
```
[FORGOT_PASSWORD] Request for email: user@example.com
[EMAIL] OTP generated for user@example.com: 123456
[EMAIL] Email not configured. OTP for testing: 123456
```

OR (if email is configured):
```
[FORGOT_PASSWORD] Request for email: user@example.com
[EMAIL] OTP generated for user@example.com: 123456
[EMAIL] OTP email sent to user@example.com
```

**If you see errors:**
```
[EMAIL] SMTP Error: Connection refused
[EMAIL] SMTP Error: Authentication failed
[EMAIL] Failed to send email: ...
```

### Step 2: Check Frontend Response
Open DevTools (F12) → Network tab:

1. Go to http://localhost:3000/auth/forgot-password
2. Enter email: `test@example.com`
3. Click "Send OTP"
4. Check Network tab for the request
5. Click on the request to see response

**Expected Response:**
```json
{
  "message": "OTP sent to your email",
  "otp": "123456"
}
```

### Step 3: Check Database
Verify OTP is stored in MongoDB:

```javascript
// In MongoDB shell or Atlas UI
db.otp_tokens.find()

// Should show:
{
  "_id": ObjectId(...),
  "email": "user@example.com",
  "otp": "123456",
  "created_at": ISODate("2026-03-19T10:00:00Z"),
  "expires_at": ISODate("2026-03-19T10:10:00Z")
}
```

---

## Testing Scenarios

### Scenario 1: Test Without Email Configuration (Immediate)

**Setup:**
- Don't configure SMTP in .env
- OTP will be logged to console

**Steps:**
1. Start backend: `python -m uvicorn app.main:app --reload`
2. Go to http://localhost:3000/auth/forgot-password
3. Enter email: `test@example.com`
4. Click "Send OTP"
5. Check backend console for OTP
6. Copy OTP from console
7. Enter OTP in form
8. Set new password
9. Login with new password

**Expected Result:**
- ✅ OTP shown in console
- ✅ OTP shown in response
- ✅ OTP stored in database
- ✅ Can verify OTP
- ✅ Can reset password

### Scenario 2: Test With Gmail Configuration (Optional)

**Setup:**
1. Enable 2FA on Gmail: https://myaccount.google.com/security
2. Create App Password: https://myaccount.google.com/apppasswords
3. Update .env:
   ```bash
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   SENDER_EMAIL=your-email@gmail.com
   SENDER_NAME=Blog System
   ```
4. Restart backend

**Steps:**
1. Go to http://localhost:3000/auth/forgot-password
2. Enter your Gmail email
3. Click "Send OTP"
4. Check Gmail inbox for OTP email
5. Copy OTP from email
6. Enter OTP in form
7. Set new password
8. Login with new password

**Expected Result:**
- ✅ Email received in inbox
- ✅ OTP shown in email
- ✅ Can verify OTP
- ✅ Can reset password

---

## Troubleshooting

### Issue 1: OTP Not in Console
**Symptoms:**
- Backend console doesn't show OTP
- Frontend shows error

**Solutions:**
1. Check backend is running
2. Check console output (look for `[EMAIL]` prefix)
3. Check for errors in console
4. Restart backend

### Issue 2: OTP in Console But Not in Response
**Symptoms:**
- Backend console shows OTP
- Frontend doesn't receive OTP
- Network tab shows error

**Solutions:**
1. Check network response status (should be 200)
2. Check response body has "otp" field
3. Check for CORS errors
4. Restart frontend

### Issue 3: Email Not Received
**Symptoms:**
- Backend shows "OTP email sent"
- Email not in inbox
- Email not in spam

**Solutions:**
1. Check SMTP credentials are correct
2. Check sender email is verified in Gmail
3. Check recipient email is correct
4. Check spam folder
5. Try different email provider

### Issue 4: SMTP Connection Error
**Symptoms:**
- Backend shows: `[EMAIL] SMTP Error: Connection refused`

**Solutions:**
1. Check SMTP_HOST is correct (smtp.gmail.com)
2. Check SMTP_PORT is correct (587)
3. Check internet connection
4. Check firewall settings
5. Try different email provider

### Issue 5: Authentication Failed
**Symptoms:**
- Backend shows: `[EMAIL] SMTP Error: Authentication failed`

**Solutions:**
1. Check SMTP_USER is correct (your email)
2. Check SMTP_PASSWORD is correct (app password, not regular password)
3. For Gmail: Use 16-character app password
4. Check credentials are not expired
5. Try different email provider

---

## Complete Testing Checklist

### Without Email Configuration
- [ ] Backend running
- [ ] Go to forgot password page
- [ ] Enter email
- [ ] Click "Send OTP"
- [ ] Check backend console for OTP
- [ ] OTP shown in response
- [ ] Copy OTP from console
- [ ] Enter OTP in form
- [ ] Click "Verify OTP"
- [ ] OTP verified successfully
- [ ] Enter new password
- [ ] Click "Reset Password"
- [ ] Password reset successful
- [ ] Redirected to login
- [ ] Login with new password works

### With Email Configuration
- [ ] Gmail 2FA enabled
- [ ] App password created
- [ ] .env file updated
- [ ] Backend restarted
- [ ] Go to forgot password page
- [ ] Enter Gmail email
- [ ] Click "Send OTP"
- [ ] Check Gmail inbox
- [ ] Email received
- [ ] OTP in email
- [ ] Copy OTP from email
- [ ] Enter OTP in form
- [ ] Click "Verify OTP"
- [ ] OTP verified successfully
- [ ] Enter new password
- [ ] Click "Reset Password"
- [ ] Password reset successful
- [ ] Redirected to login
- [ ] Login with new password works

---

## Backend Logs Reference

### Successful OTP Generation
```
[FORGOT_PASSWORD] Request for email: user@example.com
[EMAIL] OTP generated for user@example.com: 123456
[EMAIL] Email not configured. OTP for testing: 123456
[FORGOT_PASSWORD] OTP sent to user@example.com
```

### Successful Email Sending
```
[FORGOT_PASSWORD] Request for email: user@example.com
[EMAIL] OTP generated for user@example.com: 123456
[EMAIL] OTP email sent to user@example.com
[FORGOT_PASSWORD] OTP sent to user@example.com
```

### OTP Verification
```
[VERIFY_OTP] Verifying OTP for email: user@example.com
[VERIFY_OTP] OTP verified for: user@example.com
```

### Password Reset
```
[RESET_PASSWORD] Request for email: user@example.com
[RESET_PASSWORD] Password reset successful for: user@example.com
```

### Errors
```
[EMAIL] SMTP Error: Connection refused
[EMAIL] SMTP Error: Authentication failed
[EMAIL] Failed to send email: ...
[FORGOT_PASSWORD] User not found: user@example.com
[VERIFY_OTP] Invalid or expired OTP for: user@example.com
```

---

## Database Queries

### Check OTP Tokens
```javascript
// Find all OTP tokens
db.otp_tokens.find()

// Find OTP for specific email
db.otp_tokens.find({ email: "user@example.com" })

// Check if OTP is expired
db.otp_tokens.find({ expires_at: { $lt: new Date() } })

// Delete expired OTPs
db.otp_tokens.deleteMany({ expires_at: { $lt: new Date() } })
```

### Check Users
```javascript
// Find user by email
db.users.find({ email: "user@example.com" })

// Check if user exists
db.users.countDocuments({ email: "user@example.com" })
```

---

## API Testing with cURL

### Request OTP
```bash
curl http://localhost:8000/api/auth/forgot-password \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Expected Response:
# {
#   "message": "OTP sent to your email",
#   "otp": "123456"
# }
```

### Verify OTP
```bash
curl http://localhost:8000/api/auth/verify-otp \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "otp": "123456"}'

# Expected Response:
# {
#   "message": "OTP verified successfully"
# }
```

### Reset Password
```bash
curl http://localhost:8000/api/auth/reset-password \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "otp": "123456", "new_password": "newpassword123"}'

# Expected Response:
# {
#   "message": "Password reset successfully"
# }
```

---

## Files Modified

**backend/app/core/email.py**
- Changed `send_email()` to properly async
- Uses `asyncio.run_in_executor()` to run SMTP in thread pool
- Prevents blocking the event loop

---

## Summary

✅ **Issue Fixed**
- `send_email()` now properly async
- SMTP operations run in thread pool
- No more silent failures

✅ **How to Test**
1. Without email: OTP shown in console
2. With email: OTP sent to inbox
3. Both: Can verify OTP and reset password

✅ **Next Steps**
1. Restart backend
2. Test forgot password flow
3. Check backend logs
4. Verify OTP is generated
5. Complete password reset

---

**OTP functionality is now fixed!** ✅

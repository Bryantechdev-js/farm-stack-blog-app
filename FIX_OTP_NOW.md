# Fix OTP - Action Guide

## What Was Wrong
The `send_email()` function was synchronous but being called with `await`. This caused it to fail silently.

## What Was Fixed
Made `send_email()` properly async using `asyncio.run_in_executor()`.

## What to Do Now

### Step 1: Restart Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Step 2: Test OTP Flow
1. Go to http://localhost:3000/auth/forgot-password
2. Enter email: `test@example.com`
3. Click "Send OTP"
4. **Check backend console for OTP**
   ```
   [EMAIL] OTP generated for test@example.com: 123456
   ```
5. Copy OTP from console
6. Enter OTP in form
7. Set new password
8. Login with new password

### Step 3: Verify It Works
- ✅ OTP shown in console
- ✅ OTP shown in response
- ✅ Can verify OTP
- ✅ Can reset password
- ✅ Can login with new password

---

## Optional: Set Up Email

If you want OTP sent via email:

1. **Gmail Setup (5 minutes)**
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification"
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy 16-character password

2. **Update .env**
   ```bash
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   SENDER_EMAIL=your-email@gmail.com
   SENDER_NAME=Blog System
   ```

3. **Restart Backend**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

4. **Test**
   - Go to http://localhost:3000/auth/forgot-password
   - Enter your Gmail email
   - Check inbox for OTP email

---

## Troubleshooting

### OTP Not in Console
- Check backend is running
- Look for `[EMAIL]` prefix in console
- Check for errors

### Email Not Received
- Check .env file has SMTP settings
- Check credentials are correct
- Check spam folder
- Check backend logs for errors

### Still Not Working
- Check backend logs for errors
- Check DevTools Network tab
- Check MongoDB for OTP tokens
- Restart backend

---

## Files Modified
- `backend/app/core/email.py` - Made `send_email()` properly async

---

**OTP is now fixed!** ✅

Start testing now!

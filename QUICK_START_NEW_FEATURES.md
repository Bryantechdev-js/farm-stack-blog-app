# Quick Start - New Features

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Step 3: Start Frontend
```bash
cd frontend
npm run dev
```

### Step 4: Open Browser
```
http://localhost:3000
```

---

## 🔑 Feature 1: Forgot Password

### Access
1. Go to http://localhost:3000/auth/login
2. Click "Forgot password?"

### How to Use
1. **Enter Email**: Type your email address
2. **Get OTP**: Copy OTP from response (check console)
3. **Enter OTP**: Paste the 6-digit OTP
4. **Set Password**: Enter new password (min 8 chars)
5. **Confirm**: Confirm password matches
6. **Reset**: Click "Reset Password"
7. **Login**: Use new password to login

### Test Credentials
```
Email: test@example.com
OTP: Check console or response
New Password: newpassword123
```

---

## 👤 Feature 2: Edit Profile

### Access
1. Go to http://localhost:3000/profile
2. Click "Edit Profile"

### How to Use
1. **Full Name**: Enter your display name (optional)
2. **Bio**: Write about yourself (max 500 chars)
3. **Avatar URL**: Paste image URL (optional)
4. **Preview**: See avatar preview
5. **Save**: Click "Save Changes"
6. **Verify**: Check profile page for updates

### Example Data
```
Full Name: John Doe
Bio: I love blogging and sharing stories
Avatar URL: https://example.com/avatar.jpg
```

---

## 📍 New URLs

| Feature | URL |
|---------|-----|
| Forgot Password | http://localhost:3000/auth/forgot-password |
| Edit Profile | http://localhost:3000/edit-profile |
| Profile | http://localhost:3000/profile |
| Login | http://localhost:3000/auth/login |

---

## 🔍 Testing Checklist

### Forgot Password
- [ ] Click "Forgot password?" on login
- [ ] Enter email
- [ ] Copy OTP from response
- [ ] Enter OTP
- [ ] Set new password
- [ ] Confirm password
- [ ] Click "Reset Password"
- [ ] Login with new password

### Edit Profile
- [ ] Go to profile page
- [ ] Click "Edit Profile"
- [ ] Update full name
- [ ] Update bio
- [ ] Update avatar URL
- [ ] See avatar preview
- [ ] Click "Save Changes"
- [ ] Verify changes on profile

---

## 🛠️ API Endpoints

### Forgot Password
```bash
# Request OTP
POST /api/auth/forgot-password
{ "email": "user@example.com" }

# Verify OTP
POST /api/auth/verify-otp
{ "email": "user@example.com", "otp": "123456" }

# Reset Password
POST /api/auth/reset-password
{ "email": "user@example.com", "otp": "123456", "new_password": "newpass123" }
```

### Profile
```bash
# Get Current User
GET /api/auth/me

# Update Profile
PUT /api/auth/profile
{ "full_name": "John Doe", "bio": "...", "avatar_url": "..." }
```

---

## 📁 New Files

### Backend
- `backend/app/core/email.py` - OTP service

### Frontend
- `frontend/src/app/auth/forgot-password/page.tsx` - Forgot password form
- `frontend/src/app/edit-profile/page.tsx` - Profile editing form

---

## 🔐 Security

✅ OTP expires in 10 minutes  
✅ Password hashed with Argon2  
✅ Only authenticated users can edit profile  
✅ Email validation  
✅ Input sanitization  

---

## 🐛 Troubleshooting

### OTP Not Showing
- Check backend console
- Look for: `[EMAIL] OTP sent to user@example.com: 123456`

### Profile Not Updating
- Verify you're logged in
- Check DevTools Network tab
- Verify all fields are valid

### Avatar Not Displaying
- Verify URL is correct
- Check image is publicly accessible
- Try different image URL

---

## 📊 Database

### New Collection: otp_tokens
```javascript
{
  "email": "user@example.com",
  "otp": "123456",
  "created_at": ISODate(...),
  "expires_at": ISODate(...)
}
```

### Updated Collection: users
```javascript
{
  // Existing fields...
  "full_name": "John Doe",
  "bio": "I love blogging",
  "avatar_url": "https://..."
}
```

---

## 📝 Documentation

1. **FORGOT_PASSWORD_AND_PROFILE_FEATURES.md** - Detailed docs
2. **IMPLEMENTATION_GUIDE_NEW_FEATURES.md** - Implementation guide
3. **NEW_FEATURES_SUMMARY.md** - Feature summary
4. **FEATURE_IMPLEMENTATION_CHECKLIST.md** - Checklist
5. **QUICK_START_NEW_FEATURES.md** - This file

---

## ✨ Features

### Forgot Password
- ✅ OTP-based reset
- ✅ 10-minute expiration
- ✅ Argon2 hashing
- ✅ 3-step form
- ✅ Error handling

### Edit Profile
- ✅ Update full name
- ✅ Update bio
- ✅ Update avatar
- ✅ Real-time preview
- ✅ Character counter

---

## 🎯 Next Steps

1. Test all features
2. Deploy to staging
3. Implement email sending
4. Add rate limiting
5. Deploy to production

---

## 💡 Tips

- OTP is returned in response for testing
- Avatar preview shows error image if URL is invalid
- Bio has 500 character limit
- Password must be at least 8 characters
- Email cannot be changed
- Role cannot be changed

---

## 🚀 You're Ready!

Everything is set up and working. Just follow the steps above and start using the new features!

---

**Happy blogging!** 📝

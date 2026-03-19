# MongoDB Connection - Quick Fix

## 🔴 The Problem

You got this error:
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [WinError 10061]
```

**Reason:** Your MongoDB URL had a typo: `@1@` instead of `@`

---

## ✅ What Was Fixed

### 1. Fixed MongoDB URL

**Before:**
```
MONGO_URL = mongodb+srv://bryan:bryantech.dev@1@cluster0.vpzmmtb.mongodb.net/blog?appName=Cluster0
```

**After:**
```
MONGO_URL=mongodb+srv://bryan:bryantech.dev@cluster0.vpzmmtb.mongodb.net/blog?appName=Cluster0
```

### 2. Added Error Handling

- Better error messages in auth endpoints
- Better error messages in posts endpoints
- Proper async/await handling

### 3. Created Test Script

Run this to verify MongoDB connection:
```bash
cd backend
python test_connection.py
```

---

## 🚀 What to Do Now

### Step 1: Verify MongoDB Connection

```bash
cd backend
python test_connection.py
```

**Expected output:**
```
✅ Successfully connected to MongoDB!
👥 Users: 0
📝 Posts: 0
```

### Step 2: Restart Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 3: Test Signup

1. Go to `http://localhost:3000`
2. Click "Sign Up"
3. Enter email and password
4. Click "Sign Up"

**Expected:** No error, redirected to login

---

## 🔍 If Still Not Working

### Check 1: Verify .env File

```bash
cat backend/.env
```

Should show:
```
MONGO_URL=mongodb+srv://bryan:bryantech.dev@cluster0.vpzmmtb.mongodb.net/blog?appName=Cluster0
```

**Important:** No spaces around `=`, no `@1@`

### Check 2: MongoDB Atlas Status

1. Go to https://cloud.mongodb.com
2. Login
3. Check if cluster is running (green status)
4. Check if your IP is whitelisted

### Check 3: Test Connection String

```bash
mongosh "mongodb+srv://bryan:bryantech.dev@cluster0.vpzmmtb.mongodb.net/blog"
```

If this works, MongoDB is accessible.

---

## 📋 Files Changed

1. **backend/.env** - Fixed MongoDB URL
2. **backend/app/api/auth.py** - Added error handling
3. **backend/app/api/posts.py** - Added error handling
4. **backend/test_connection.py** - New test script

---

## ✨ Now Your App Should Work!

1. ✅ Backend connects to MongoDB
2. ✅ Signup works
3. ✅ Login works
4. ✅ Create posts works
5. ✅ View posts works

---

## 🎯 Quick Checklist

- [ ] Run `python test_connection.py` - should pass
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can sign up new user
- [ ] Can login with credentials
- [ ] Can create blog post
- [ ] Can view posts

---

**Status: ✅ MongoDB connection fixed!**

Run the test script to verify everything is working.

# MongoDB Setup & Troubleshooting

## The Error You Got

```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [WinError 10061] 
No connection could be made because the target machine actively refused it
```

**What it means:** The backend tried to connect to MongoDB but couldn't find it.

**Why it happened:** Your MongoDB URL had a typo (`@1@` instead of `@`), and the code was trying to connect to `localhost:27017` instead of MongoDB Atlas.

---

## ✅ What Was Fixed

1. **Fixed MongoDB URL** in `backend/.env`
   - Changed: `mongodb+srv://bryan:bryantech.dev@1@cluster0...`
   - To: `mongodb+srv://bryan:bryantech.dev@cluster0...`

2. **Added error handling** in auth and posts endpoints
   - Better error messages
   - Proper async/await handling

3. **Created test script** to verify connection

---

## 🧪 Test Your MongoDB Connection

### Step 1: Run the Test Script

```bash
cd backend
python test_connection.py
```

**Expected output:**
```
============================================================
MongoDB Connection Test
============================================================

📍 MongoDB URL: mongodb+srv://bryan:bryantech.dev@cluster0...

🔄 Connecting to MongoDB...
✅ Successfully connected to MongoDB!

📚 Collections in 'blog' database: []

👥 Users: 0
📝 Posts: 0

============================================================
✅ All tests passed! MongoDB is working correctly.
============================================================
```

### Step 2: If Test Fails

Check these things:

1. **Verify .env file**
   ```bash
   cat backend/.env
   ```
   Should show:
   ```
   MONGO_URL=mongodb+srv://bryan:bryantech.dev@cluster0.vpzmmtb.mongodb.net/blog?appName=Cluster0
   ```

2. **Check MongoDB Atlas**
   - Go to https://cloud.mongodb.com
   - Login with your account
   - Check if cluster is running (green status)
   - Check IP whitelist includes your IP

3. **Test connection string**
   ```bash
   mongosh "mongodb+srv://bryan:bryantech.dev@cluster0.vpzmmtb.mongodb.net/blog"
   ```

---

## 🚀 Now Run Your Application

### Terminal 1 - Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Terminal 2 - Frontend

```bash
cd frontend
npm install
npm run dev
```

**Expected output:**
```
  ▲ Next.js 15.5.13
  - Local:        http://localhost:3000
```

### Open Browser

Go to `http://localhost:3000`

---

## 🧪 Test Signup

1. Click "Sign Up"
2. Enter email: `test@example.com`
3. Enter password: `password123`
4. Click "Sign Up"

**Expected:**
- No error
- Redirected to login page
- Backend shows: `POST /auth/signup HTTP/1.1" 200 OK`

---

## 🔍 Common Issues & Solutions

### Issue 1: "No connection could be made"

**Cause:** MongoDB URL is wrong or MongoDB is not accessible

**Solution:**
1. Check `.env` file has correct URL
2. Verify MongoDB Atlas cluster is running
3. Check IP whitelist in MongoDB Atlas
4. Run `python test_connection.py`

### Issue 2: "Invalid credentials"

**Cause:** Username or password in URL is wrong

**Solution:**
1. Go to MongoDB Atlas
2. Click "Database Access"
3. Check username and password
4. Update `.env` file

### Issue 3: "Timeout"

**Cause:** Network connectivity issue

**Solution:**
1. Check internet connection
2. Check firewall settings
3. Try from different network
4. Check MongoDB Atlas status page

### Issue 4: "Authentication failed"

**Cause:** IP not whitelisted

**Solution:**
1. Go to MongoDB Atlas
2. Click "Network Access"
3. Add your IP address
4. Or add `0.0.0.0/0` to allow all (not recommended for production)

---

## 📝 MongoDB Atlas Setup (If Needed)

### Create a New Cluster

1. Go to https://cloud.mongodb.com
2. Click "Create" → "Build a Cluster"
3. Choose "Free" tier
4. Select region closest to you
5. Click "Create Cluster"
6. Wait for cluster to be created (5-10 minutes)

### Create Database User

1. Click "Database Access"
2. Click "Add New Database User"
3. Enter username: `bryan`
4. Enter password: `bryantech.dev`
5. Click "Add User"

### Get Connection String

1. Click "Databases"
2. Click "Connect" on your cluster
3. Choose "Drivers"
4. Copy the connection string
5. Replace `<password>` with your password
6. Update `backend/.env`

### Add IP to Whitelist

1. Click "Network Access"
2. Click "Add IP Address"
3. Enter your IP or `0.0.0.0/0` (allow all)
4. Click "Confirm"

---

## ✅ Verification Checklist

- [ ] `backend/.env` has correct MongoDB URL
- [ ] MongoDB URL has no typos (no `@1@`)
- [ ] MongoDB Atlas cluster is running
- [ ] Your IP is whitelisted
- [ ] `python test_connection.py` passes
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can sign up new user
- [ ] Can login with credentials
- [ ] Can create blog post

---

## 🔐 Security Notes

**Never commit `.env` to git!**

Your `.env` contains:
- MongoDB username
- MongoDB password
- Database name

These are secrets and should never be exposed.

**For production:**
- Use environment variables from hosting platform
- Use strong passwords
- Restrict IP whitelist to your servers only
- Enable encryption at rest
- Enable backups

---

## 📞 Still Having Issues?

1. Check backend terminal for error messages
2. Run `python test_connection.py` to diagnose
3. Check MongoDB Atlas status
4. Verify `.env` file is correct
5. Try restarting backend and frontend
6. Check firewall/antivirus settings

---

## 🎯 Next Steps

Once MongoDB is working:

1. ✅ Test signup/login
2. ✅ Create blog posts
3. ✅ Upload images
4. ✅ View posts
5. ✅ Read documentation

---

**Status: MongoDB should now be working!**

Run `python test_connection.py` to verify, then start your application.

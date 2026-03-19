# MongoDB Authentication Error - FIX

## The Error

```
bad auth : authentication failed
code: 8000, codeName: 'AtlasError'
```

**Meaning:** Your MongoDB username or password is wrong.

---

## 🔧 How to Fix

### Step 1: Go to MongoDB Atlas

1. Open https://cloud.mongodb.com
2. Login with your account
3. Click on your project
4. Click "Database Access" (left sidebar)

### Step 2: Check Your Database User

Look for a user named `bryan`:

- If it exists: Check if the password is `bryantech.dev`
- If it doesn't exist: Create a new user

### Step 3: If User Doesn't Exist - Create It

1. Click "Add New Database User"
2. Choose "Password" authentication
3. Enter username: `bryan`
4. Enter password: `bryantech.dev`
5. Click "Add User"
6. Wait for it to be created

### Step 4: If User Exists - Reset Password

1. Find the `bryan` user
2. Click the "..." menu
3. Click "Edit Password"
4. Enter new password: `bryantech.dev`
5. Click "Update User"

### Step 5: Verify Connection String

1. Click "Databases" (left sidebar)
2. Click "Connect" on your cluster
3. Choose "Drivers"
4. Copy the connection string
5. It should look like:
   ```
   mongodb+srv://bryan:bryantech.dev@cluster0.vpzmmtb.mongodb.net/?retryWrites=true&w=majority
   ```

### Step 6: Update Your .env File

Replace `backend/.env` with:
```
MONGO_URL=mongodb+srv://bryan:bryantech.dev@cluster0.vpzmmtb.mongodb.net/blog?appName=Cluster0
```

**Important:**
- Replace `bryan` with your actual username
- Replace `bryantech.dev` with your actual password
- Keep the database name as `blog`
- Keep it on ONE line

### Step 7: Restart Backend

```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## ⚠️ Common Issues

### Issue 1: Special Characters in Password

If your password has special characters like `@`, `#`, `$`, etc., you need to URL-encode them:

- `@` → `%40`
- `#` → `%23`
- `$` → `%24`
- `:` → `%3A`
- `/` → `%2F`

**Example:**
```
Password: my@password#123
URL: mongodb+srv://bryan:my%40password%23123@cluster0...
```

### Issue 2: Wrong Cluster

Make sure you're using the correct cluster name. Check in MongoDB Atlas:
1. Click "Databases"
2. Find your cluster
3. Click "Connect"
4. Copy the connection string

### Issue 3: IP Not Whitelisted

Even with correct credentials, you need to whitelist your IP:
1. Click "Network Access" (left sidebar)
2. Click "Add IP Address"
3. Enter your IP or `0.0.0.0/0` (allow all)
4. Click "Confirm"

---

## 🧪 Test the Connection

After updating `.env`, run:

```bash
cd backend
python test_mongo_simple.py
```

**Expected output:**
```
✅ Successfully connected to MongoDB Atlas!
   Users: 0
   Posts: 0
✅ All tests passed!
```

---

## 📋 Checklist

- [ ] Logged into MongoDB Atlas
- [ ] Found or created user `bryan`
- [ ] Password is `bryantech.dev`
- [ ] Updated `backend/.env` with correct credentials
- [ ] Restarted backend
- [ ] Ran `python test_mongo_simple.py` - passed
- [ ] Can sign up new user

---

## 🆘 Still Not Working?

1. **Double-check credentials** in MongoDB Atlas
2. **Check for special characters** in password (need URL encoding)
3. **Verify IP is whitelisted** in Network Access
4. **Check cluster name** is correct
5. **Restart backend** after any changes

---

## 💡 Alternative: Create New User

If you're unsure about the current user, create a new one:

1. Go to MongoDB Atlas
2. Click "Database Access"
3. Click "Add New Database User"
4. Username: `bloguser`
5. Password: `BlogPassword123!`
6. Click "Add User"
7. Update `.env`:
   ```
   MONGO_URL=mongodb+srv://bloguser:BlogPassword123!@cluster0.vpzmmtb.mongodb.net/blog?appName=Cluster0
   ```

**Note:** If password has special characters, URL-encode them!

---

**Status: Follow the steps above to fix authentication**

# System Verification Checklist

## Pre-Flight Checks

### Backend Setup
- [ ] MongoDB connection string is valid in `.env`
- [ ] JWT_SECRET is set in `.env`
- [ ] Python virtual environment is activated
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Backend starts without errors: `python -m uvicorn app.main:app --reload`

### Frontend Setup
- [ ] Node.js and npm installed
- [ ] All dependencies installed: `npm install`
- [ ] `.env.local` exists with `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`
- [ ] Frontend starts without errors: `npm run dev`

## Architecture Verification

### 1. Middleware is Active
**File**: `backend/app/main.py`
**Check**: Line should contain:
```python
from app.core.middleware import auth_middleware
app.middleware("http")(auth_middleware)
```
**Status**: ✅ FIXED

### 2. Image Paths are Correct
**File**: `backend/app/api/posts.py`
**Check**: `format_post()` function should prepend `/` to image paths:
```python
if image and not image.startswith("/"):
    image = f"/{image}"
```
**Status**: ✅ FIXED

### 3. Next.js Rewrites are Configured
**File**: `frontend/next.config.ts`
**Check**: Should have rewrites for `/api/*` and `/uploads/*`:
```typescript
rewrites: async () => {
  return {
    beforeFiles: [
      { source: '/api/:path*', destination: 'http://localhost:8000/:path*' },
      { source: '/uploads/:path*', destination: 'http://localhost:8000/uploads/:path*' },
    ],
  };
}
```
**Status**: ✅ VERIFIED

### 4. Frontend Uses Relative Paths
**Files to Check**:
- `frontend/src/app/page.tsx` - ✅ Uses `/api/*`
- `frontend/src/app/auth/login/page.tsx` - ✅ Uses `/api/*`
- `frontend/src/app/dashboard/page.tsx` - ✅ Uses `/api/*`
- `frontend/src/app/posts/[id]/page.tsx` - ✅ Uses `/api/*`
- `frontend/src/app/profile/page.tsx` - ✅ Uses `/api/*`

**Status**: ✅ ALL VERIFIED

## Runtime Verification

### Step 1: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```
**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 2: Start Frontend
```bash
cd frontend
npm run dev
```
**Expected Output**:
```
▲ Next.js 15.x.x
- Local:        http://localhost:3000
```

### Step 3: Test Signup
1. Go to http://localhost:3000/auth/signup
2. Enter email: `test@example.com`
3. Enter password: `password123`
4. Click "Sign Up"
5. **Expected**: Success message, redirect to login

### Step 4: Test Login
1. Go to http://localhost:3000/auth/login
2. Enter email: `test@example.com`
3. Enter password: `password123`
4. Click "Sign In"
5. **Expected**: Success message, redirect to dashboard

### Step 5: Verify Cookie Storage
1. Open DevTools (F12)
2. Go to Application tab
3. Click Cookies → http://localhost:3000
4. **Expected**: See `access_token` cookie with:
   - Value: JWT token (long string)
   - HttpOnly: ✓ (checked)
   - SameSite: Lax
   - Path: /

### Step 6: Test Image Upload
1. Go to http://localhost:3000/dashboard
2. Click "+ New Post"
3. Enter title: "Test Post"
4. Enter content: "This is a test"
5. Select an image file
6. Click "Publish Post"
7. **Expected**: Success message, post appears in list with image

### Step 7: Verify Image Display
1. Click on the post to view details
2. **Expected**: Image displays correctly
3. Open DevTools Network tab
4. **Expected**: Image request shows `/uploads/filename.jpg`

### Step 8: Test Comments
1. On post detail page, scroll to comments
2. Enter comment text: "Great post!"
3. Click "Post Comment"
4. **Expected**: Comment appears immediately with your email

### Step 9: Test Like/Bookmark
1. On post detail page, click heart icon
2. **Expected**: Like count increases, button highlights
3. Click heart again
4. **Expected**: Like count decreases, button unhighlights
5. Repeat for bookmark button

### Step 10: Test Logout
1. Go to http://localhost:3000/profile
2. Click "Logout" button
3. **Expected**: Redirected to login page
4. Open DevTools → Application → Cookies
5. **Expected**: `access_token` cookie is gone

## Error Scenarios

### Scenario 1: Access Protected Page Without Login
1. Clear cookies (DevTools → Application → Cookies → Delete all)
2. Go to http://localhost:3000/dashboard
3. **Expected**: Redirected to login page

### Scenario 2: Invalid Credentials
1. Go to http://localhost:3000/auth/login
2. Enter wrong password
3. Click "Sign In"
4. **Expected**: Error message "Invalid credentials"

### Scenario 3: Duplicate Email
1. Go to http://localhost:3000/auth/signup
2. Enter email that already exists
3. Click "Sign Up"
4. **Expected**: Error message "Email already exists"

### Scenario 4: Missing Image on Post Creation
1. Go to http://localhost:3000/dashboard
2. Click "+ New Post"
3. Enter title and content but don't select image
4. Click "Publish Post"
5. **Expected**: Error message "Please select an image"

## Database Verification

### Check Users Collection
```bash
# In MongoDB shell or Atlas UI
db.users.find()
```
**Expected**: Should see created users with:
- email
- password (hashed with Argon2)
- role (user or admin)
- created_at

### Check Posts Collection
```bash
db.posts.find()
```
**Expected**: Should see created posts with:
- title
- content
- image (path like `/uploads/uuid.jpg`)
- author_id
- author_email
- likes (array of user IDs)
- bookmarks (array of user IDs)
- comments_count

### Check Comments Collection
```bash
db.comments.find()
```
**Expected**: Should see comments with:
- post_id
- user_id
- user_email
- content
- created_at

## Performance Checks

### API Response Times
- Login: < 500ms
- Get posts: < 1000ms
- Create post: < 2000ms (includes image upload)
- Add comment: < 500ms

### Frontend Performance
- Page load: < 3s
- Image load: < 2s
- Comment submission: < 1s

## Security Verification

### Password Hashing
1. Check database user document
2. Password field should start with `$argon2`
3. Should NOT be plain text

### JWT Token
1. Login and get token from cookie
2. Decode at https://jwt.io
3. Should contain:
   - `sub`: user ID
   - `role`: user role
   - `exp`: expiration time

### CORS Headers
1. Open DevTools Network tab
2. Make any API request
3. Check Response Headers for:
   - `Access-Control-Allow-Credentials: true`
   - `Access-Control-Allow-Origin: http://localhost:3000`

## Final Sign-Off

- [ ] All pre-flight checks passed
- [ ] Backend starts successfully
- [ ] Frontend starts successfully
- [ ] Signup works
- [ ] Login works and stores cookie
- [ ] Images upload and display
- [ ] Comments work
- [ ] Likes/bookmarks work
- [ ] Logout redirects to login
- [ ] Protected pages redirect to login when not authenticated
- [ ] All error scenarios handled properly
- [ ] Database contains expected data
- [ ] Performance is acceptable
- [ ] Security measures are in place

## Troubleshooting

If any check fails, refer to `FINAL_FIXES_APPLIED.md` for detailed solutions.

### Common Issues:
1. **Cookie not storing** → Check middleware is active and returns JSON
2. **Images not loading** → Check image paths start with `/uploads/`
3. **Comments fail** → Check error message in DevTools console
4. **Redirect not working** → Check router.push() is called
5. **Database errors** → Check MongoDB connection string in .env

## Next Steps

Once all checks pass:
1. Deploy to production
2. Update environment variables
3. Enable HTTPS
4. Set secure=True in cookies
5. Monitor logs
6. Optimize performance
7. Add additional features

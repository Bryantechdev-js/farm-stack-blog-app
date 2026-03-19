# Quick Start Guide - After Critical Fixes

## What Was Fixed
The JWT cookie was NOT being stored because:
1. ❌ Middleware was returning redirects instead of JSON responses
2. ❌ Frontend was using full URLs instead of relative paths
3. ❌ No proxy configuration in Next.js

All three issues are now fixed!

## How to Test

### Step 1: Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```
Backend runs on `http://localhost:8000`

### Step 2: Start Frontend
```bash
cd frontend
npm run dev
```
Frontend runs on `http://localhost:3000`

### Step 3: Test Authentication Flow

#### Sign Up
1. Go to `http://localhost:3000/auth/signup`
2. Enter email and password (min 8 chars)
3. Click "Sign Up"
4. Should redirect to login page

#### Login
1. Go to `http://localhost:3000/auth/login`
2. Enter credentials
3. Click "Sign In"
4. Should redirect to dashboard
5. **Check DevTools** → Application → Cookies → `access_token` should be there ✅

#### Create Post
1. On dashboard, click "+ New Post"
2. Fill in title, content, and select image
3. Click "Publish Post"
4. Post should appear in "My Posts" section
5. Toast notification should show success ✅

#### Like/Comment
1. Go to home page
2. Click on any post
3. Click heart icon to like
4. Add comment and post
5. Should work without errors ✅

#### Admin Panel
1. If you're admin, click "Admin" in navbar
2. View analytics, users, posts, comments
3. Can delete users/posts/comments

#### Logout
1. Click profile → Logout
2. Cookie should be deleted
3. Redirected to home page
4. Trying to access dashboard should redirect to login ✅

## Expected Behavior

### ✅ What Should Work Now
- Login stores JWT in httpOnly cookie
- Dashboard loads without infinite loading
- CRUD operations work (create, read, update, delete posts)
- Comments and likes work
- Admin panel works
- Logout deletes cookie
- 401 errors redirect to login
- Toast notifications show on success/error

### ❌ What Should NOT Work
- Accessing protected routes without login (redirects to login)
- Using expired tokens (redirects to login)
- Invalid credentials (shows error toast)

## Troubleshooting

### Cookie Not Showing in DevTools
1. Check browser console for errors
2. Verify backend is running on port 8000
3. Verify frontend is running on port 3000
4. Check that login response is 200 (not 301/302)
5. Restart both frontend and backend

### Dashboard Still Loading
1. Check browser console for errors
2. Verify `/api/auth/me` returns 200 with user data
3. Check that cookie is being sent with request
4. Verify backend CORS allows credentials

### CRUD Operations Failing
1. Check browser console for 401 errors
2. Verify cookie is present in DevTools
3. Verify backend is validating token correctly
4. Check that `credentials: 'include'` is in fetch calls

### Admin Panel Not Accessible
1. Verify user role is "admin" in database
2. Check that `/api/admin/analytics` returns data
3. Verify 401 handling redirects to login

## Key Files to Know

### Backend
- `backend/app/main.py` - FastAPI app setup
- `backend/app/api/auth.py` - Login/signup endpoints
- `backend/app/api/posts.py` - CRUD endpoints
- `backend/app/core/security.py` - JWT and password hashing
- `backend/.env` - Environment variables

### Frontend
- `frontend/next.config.ts` - API proxy configuration
- `frontend/src/app/auth/login/page.tsx` - Login page
- `frontend/src/app/dashboard/page.tsx` - Dashboard with CRUD
- `frontend/src/app/page.tsx` - Home page with posts
- `frontend/src/components/Toast.tsx` - Toast notifications

## Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb+srv://...
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-12345
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Production Deployment

When deploying to production:

1. **Change JWT_SECRET** to a strong random value
2. **Set secure=True** in cookie settings (requires HTTPS)
3. **Update CORS origins** to your domain
4. **Use environment variables** for all secrets
5. **Enable HTTPS** for secure cookies
6. **Set proper SameSite** policy (Lax or Strict)

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Cookie not stored | Check that API returns 200, not redirect |
| Dashboard infinite loading | Check `/api/auth/me` endpoint |
| CRUD operations fail | Verify cookie is sent with request |
| 401 errors | Token expired, need to login again |
| Admin panel 403 | User role is not "admin" |
| Image upload fails | Check file type and size |

## Next Steps

1. ✅ Test all features thoroughly
2. ✅ Check browser DevTools for errors
3. ✅ Verify cookies are stored correctly
4. ✅ Test logout and re-login
5. ✅ Test admin panel
6. ✅ Test CRUD operations
7. Consider adding refresh tokens
8. Consider adding rate limiting
9. Consider adding error tracking
10. Deploy to production

## Support

If you encounter issues:
1. Check browser console for errors
2. Check backend logs for errors
3. Verify all environment variables are set
4. Verify both frontend and backend are running
5. Clear browser cache and cookies
6. Restart both services

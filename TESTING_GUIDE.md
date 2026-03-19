# Testing Guide - Cookie Auth & New UI

## Quick Start

### 1. Start Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Access Application
- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

## Test Scenarios

### Test 1: Cookie-Based Authentication
**Objective**: Verify cookies are being set and sent correctly

**Steps**:
1. Open http://localhost:3000/auth/signup
2. Create account with email: `test@example.com`, password: `password123`
3. You should be redirected to login page
4. Login with same credentials
5. Open DevTools (F12) → Application → Cookies
6. Verify `access_token` cookie exists with value
7. You should be redirected to dashboard

**Expected Result**: ✅ Cookie is set and user is authenticated

### Test 2: Create Post (Tests 401 Fix)
**Objective**: Verify 401 error is fixed and posts can be created

**Steps**:
1. Login (from Test 1)
2. Click "+ New Post" button
3. Fill in:
   - Title: "My First Post"
   - Content: "This is a test post"
   - Image: Select any image file
4. Click "Publish Post"
5. Check browser console for errors

**Expected Result**: ✅ Post is created successfully, no 401 error

### Test 3: Verify Cookie Persistence
**Objective**: Verify user stays logged in after page refresh

**Steps**:
1. Login (from Test 1)
2. Refresh page (F5)
3. Check if you're still logged in
4. Check DevTools → Cookies for `access_token`

**Expected Result**: ✅ User is still logged in, cookie persists

### Test 4: Logout Clears Cookie
**Objective**: Verify logout deletes the cookie

**Steps**:
1. Login (from Test 1)
2. Go to Profile page
3. Click "Logout" button
4. Check DevTools → Cookies
5. Try to access dashboard

**Expected Result**: ✅ Cookie is deleted, redirected to login

### Test 5: UI/UX - Dark Theme
**Objective**: Verify all pages have consistent monochromatic design

**Pages to Check**:
- [ ] Home page (/) - Dark gradient background, slate cards
- [ ] Login page (/auth/login) - Dark form with slate styling
- [ ] Signup page (/auth/signup) - Dark form with slate styling
- [ ] Dashboard (/dashboard) - Dark theme with post cards
- [ ] Profile (/profile) - Dark theme with user info
- [ ] Post detail (/posts/[id]) - Dark theme with comments
- [ ] Admin (/admin) - Dark theme with tables

**Expected Result**: ✅ All pages have consistent dark monochromatic design

### Test 6: Text Visibility
**Objective**: Verify all text is clearly visible

**Steps**:
1. Visit each page
2. Check that all text is readable
3. Check that buttons are clearly visible
4. Check that form inputs are clearly visible

**Expected Result**: ✅ All text is visible and readable

### Test 7: Engagement Features
**Objective**: Verify likes, comments, and bookmarks work

**Steps**:
1. Login and create a post
2. Go to home page
3. Click on a post
4. Click like button (❤️)
5. Add a comment
6. Click bookmark button (🔖)
7. Delete comment

**Expected Result**: ✅ All engagement features work

### Test 8: Admin Dashboard
**Objective**: Verify admin features work

**Steps**:
1. Create two user accounts
2. Use MongoDB to set one as admin
3. Login as admin
4. Go to /admin
5. Check Analytics tab - should show stats
6. Check Users tab - should list users
7. Check Posts tab - should list posts
8. Check Comments tab - should list comments

**Expected Result**: ✅ Admin dashboard displays all data

### Test 9: Responsive Design
**Objective**: Verify design works on mobile

**Steps**:
1. Open DevTools (F12)
2. Click device toggle (mobile view)
3. Test different screen sizes:
   - iPhone 12 (390x844)
   - iPad (768x1024)
   - Desktop (1920x1080)
4. Check that layout adapts properly

**Expected Result**: ✅ Layout is responsive on all sizes

### Test 10: Error Handling
**Objective**: Verify error messages are displayed correctly

**Steps**:
1. Try to login with wrong password
2. Try to create post without title
3. Try to access admin page as regular user
4. Try to access dashboard without login

**Expected Result**: ✅ Error messages are displayed clearly

## Browser DevTools Checks

### Check Cookies
1. Open DevTools (F12)
2. Go to Application tab
3. Click Cookies
4. Select http://localhost:3000
5. Look for `access_token` cookie
6. Verify it has a value and is httpOnly

### Check Network Requests
1. Open DevTools (F12)
2. Go to Network tab
3. Perform an action (create post, like, etc.)
4. Look for the request
5. Check Request Headers for `Cookie: access_token=...`
6. Check Response Headers for `Set-Cookie` on login

### Check Console
1. Open DevTools (F12)
2. Go to Console tab
3. Perform actions
4. Verify no errors appear
5. Check for any 401 errors

## Troubleshooting

### Issue: 401 Error on Post Creation
**Solution**:
1. Check backend is running on 127.0.0.1:8000
2. Check CORS configuration in backend/app/main.py
3. Verify cookie is being set (check DevTools)
4. Check that `credentials: 'include'` is in fetch calls

### Issue: Cookie Not Being Set
**Solution**:
1. Check backend is setting cookie with correct settings
2. Verify `samesite="lax"` is set
3. Check that response includes `Set-Cookie` header
4. Verify frontend is using `credentials: 'include'`

### Issue: User Logged Out After Refresh
**Solution**:
1. Check that cookie has `max_age=3600`
2. Verify cookie is not being deleted
3. Check browser cookie settings
4. Try clearing cookies and logging in again

### Issue: Dark Theme Not Showing
**Solution**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+Shift+R)
3. Check that Tailwind CSS is loaded
4. Verify no CSS overrides are applied

## Performance Checks

### Page Load Time
1. Open DevTools (F12)
2. Go to Performance tab
3. Reload page
4. Check load time (should be < 3 seconds)

### Bundle Size
1. Run `npm run build` in frontend
2. Check output for bundle sizes
3. Should be around 119-120 kB for First Load JS

### Network Requests
1. Open DevTools (F12)
2. Go to Network tab
3. Reload page
4. Count total requests (should be < 20)
5. Check total size (should be < 500 kB)

## Success Criteria

All tests should pass:
- ✅ Cookies are set and sent correctly
- ✅ No 401 errors on post creation
- ✅ User stays logged in after refresh
- ✅ Logout clears cookie
- ✅ All pages have dark monochromatic design
- ✅ All text is visible and readable
- ✅ Engagement features work
- ✅ Admin dashboard works
- ✅ Responsive design works
- ✅ Error handling works

## Notes

- Backend must be running on `127.0.0.1:8000` (not `localhost`)
- Frontend must be running on `localhost:3000`
- Cookies are automatically sent with `credentials: 'include'`
- No localStorage is used - pure cookie-based auth
- All pages use monochromatic slate color scheme

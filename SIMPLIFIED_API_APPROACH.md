# Simplified API Approach - No api.ts File

## Changes Made

### ✅ Removed
- `frontend/src/lib/api.ts` - Deleted (no longer needed)

### ✅ Updated
- `frontend/src/app/page.tsx` - Calls endpoints directly
- `frontend/src/app/auth/login/page.tsx` - Calls endpoints directly
- `frontend/src/app/auth/signup/page.tsx` - Calls endpoints directly
- `frontend/src/app/dashboard/page.tsx` - Calls endpoints directly

## How It Works Now

### Before (With api.ts)
```typescript
// In page.tsx
import { api } from '@/lib/api';

const result = await api.login(email, password);
```

### After (Direct Calls)
```typescript
// In page.tsx
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const res = await fetch(`${API_BASE}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
  credentials: 'include',
});

const data = await res.json();
```

## Benefits

✅ **Simpler** - No abstraction layer, direct API calls
✅ **Clearer** - See exactly what's being called
✅ **Easier to Debug** - Direct fetch calls are easier to trace
✅ **Less Code** - No need for api.ts file
✅ **Faster** - One less file to load

## Cookie Handling

All fetch calls include `credentials: 'include'` to ensure cookies are sent:

```typescript
const res = await fetch(url, {
  credentials: 'include',  // ✅ This sends cookies
});
```

This is why login now works - the cookie is properly sent with each request.

## API Endpoints Called Directly

### Authentication
```typescript
// Login
fetch(`${API_BASE}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
  credentials: 'include',
})

// Signup
fetch(`${API_BASE}/auth/signup`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
  credentials: 'include',
})

// Get Current User
fetch(`${API_BASE}/auth/me`, {
  credentials: 'include',
})

// Logout
fetch(`${API_BASE}/auth/logout`, {
  method: 'POST',
  credentials: 'include',
})
```

### Posts
```typescript
// Get all posts
fetch(`${API_BASE}/posts`, {
  credentials: 'include',
})

// Get single post
fetch(`${API_BASE}/posts/${id}`, {
  credentials: 'include',
})

// Create post
fetch(`${API_BASE}/posts`, {
  method: 'POST',
  body: formData,  // FormData for file upload
  credentials: 'include',
})

// Update post
fetch(`${API_BASE}/posts/${id}`, {
  method: 'PUT',
  body: formData,
  credentials: 'include',
})

// Delete post
fetch(`${API_BASE}/posts/${id}`, {
  method: 'DELETE',
  credentials: 'include',
})
```

### Comments
```typescript
// Get comments
fetch(`${API_BASE}/posts/${postId}/comments`, {
  credentials: 'include',
})

// Add comment
fetch(`${API_BASE}/posts/${postId}/comments`, {
  method: 'POST',
  body: formData,
  credentials: 'include',
})

// Delete comment
fetch(`${API_BASE}/posts/${postId}/comments/${commentId}`, {
  method: 'DELETE',
  credentials: 'include',
})
```

### Engagement
```typescript
// Like post
fetch(`${API_BASE}/posts/${postId}/like`, {
  method: 'POST',
  credentials: 'include',
})

// Bookmark post
fetch(`${API_BASE}/posts/${postId}/bookmark`, {
  method: 'POST',
  credentials: 'include',
})
```

## Error Handling

Simple error handling in each page:

```typescript
try {
  const res = await fetch(url, options);
  const data = await res.json();

  if (!res.ok) {
    setError(data.detail || 'Request failed');
    return;
  }

  // Success - use data
} catch (err: any) {
  setError(err.message || 'Request failed');
}
```

## Testing

### 1. Restart Frontend
```bash
cd frontend
npm run dev
```

### 2. Test Login
1. Open `http://localhost:3000/auth/login`
2. Enter credentials
3. Click Login
4. Should redirect to dashboard

### 3. Verify Cookie
1. Press F12
2. Application → Cookies → http://localhost:3000
3. Should see `access_token` cookie

### 4. Test Dashboard
1. Should see "My Posts"
2. Should see "New Post" button
3. Should see profile with email

## Files Structure

```
frontend/src/
├── app/
│   ├── page.tsx (home - direct API calls)
│   ├── dashboard/page.tsx (dashboard - direct API calls)
│   ├── profile/page.tsx (profile - direct API calls)
│   ├── admin/page.tsx (admin - direct API calls)
│   ├── posts/[id]/page.tsx (post detail - direct API calls)
│   ├── auth/
│   │   ├── login/page.tsx (login - direct API calls)
│   │   └── signup/page.tsx (signup - direct API calls)
│   └── layout.tsx
└── lib/
    └── (api.ts removed - no longer needed)
```

## Summary

✅ Simpler approach - no api.ts file
✅ Direct fetch calls from pages
✅ Proper cookie handling with `credentials: 'include'`
✅ Cleaner error handling
✅ Easier to debug and maintain

**Ready to test! 🚀**

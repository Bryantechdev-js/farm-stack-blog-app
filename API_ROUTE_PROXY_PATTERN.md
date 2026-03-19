# API Route Proxy Pattern - Technical Deep Dive

## Why We Need API Route Proxies

### The Problem with Next.js Rewrites
```typescript
// ❌ DOESN'T WORK - Rewrites don't forward Set-Cookie
rewrites: async () => {
  return {
    beforeFiles: [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ],
  };
}
```

**Why it fails:**
- Rewrites happen at the server level
- Set-Cookie headers are not forwarded to the browser
- Browser never receives the cookie
- Authentication fails

### The Solution: API Route Proxies
```typescript
// ✅ WORKS - API routes forward Set-Cookie properly
export async function POST(request: NextRequest) {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    body: await request.json(),
  });
  
  const result = NextResponse.json(await response.json());
  
  // Extract and forward Set-Cookie header
  const setCookie = response.headers.get('set-cookie');
  if (setCookie) {
    result.headers.set('set-cookie', setCookie);
  }
  
  return result;
}
```

**Why it works:**
- API routes are actual HTTP endpoints
- We have full control over response headers
- We can extract Set-Cookie from backend
- We can include it in response to browser
- Browser receives and stores cookie

## Implementation Pattern

### 1. Create API Route File
```
frontend/src/app/api/[service]/[...path]/route.ts
```

### 2. Handle All HTTP Methods
```typescript
export async function GET(request, { params }) { ... }
export async function POST(request, { params }) { ... }
export async function PUT(request, { params }) { ... }
export async function DELETE(request, { params }) { ... }
```

### 3. Forward Request to Backend
```typescript
const response = await fetch(`http://localhost:8000/${path}`, {
  method: 'GET',
  headers: {
    'Cookie': request.headers.get('cookie') || '',
  },
  credentials: 'include',
});
```

### 4. Forward Response to Browser
```typescript
const result = NextResponse.json(data, { status: response.status });

// Forward Set-Cookie header
const setCookie = response.headers.get('set-cookie');
if (setCookie) {
  result.headers.set('set-cookie', setCookie);
}

return result;
```

## Complete Example: Auth Proxy

```typescript
// frontend/src/app/api/auth/[...path]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');
  const body = await request.json();

  try {
    // Forward request to backend
    const response = await fetch(`http://localhost:8000/auth/${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      credentials: 'include',
    });

    // Get response data
    const data = await response.json();
    
    // Create response
    const result = NextResponse.json(data, { status: response.status });

    // Forward Set-Cookie header to browser
    const setCookieHeader = response.headers.get('set-cookie');
    if (setCookieHeader) {
      result.headers.set('set-cookie', setCookieHeader);
    }

    return result;
  } catch (error) {
    console.error('Auth proxy error:', error);
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');

  try {
    // Forward request with cookies
    const response = await fetch(`http://localhost:8000/auth/${path}`, {
      method: 'GET',
      headers: {
        'Cookie': request.headers.get('cookie') || '',
      },
      credentials: 'include',
    });

    const data = await response.json();
    const result = NextResponse.json(data, { status: response.status });

    // Forward Set-Cookie header
    const setCookieHeader = response.headers.get('set-cookie');
    if (setCookieHeader) {
      result.headers.set('set-cookie', setCookieHeader);
    }

    return result;
  } catch (error) {
    console.error('Auth proxy error:', error);
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Request Flow Diagram

```
Browser Request
    ↓
POST /api/auth/login
    ↓
Next.js API Route Handler
    ↓
Extract request body
    ↓
Forward to backend: POST http://localhost:8000/auth/login
    ↓
Backend processes request
    ↓
Backend returns: 200 OK + Set-Cookie header
    ↓
API Route receives response
    ↓
Extract Set-Cookie header
    ↓
Create NextResponse with data
    ↓
Include Set-Cookie in response headers
    ↓
Return response to browser
    ↓
Browser receives: 200 OK + Set-Cookie header
    ↓
Browser stores cookie automatically ✅
```

## Cookie Forwarding

### Sending Cookies to Backend
```typescript
const response = await fetch('http://localhost:8000/auth/me', {
  method: 'GET',
  headers: {
    'Cookie': request.headers.get('cookie') || '',
  },
  credentials: 'include',
});
```

### Receiving Cookies from Backend
```typescript
const setCookieHeader = response.headers.get('set-cookie');
if (setCookieHeader) {
  result.headers.set('set-cookie', setCookieHeader);
}
```

## Handling Different Content Types

### JSON
```typescript
const body = await request.json();
const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});
```

### FormData (File Uploads)
```typescript
const body = await request.formData();
const response = await fetch(url, {
  method: 'POST',
  body: body,
  // Don't set Content-Type - browser will set it with boundary
});
```

### Binary (Images)
```typescript
const buffer = await response.arrayBuffer();
return new NextResponse(buffer, {
  status: 200,
  headers: {
    'Content-Type': 'image/jpeg',
    'Cache-Control': 'public, max-age=3600',
  },
});
```

## Error Handling

```typescript
try {
  const response = await fetch(url, { ... });
  
  if (!response.ok) {
    const error = await response.json();
    return NextResponse.json(error, { status: response.status });
  }
  
  const data = await response.json();
  return NextResponse.json(data, { status: 200 });
} catch (error) {
  console.error('Proxy error:', error);
  return NextResponse.json(
    { detail: 'Internal server error' },
    { status: 500 }
  );
}
```

## Performance Considerations

### Caching
```typescript
// Cache static files
return new NextResponse(buffer, {
  headers: {
    'Cache-Control': 'public, max-age=3600',
  },
});
```

### Streaming (for large files)
```typescript
const response = await fetch(url);
return new NextResponse(response.body, {
  status: response.status,
  headers: response.headers,
});
```

## Security Considerations

### ✅ What's Secure
- httpOnly cookies (can't be accessed by JavaScript)
- Cookies only sent over HTTPS in production
- SameSite=Lax prevents CSRF
- API routes validate requests

### ⚠️ What to Watch
- Don't expose sensitive headers
- Validate all inputs
- Rate limit API routes
- Log suspicious activity
- Use HTTPS in production

## Production Deployment

### Update Backend URL
```typescript
const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
const response = await fetch(`${backendUrl}/auth/${path}`, ...);
```

### Environment Variables
```
NEXT_PUBLIC_BACKEND_URL=https://api.example.com
```

### CORS Configuration
```python
# Backend
allow_origins=[
    "https://example.com",
    "https://www.example.com",
]
```

## Advantages of This Pattern

✅ **Proper Cookie Handling** - Set-Cookie headers forwarded correctly
✅ **Same Origin** - All requests appear from same origin
✅ **Full Control** - Can modify headers, handle errors, add logging
✅ **Type Safe** - TypeScript support for request/response
✅ **Flexible** - Can handle any HTTP method and content type
✅ **Scalable** - Works with any backend
✅ **Secure** - httpOnly cookies, no XSS vulnerability

## Disadvantages

❌ **Extra Hop** - Request goes through Next.js before backend
❌ **Latency** - Slightly slower than direct requests
❌ **Complexity** - More code to maintain
❌ **Debugging** - Harder to debug issues

## When to Use This Pattern

✅ **Use when:**
- You need cookie-based authentication
- Backend is on different domain/port
- You need to modify headers
- You need to handle file uploads
- You need to serve static files

❌ **Don't use when:**
- You can use same origin
- You don't need cookies
- You need maximum performance
- You have simple API calls

## Alternative Approaches

### 1. Same Origin (Best)
```
Frontend and Backend on same domain
No proxy needed
Cookies work automatically
```

### 2. CORS with Credentials
```
Frontend: http://localhost:3000
Backend: http://localhost:8000
CORS: allow_credentials=True
Still doesn't forward Set-Cookie properly
```

### 3. Token in LocalStorage (Not Recommended)
```
Vulnerable to XSS attacks
Not secure for sensitive data
```

### 4. API Route Proxy (What We Use)
```
Frontend: http://localhost:3000
API Routes: http://localhost:3000/api/*
Backend: http://localhost:8000
Proper cookie handling
Secure and flexible
```

## Summary

API Route Proxies are the best way to handle cookie-based authentication in Next.js when your backend is on a different domain/port. They provide:

- ✅ Proper cookie forwarding
- ✅ Same origin for browser
- ✅ Full control over requests/responses
- ✅ Security and flexibility
- ✅ Easy to implement and maintain

This pattern is used by many production applications and is the recommended approach for Next.js + separate backend architecture.

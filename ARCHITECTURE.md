# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User's Browser                           │
│                   http://localhost:3000                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    Next.js Frontend                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Pages:                                                   │  │
│  │ - / (redirects to /dashboard)                           │  │
│  │ - /auth/login                                           │  │
│  │ - /auth/signup                                          │  │
│  │ - /dashboard (main page)                                │  │
│  │ - /posts/[id] (post detail)                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ API Client (src/lib/api.ts):                            │  │
│  │ - Handles all HTTP requests                             │  │
│  │ - Manages cookies automatically                         │  │
│  │ - Type-safe responses                                   │  │
│  │ - Error handling                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             │ (with cookies)
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend                              │
│              http://127.0.0.1:8000                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ API Endpoints:                                           │  │
│  │ - POST /auth/signup                                      │  │
│  │ - POST /auth/login                                       │  │
│  │ - GET /posts                                             │  │
│  │ - GET /posts/{id}                                        │  │
│  │ - POST /posts (create)                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Core Components:                                         │  │
│  │ - Security (JWT, password hashing)                       │  │
│  │ - Middleware (auth validation)                           │  │
│  │ - CORS (cross-origin requests)                           │  │
│  │ - Logging                                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Async Queries
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    MongoDB Database                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Collections:                                             │  │
│  │ - users (email, password_hash, role)                     │  │
│  │ - posts (title, content, image, created_at)             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      SIGNUP FLOW                                │
└─────────────────────────────────────────────────────────────────┘

User Input (email, password)
         │
         ▼
Frontend Validation
         │
         ▼
POST /auth/signup
         │
         ▼
Backend Validation
         │
         ▼
Hash Password (bcrypt)
         │
         ▼
Store in MongoDB
         │
         ▼
Return Success Message
         │
         ▼
Redirect to Login


┌─────────────────────────────────────────────────────────────────┐
│                      LOGIN FLOW                                 │
└─────────────────────────────────────────────────────────────────┘

User Input (email, password)
         │
         ▼
POST /auth/login
         │
         ▼
Find User in MongoDB
         │
         ▼
Verify Password (bcrypt)
         │
         ▼
Create JWT Token
         │
         ▼
Set httpOnly Cookie
         │
         ▼
Return Success Message
         │
         ▼
Redirect to Dashboard


┌─────────────────────────────────────────────────────────────────┐
│                   AUTHENTICATED REQUEST FLOW                    │
└─────────────────────────────────────────────────────────────────┘

Frontend Request
         │
         ▼
Include Cookie (automatic)
         │
         ▼
POST /posts (with cookie)
         │
         ▼
Backend Middleware
         │
         ▼
Extract Token from Cookie
         │
         ▼
Validate JWT Signature
         │
         ▼
Check Token Expiration
         │
         ▼
Extract User ID
         │
         ▼
Process Request
         │
         ▼
Return Response
```

## Data Flow - Create Post

```
┌─────────────────────────────────────────────────────────────────┐
│                    CREATE POST FLOW                             │
└─────────────────────────────────────────────────────────────────┘

User fills form:
- Title
- Content
- Image file
         │
         ▼
Frontend Validation
         │
         ▼
Create FormData
         │
         ▼
POST /posts (multipart/form-data)
         │
         ▼
Backend receives request
         │
         ▼
Validate authentication
         │
         ▼
Sanitize HTML content (bleach)
         │
         ▼
Save image to disk
         │
         ▼
Create post document:
{
  title: "...",
  content: "...",
  image: "uploads/...",
  created_at: "..."
}
         │
         ▼
Insert into MongoDB
         │
         ▼
Return post ID
         │
         ▼
Frontend fetches updated posts
         │
         ▼
Display in dashboard
```

## Component Structure

### Backend Structure

```
backend/
├── app/
│   ├── main.py
│   │   ├── FastAPI app initialization
│   │   ├── CORS middleware
│   │   ├── Auth middleware
│   │   └── Router includes
│   │
│   ├── api/
│   │   ├── auth.py
│   │   │   ├── signup endpoint
│   │   │   └── login endpoint
│   │   │
│   │   └── posts.py
│   │       ├── create post endpoint
│   │       ├── get all posts endpoint
│   │       └── get single post endpoint
│   │
│   ├── core/
│   │   ├── security.py
│   │   │   ├── hash_password()
│   │   │   ├── verify_password()
│   │   │   └── create_token()
│   │   │
│   │   ├── middleware.py
│   │   │   └── auth_middleware()
│   │   │
│   │   └── logging.py
│   │       └── setup_logging()
│   │
│   ├── db/
│   │   └── mongo.py
│   │       ├── MongoDB client
│   │       └── db connection
│   │
│   └── models/
│       └── user.py
│           └── UserCreate schema
│
├── .env (MongoDB URL)
├── requirements.txt
└── Dockerfile
```

### Frontend Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx
│   │   │   └── Home (redirects to dashboard)
│   │   │
│   │   ├── layout.tsx
│   │   │   └── Root layout
│   │   │
│   │   ├── globals.css
│   │   │   └── Global styles
│   │   │
│   │   ├── auth/
│   │   │   ├── login/page.tsx
│   │   │   │   └── Login page
│   │   │   │
│   │   │   └── signup/page.tsx
│   │   │       └── Signup page
│   │   │
│   │   ├── dashboard/page.tsx
│   │   │   ├── Post listing
│   │   │   └── Post creation form
│   │   │
│   │   └── posts/
│   │       └── [id]/page.tsx
│   │           └── Post detail page
│   │
│   └── lib/
│       └── api.ts
│           ├── getPosts()
│           ├── getPost()
│           ├── createPost()
│           ├── signup()
│           └── login()
│
├── .env.local (API URL)
├── package.json
└── tsconfig.json
```

## Request/Response Examples

### Signup Request

```
POST /auth/signup HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "User created successfully"
}
```

### Login Request

```
POST /auth/login HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...; HttpOnly; SameSite=Lax

{
  "message": "Login successful"
}
```

### Create Post Request

```
POST /posts HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Cookie: access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

------WebKitFormBoundary
Content-Disposition: form-data; name="title"

My Blog Post
------WebKitFormBoundary
Content-Disposition: form-data; name="content"

This is my blog post content
------WebKitFormBoundary
Content-Disposition: form-data; name="image"; filename="image.jpg"
Content-Type: image/jpeg

[binary image data]
------WebKitFormBoundary--

HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "507f1f77bcf86cd799439012",
  "message": "Post created"
}
```

### Get Posts Request

```
GET /posts HTTP/1.1
Host: 127.0.0.1:8000
Cookie: access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": "507f1f77bcf86cd799439011",
    "title": "My First Post",
    "content": "This is my first blog post",
    "image": "uploads/image.jpg"
  },
  {
    "id": "507f1f77bcf86cd799439012",
    "title": "My Second Post",
    "content": "This is my second blog post",
    "image": "uploads/image2.jpg"
  }
]
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                              │
└─────────────────────────────────────────────────────────────────┘

Layer 1: HTTPS/TLS
├── Encrypts data in transit
└── Prevents man-in-the-middle attacks

Layer 2: CORS
├── Restricts requests to known origins
└── Prevents unauthorized cross-origin requests

Layer 3: Authentication
├── JWT tokens
├── httpOnly cookies
└── Token expiration (1 hour)

Layer 4: Authorization
├── Auth middleware
├── Token validation
└── User identification

Layer 5: Input Validation
├── Pydantic schemas
├── Email validation
└── Password requirements

Layer 6: Data Protection
├── Password hashing (bcrypt)
├── HTML sanitization (bleach)
└── Environment variables for secrets

Layer 7: Database Security
├── MongoDB authentication
├── IP whitelist (Atlas)
└── Encrypted connections
```

## Deployment Architecture (Docker)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKER DEPLOYMENT                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Docker Host                                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Nginx Container (Port 80)                                │  │
│  │ ├── Reverse proxy                                        │  │
│  │ ├── Route /api/* → Backend                               │  │
│  │ └── Route /* → Frontend                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Frontend Container (Port 3000)                           │  │
│  │ ├── Next.js app                                          │  │
│  │ └── Serves static files                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Backend Container (Port 8000)                            │  │
│  │ ├── FastAPI app                                          │  │
│  │ └── API endpoints                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ MongoDB Container (Port 27017)                           │  │
│  │ ├── Database                                             │  │
│  │ └── Data persistence                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
Frontend:
├── Next.js 15 (React framework)
├── TypeScript (type safety)
├── Tailwind CSS (styling)
└── React Hooks (state management)

Backend:
├── FastAPI (web framework)
├── Pydantic (data validation)
├── Motor (async MongoDB driver)
├── PyJWT (JWT tokens)
├── Passlib (password hashing)
└── Bleach (HTML sanitization)

Database:
├── MongoDB (NoSQL database)
└── Motor (async driver)

DevOps:
├── Docker (containerization)
├── Docker Compose (orchestration)
├── Nginx (reverse proxy)
└── Git (version control)
```

---

This architecture provides:
- ✅ Scalability
- ✅ Security
- ✅ Maintainability
- ✅ Performance
- ✅ Reliability

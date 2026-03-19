# FARM Stack Blog App - Setup Guide

## Architecture Overview

This is a full-stack blog application using:
- **F**astAPI (Backend)
- **A**sync MongoDB (Database)
- **R**eact/Next.js (Frontend)
- **M**ongo (Database)

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   └── posts.py      # Blog posts endpoints
│   │   ├── core/
│   │   │   ├── security.py   # JWT & password hashing
│   │   │   ├── middleware.py # Auth middleware
│   │   │   └── logging.py    # Logging setup
│   │   ├── db/
│   │   │   └── mongo.py      # MongoDB connection
│   │   ├── models/
│   │   │   └── user.py       # User schema
│   │   └── main.py           # FastAPI app
│   ├── nginx/
│   │   └── nginx.conf        # Reverse proxy config
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── page.tsx              # Home (redirects to dashboard)
    │   │   ├── layout.tsx            # Root layout
    │   │   ├── globals.css           # Global styles
    │   │   ├── auth/
    │   │   │   ├── login/page.tsx    # Login page
    │   │   │   └── signup/page.tsx   # Signup page
    │   │   ├── dashboard/page.tsx    # Main dashboard
    │   │   └── posts/
    │   │       └── [id]/page.tsx     # Post detail page
    │   └── lib/
    │       └── api.ts                # API client
    ├── .env.local
    ├── package.json
    └── tsconfig.json
```

## Backend API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/login` - Login user (sets httpOnly cookie)

### Posts
- `GET /api/posts` - Get all posts
- `GET /api/posts/{id}` - Get single post
- `POST /api/posts` - Create new post (requires auth)

## Frontend Pages

- `/` - Redirects to dashboard
- `/auth/login` - Login page
- `/auth/signup` - Signup page
- `/dashboard` - Main dashboard (list posts, create new)
- `/posts/[id]` - Post detail page

## Running the Application

### Option 1: Docker Compose (Recommended)

```bash
cd backend
docker-compose up
```

This starts:
- MongoDB on port 27017
- FastAPI backend on port 8000
- Next.js frontend on port 3000
- Nginx reverse proxy on port 80

Access the app at `http://localhost`

### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**MongoDB:**
```bash
# Make sure MongoDB is running locally on port 27017
mongod
```

## Frontend-Backend Integration

### API Client (`frontend/src/lib/api.ts`)

The API client handles:
- Base URL configuration via `NEXT_PUBLIC_API_URL`
- Automatic cookie inclusion for auth
- Error handling
- Type-safe responses

### Environment Variables

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost/api
```

For production, update to your domain:
```
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
```

## Nginx Configuration

The nginx reverse proxy routes:
- `/api/*` → FastAPI backend (port 8000)
- `/*` → Next.js frontend (port 3000)

Key features:
- Proper header forwarding (Host, X-Real-IP, X-Forwarded-For)
- Cookie path handling for auth
- 10MB file upload limit

## Authentication Flow

1. User signs up/logs in
2. Backend validates credentials and creates JWT token
3. Token stored in httpOnly cookie (secure, not accessible via JS)
4. Frontend includes cookie automatically in requests
5. Backend middleware validates token on protected routes
6. Invalid/missing token redirects to login

## Creating a Blog Post

1. Navigate to `/dashboard`
2. Click "New Post"
3. Fill in title, content, and upload image
4. Click "Publish Post"
5. Post appears in the feed immediately

## Security Features

- Password hashing with bcrypt
- JWT tokens with 1-hour expiration
- httpOnly cookies (CSRF protection)
- HTML sanitization with bleach
- CORS configured for frontend origin
- Auth middleware on protected routes

## Troubleshooting

### Posts not loading
- Check MongoDB connection in backend logs
- Verify API URL in frontend `.env.local`
- Check browser console for CORS errors

### Login not working
- Ensure cookies are enabled
- Check that secure=False in development (set to True in production)
- Verify JWT secret is consistent

### Image uploads failing
- Check file permissions in uploads directory
- Verify nginx client_max_body_size is set to 10M
- Check file size doesn't exceed limit

## Next Steps

- Add post editing/deletion
- Add user profiles
- Add comments system
- Add search functionality
- Add pagination
- Deploy to production

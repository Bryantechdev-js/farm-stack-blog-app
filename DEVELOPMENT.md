# Development Guide - FARM Stack Blog

## Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB (local or Atlas)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your MongoDB URL
# Copy from .env.example and update MONGO_URL
cp .env.example .env

# Run the backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: `http://127.0.0.1:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Run the frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/blog?appName=Cluster0
```

**Important:** Never commit `.env` to git. It contains sensitive credentials.

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

**Note:** `NEXT_PUBLIC_` prefix means this variable is exposed to the browser. Only use it for non-sensitive URLs. The MongoDB URL stays in the backend `.env` and is never exposed to the frontend.

## API Endpoints

All endpoints are prefixed with the `API_BASE` URL.

### Authentication
- `POST /auth/signup` - Register new user
  ```json
  { "email": "user@example.com", "password": "password123" }
  ```
- `POST /auth/login` - Login user
  ```json
  { "email": "user@example.com", "password": "password123" }
  ```

### Posts
- `GET /posts` - Get all posts
- `GET /posts/{id}` - Get single post
- `POST /posts` - Create post (multipart form data)
  ```
  title: string
  content: string
  image: File
  ```

## Testing the API

### Using cURL

**Signup:**
```bash
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Get Posts:**
```bash
curl http://127.0.0.1:8000/posts \
  -b cookies.txt
```

### Using Postman

1. Create a POST request to `http://127.0.0.1:8000/auth/login`
2. Set body to JSON with email and password
3. In the response, check the `Set-Cookie` header
4. Copy the `access_token` value
5. For authenticated requests, add it to Cookies

## Frontend-Backend Communication

### How It Works

1. **Frontend** (`frontend/src/lib/api.ts`) - API client that:
   - Uses `NEXT_PUBLIC_API_URL` environment variable
   - Automatically includes credentials (cookies) in requests
   - Handles errors and returns typed responses

2. **Backend** (`backend/app/main.py`) - FastAPI server that:
   - Loads `MONGO_URL` from `.env` file
   - Configures CORS to allow frontend origins
   - Sets httpOnly cookies for authentication
   - Validates JWT tokens on protected routes

3. **Nginx** (Docker only) - Reverse proxy that:
   - Routes `/api/*` to backend
   - Routes `/*` to frontend
   - Forwards headers properly

### Development vs Production

**Development:**
- Frontend: `http://localhost:3000`
- Backend: `http://127.0.0.1:8000`
- Frontend calls backend directly
- CORS enabled for localhost

**Production (Docker):**
- Frontend: `http://localhost:3000` (via nginx)
- Backend: `http://backend:8000` (internal)
- Frontend calls backend via nginx at `/api`
- Update `NEXT_PUBLIC_API_URL=http://localhost/api`

## Common Issues

### "Failed to fetch" Error
- Check backend is running: `http://127.0.0.1:8000/docs`
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors
- Ensure credentials are included in fetch requests

### MongoDB Connection Error
- Verify `MONGO_URL` in `.env`
- Check MongoDB is running (local) or accessible (Atlas)
- Test connection: `mongosh "mongodb+srv://..."`

### Cookies Not Being Set
- Check backend response headers for `Set-Cookie`
- Ensure `credentials: 'include'` in fetch requests
- In development, `secure=False` in cookies (set to `True` in production)

### Image Upload Fails
- Check file size (nginx limit is 10MB)
- Verify `uploads/` directory exists and is writable
- Check file permissions

## Debugging

### Backend Logs
```bash
# With reload enabled, you'll see logs in terminal
uvicorn app.main:app --reload
```

### Frontend Logs
```bash
# Check browser console (F12)
# Check terminal where `npm run dev` is running
```

### Database Inspection
```bash
# Connect to MongoDB
mongosh "your-connection-string"

# List databases
show dbs

# Use blog database
use blog

# List collections
show collections

# View users
db.users.find()

# View posts
db.posts.find()
```

## File Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py       # Auth endpoints
│   │   └── posts.py      # Post endpoints
│   ├── core/
│   │   ├── security.py   # JWT & password hashing
│   │   ├── middleware.py # Auth middleware
│   │   └── logging.py    # Logging setup
│   ├── db/
│   │   └── mongo.py      # MongoDB connection
│   ├── models/
│   │   └── user.py       # User schema
│   └── main.py           # FastAPI app
├── .env                  # Environment variables (not in git)
├── .env.example          # Example env file
├── requirements.txt      # Python dependencies
└── Dockerfile

frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Home page
│   │   ├── layout.tsx            # Root layout
│   │   ├── globals.css           # Global styles
│   │   ├── auth/
│   │   │   ├── login/page.tsx
│   │   │   └── signup/page.tsx
│   │   ├── dashboard/page.tsx    # Main dashboard
│   │   └── posts/
│   │       └── [id]/page.tsx     # Post detail
│   └── lib/
│       └── api.ts                # API client
├── .env.local            # Environment variables (not in git)
├── .env.example          # Example env file
├── package.json
└── tsconfig.json
```

## Next Steps

- Add post editing/deletion
- Add user profiles
- Add comments system
- Add search functionality
- Add pagination
- Add rate limiting
- Add email verification
- Deploy to production

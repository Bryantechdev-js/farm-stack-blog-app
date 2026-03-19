# Quick Start - Complete FARM Stack Blog

## Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB Atlas account
- Backend running at `http://127.0.0.1:8000`
- Frontend running at `http://localhost:3000`

## 1. Backend Setup

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Configure Environment
File: `backend/.env`
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0
```

### Start Backend
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: `http://127.0.0.1:8000`
API Docs: `http://127.0.0.1:8000/docs`

## 2. Frontend Setup

### Install Dependencies
```bash
cd frontend
npm install
```

### Configure Environment
File: `frontend/.env.local`
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### Start Frontend
```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 3. Test the Application

### Create Test Account
1. Open `http://localhost:3000`
2. Click "Sign Up"
3. Enter email: `test@example.com`
4. Enter password: `TestPassword123`
5. Click "Sign Up"

### Login
1. Click "Login"
2. Enter same credentials
3. Click "Login"

### Create a Post
1. Click "Dashboard"
2. Click "New Post"
3. Fill in:
   - Title: "My First Post"
   - Content: "This is my first blog post"
   - Image: Select any image file
4. Click "Publish Post"

### View Posts
1. Click "Home" or logo
2. See all posts in grid
3. Click on any post to view details
4. Add comments
5. Like and bookmark posts

### Admin Features
1. Create another user with admin role (via database)
2. Login as admin
3. Click "Admin" button
4. View analytics, manage users/posts/comments

## 4. Key Features

### For Users
- ✅ Sign up and login
- ✅ Create, edit, delete posts
- ✅ Comment on posts
- ✅ Like and bookmark posts
- ✅ View profile
- ✅ Logout

### For Admins
- ✅ View system analytics
- ✅ Manage all users (change role, delete)
- ✅ Manage all posts (delete)
- ✅ Manage all comments (delete)
- ✅ View engagement metrics

## 5. API Endpoints

### Authentication
```
POST   /auth/signup          - Create account
POST   /auth/login           - Login (sets cookie)
POST   /auth/logout          - Logout
GET    /auth/me              - Get current user
```

### Posts
```
GET    /posts                - Get all posts
GET    /posts/{id}           - Get single post
POST   /posts                - Create post
PUT    /posts/{id}           - Update post
DELETE /posts/{id}           - Delete post
```

### Comments
```
GET    /posts/{id}/comments           - Get comments
POST   /posts/{id}/comments           - Add comment
DELETE /posts/{id}/comments/{cid}     - Delete comment
```

### Engagement
```
POST   /posts/{id}/like               - Toggle like
POST   /posts/{id}/bookmark           - Toggle bookmark
```

### Admin
```
GET    /admin/users                   - Get all users
PUT    /admin/users/{id}/role         - Change role
DELETE /admin/users/{id}              - Delete user
GET    /admin/posts                   - Get all posts
DELETE /admin/posts/{id}              - Delete post
GET    /admin/comments                - Get all comments
DELETE /admin/comments/{id}           - Delete comment
GET    /admin/analytics               - Get analytics
```

## 6. Frontend Routes

```
/                    - Home (all posts)
/auth/login          - Login page
/auth/signup         - Signup page
/dashboard           - User's posts (CRUD)
/profile             - User profile
/posts/[id]          - Post detail + comments
/admin               - Admin dashboard
```

## 7. Database Collections

### users
```javascript
{
  _id: ObjectId,
  email: String,
  password: String (Argon2),
  role: String ("user" or "admin"),
  created_at: DateTime
}
```

### posts
```javascript
{
  _id: ObjectId,
  title: String,
  content: String,
  image: String,
  author_id: ObjectId,
  author_email: String,
  created_at: DateTime,
  updated_at: DateTime,
  likes: [ObjectId],
  bookmarks: [ObjectId],
  comments_count: Number
}
```

### comments
```javascript
{
  _id: ObjectId,
  post_id: ObjectId,
  user_id: ObjectId,
  user_email: String,
  content: String,
  created_at: DateTime
}
```

## 8. Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version

# Check MongoDB connection
cd backend
python test_mongo_simple.py

# Check environment variables
cd backend
python check_env.py
```

### Frontend won't connect to backend
```bash
# Verify backend is running
curl http://127.0.0.1:8000/health

# Check frontend environment
# In browser console: console.log(process.env.NEXT_PUBLIC_API_URL)

# Restart frontend dev server
cd frontend
npm run dev
```

### Upload errors
```bash
# Verify uploads directory exists
ls -la backend/uploads/

# Create if missing
mkdir -p backend/uploads
```

### MongoDB connection errors
```bash
# Check connection string in .env
cat backend/.env

# Test connection
cd backend
python test_mongo_simple.py
```

## 9. Production Deployment

### Backend (Heroku/Railway/Render)
```bash
# Set environment variables
MONGO_URL=your_production_mongodb_url

# Deploy
git push heroku main
```

### Frontend (Vercel/Netlify)
```bash
# Set environment variables
NEXT_PUBLIC_API_URL=https://your-backend-url.com

# Deploy
npm run build
# Deploy build folder
```

## 10. Security Checklist

- ✅ Change SECRET in `backend/app/core/security.py` for production
- ✅ Set `secure=True` for cookies in production (HTTPS only)
- ✅ Use environment variables for all secrets
- ✅ Enable HTTPS on production
- ✅ Add rate limiting
- ✅ Add request logging
- ✅ Use cloud storage for uploads (S3, GCS)
- ✅ Add CSRF protection
- ✅ Add input validation
- ✅ Add monitoring/alerting

## 11. Performance Tips

- Add pagination to posts (currently loads all)
- Add search functionality
- Add image optimization
- Add caching (Redis)
- Add database indexes
- Add CDN for static files
- Add compression middleware
- Monitor database queries

## 12. Support

For issues or questions:
1. Check browser console (F12)
2. Check backend console logs
3. Check MongoDB connection
4. Review error messages
5. Check API documentation at `/docs`

## 13. Next Steps

1. ✅ Test all features
2. ✅ Create test data
3. ✅ Verify admin dashboard
4. ✅ Test file uploads
5. ✅ Test comments and engagement
6. ✅ Deploy to production
7. ✅ Set up monitoring
8. ✅ Add more features as needed

---

**You're all set! Start building your blog! 🚀**

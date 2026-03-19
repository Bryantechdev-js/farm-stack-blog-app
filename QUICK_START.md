# Quick Start Guide - FARM Stack Blog Application

## Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB (local or cloud)
- npm or yarn

## Setup Instructions

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

# Create .env file with MongoDB connection
# Copy from .env.example and update with your MongoDB URL
cp .env.example .env

# Run the backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > .env.local

# Run development server
npm run dev

# Or build for production
npm run build
npm start
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## Test Credentials

Create a test account:
1. Go to http://localhost:3000/auth/signup
2. Enter email and password (min 8 characters)
3. Click Sign Up
4. Login with your credentials

## Features to Test

### User Features
- ✅ Sign up and login
- ✅ Create blog posts with images
- ✅ Edit and delete your posts
- ✅ View all blog posts on home page
- ✅ Like/unlike posts
- ✅ Bookmark/unbookmark posts
- ✅ Comment on posts
- ✅ Delete your comments
- ✅ View your profile
- ✅ Logout

### Admin Features (Create admin user first)
1. Create a regular user account
2. Use MongoDB to update user role to "admin"
3. Login and access admin dashboard at `/admin`
4. Manage users, posts, and comments
5. View analytics and statistics

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/blog_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Troubleshooting

### Cookies Not Being Set
- Ensure backend is running on `127.0.0.1:8000` (not `localhost`)
- Check CORS configuration in `backend/app/main.py`
- Verify `credentials: 'include'` is set in all fetch calls

### MongoDB Connection Issues
- Check MongoDB URL format: `mongodb+srv://username:password@cluster.mongodb.net/database`
- Ensure IP whitelist includes your machine
- Verify credentials are correct

### Build Errors
- Clear `.next` folder: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Run build again: `npm run build`

## Project Structure

```
farm_stack_blog/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── posts.py
│   │   │   └── admin.py
│   │   ├── core/
│   │   │   ├── security.py
│   │   │   ├── middleware.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   └── mongo.py
│   │   ├── models/
│   │   │   └── user.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── auth/
│   │   │   ├── posts/
│   │   │   ├── admin/
│   │   │   ├── dashboard/
│   │   │   ├── profile/
│   │   │   ├── page.tsx (home)
│   │   │   └── layout.tsx
│   │   └── globals.css
│   ├── package.json
│   └── .env.local
└── README.md
```

## API Endpoints Reference

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user

### Posts
- `GET /posts` - Get all posts
- `GET /posts/{id}` - Get single post
- `POST /posts` - Create post (multipart/form-data)
- `PUT /posts/{id}` - Update post (multipart/form-data)
- `DELETE /posts/{id}` - Delete post

### Comments
- `GET /posts/{id}/comments` - Get post comments
- `POST /posts/{id}/comments` - Add comment
- `DELETE /posts/{id}/comments/{comment_id}` - Delete comment

### Engagement
- `POST /posts/{id}/like` - Toggle like
- `POST /posts/{id}/bookmark` - Toggle bookmark

### Admin
- `GET /admin/analytics` - Get analytics
- `GET /admin/users` - Get all users
- `GET /admin/posts` - Get all posts
- `GET /admin/comments` - Get all comments
- `DELETE /admin/users/{id}` - Delete user
- `PUT /admin/users/{id}/role` - Update user role
- `DELETE /admin/comments/{id}` - Delete comment

## Performance Tips

1. **Image Optimization**: Consider using Next.js Image component for better performance
2. **Caching**: Implement Redis for session caching
3. **Database Indexing**: Add indexes on frequently queried fields
4. **Pagination**: Implement pagination for large datasets
5. **Lazy Loading**: Load comments and engagement data on demand

## Security Considerations

- ✅ Passwords hashed with Argon2
- ✅ JWT tokens for authentication
- ✅ httpOnly cookies for token storage
- ✅ CORS properly configured
- ✅ Role-based access control
- ✅ Input validation on backend

## Support

For issues or questions, check:
1. Backend logs: `uvicorn` console output
2. Frontend logs: Browser console (F12)
3. MongoDB connection: Check Atlas dashboard
4. CORS errors: Check browser Network tab

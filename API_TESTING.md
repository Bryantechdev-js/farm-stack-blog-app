# API Testing Guide

## Using cURL

### 1. Signup

```bash
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "message": "User created successfully"
}
```

### 2. Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "message": "Login successful"
}
```

**Note:** The `-c cookies.txt` flag saves the authentication cookie to a file.

### 3. Get All Posts

```bash
curl http://127.0.0.1:8000/posts \
  -b cookies.txt
```

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "title": "My First Post",
    "content": "This is my first blog post",
    "image": "uploads/image.jpg"
  }
]
```

### 4. Get Single Post

```bash
curl http://127.0.0.1:8000/posts/507f1f77bcf86cd799439011 \
  -b cookies.txt
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "My First Post",
  "content": "This is my first blog post",
  "image": "uploads/image.jpg"
}
```

### 5. Create Post

```bash
curl -X POST http://127.0.0.1:8000/posts \
  -b cookies.txt \
  -F "title=My Blog Post" \
  -F "content=This is the content of my blog post" \
  -F "image=@/path/to/image.jpg"
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439012",
  "message": "Post created"
}
```

## Using Postman

### Setup

1. Open Postman
2. Create a new collection called "Blog API"
3. Create environment variables:
   - `base_url` = `http://127.0.0.1:8000`
   - `token` = (will be set after login)

### 1. Signup Request

**Method:** POST
**URL:** `{{base_url}}/auth/signup`
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### 2. Login Request

**Method:** POST
**URL:** `{{base_url}}/auth/login`
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**After Response:**
- Go to "Cookies" tab
- Copy the `access_token` value
- Set environment variable: `token` = `<copied_token>`

### 3. Get All Posts

**Method:** GET
**URL:** `{{base_url}}/posts`
**Headers:**
```
Cookie: access_token={{token}}
```

### 4. Get Single Post

**Method:** GET
**URL:** `{{base_url}}/posts/507f1f77bcf86cd799439011`
**Headers:**
```
Cookie: access_token={{token}}
```

### 5. Create Post

**Method:** POST
**URL:** `{{base_url}}/posts`
**Headers:**
```
Cookie: access_token={{token}}
```
**Body (form-data):**
```
title: My Blog Post
content: This is the content
image: <select image file>
```

## Using JavaScript/Fetch

### Signup

```javascript
const response = await fetch('http://127.0.0.1:8000/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  }),
  credentials: 'include'
});
const data = await response.json();
console.log(data);
```

### Login

```javascript
const response = await fetch('http://127.0.0.1:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  }),
  credentials: 'include'
});
const data = await response.json();
console.log(data);
```

### Get Posts

```javascript
const response = await fetch('http://127.0.0.1:8000/posts', {
  credentials: 'include'
});
const posts = await response.json();
console.log(posts);
```

### Create Post

```javascript
const formData = new FormData();
formData.append('title', 'My Blog Post');
formData.append('content', 'This is the content');
formData.append('image', fileInput.files[0]);

const response = await fetch('http://127.0.0.1:8000/posts', {
  method: 'POST',
  body: formData,
  credentials: 'include'
});
const data = await response.json();
console.log(data);
```

## Using Python Requests

```python
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'
session = requests.Session()

# Signup
response = session.post(f'{BASE_URL}/auth/signup', json={
    'email': 'user@example.com',
    'password': 'password123'
})
print(response.json())

# Login
response = session.post(f'{BASE_URL}/auth/login', json={
    'email': 'user@example.com',
    'password': 'password123'
})
print(response.json())

# Get posts
response = session.get(f'{BASE_URL}/posts')
print(response.json())

# Create post
with open('image.jpg', 'rb') as f:
    files = {'image': f}
    data = {
        'title': 'My Blog Post',
        'content': 'This is the content'
    }
    response = session.post(f'{BASE_URL}/posts', files=files, data=data)
    print(response.json())
```

## API Documentation

### Interactive API Docs

Visit `http://127.0.0.1:8000/docs` in your browser to see:
- All available endpoints
- Request/response schemas
- Try out endpoints directly
- See example requests

### Alternative Docs

Visit `http://127.0.0.1:8000/redoc` for ReDoc documentation.

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already exists"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Post not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

## Testing Workflow

### 1. Test Authentication
```bash
# Signup
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"test@example.com","password":"test123"}'
```

### 2. Test Posts
```bash
# Get posts (should be empty)
curl http://127.0.0.1:8000/posts -b cookies.txt

# Create post
curl -X POST http://127.0.0.1:8000/posts \
  -b cookies.txt \
  -F "title=Test Post" \
  -F "content=Test content" \
  -F "image=@test.jpg"

# Get posts (should show new post)
curl http://127.0.0.1:8000/posts -b cookies.txt
```

### 3. Test Frontend Integration
1. Open `http://localhost:3000`
2. Sign up with test account
3. Create a blog post
4. Verify post appears in dashboard
5. Click post to view details
6. Refresh page (verify authentication persists)

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test GET /posts endpoint
ab -n 100 -c 10 http://127.0.0.1:8000/posts

# Test with authentication
ab -n 100 -c 10 -C "access_token=<token>" http://127.0.0.1:8000/posts
```

### Load Testing with wrk

```bash
# Install wrk: https://github.com/wg/wrk

# Test GET /posts
wrk -t4 -c100 -d30s http://127.0.0.1:8000/posts

# Test with script for authentication
wrk -t4 -c100 -d30s -s script.lua http://127.0.0.1:8000/posts
```

## Debugging Tips

### Enable Verbose Output

**cURL:**
```bash
curl -v http://127.0.0.1:8000/posts
```

**Python:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Response Headers

```bash
curl -i http://127.0.0.1:8000/posts
```

### Monitor Network Traffic

1. Open browser DevTools (F12)
2. Go to Network tab
3. Perform actions
4. Check request/response details

### Check Backend Logs

Look at terminal where backend is running for:
- Request logs
- Error messages
- Database queries
- Authentication attempts

## Common Issues

### CORS Error
```
Access to XMLHttpRequest at 'http://127.0.0.1:8000/...' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution:** Ensure CORS is configured in `backend/app/main.py`

### Cookie Not Being Set
- Check `Set-Cookie` header in response
- Ensure `credentials: 'include'` in fetch requests
- Check browser cookie settings

### 401 Unauthorized
- Verify token is being sent
- Check token hasn't expired (1 hour)
- Try logging in again

### Image Upload Fails
- Check file size (max 10MB)
- Verify file format is image
- Check `uploads/` directory exists
- Check file permissions

---

**Happy testing!** 🧪

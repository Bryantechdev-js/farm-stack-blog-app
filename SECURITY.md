# Security Configuration

## Environment Variables

### Backend (.env) - NEVER expose to frontend
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/blog
```

**Why?** Contains database credentials. Only backend needs this.

### Frontend (.env.local) - Safe to expose
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

**Why?** Only contains the API URL, no credentials. The `NEXT_PUBLIC_` prefix means it's embedded in the browser bundle.

## Authentication Flow

1. **Signup/Login**: User sends email + password to backend
2. **Password Hashing**: Backend hashes password with bcrypt before storing
3. **JWT Token**: Backend creates JWT token with user ID and role
4. **Cookie Storage**: Token stored in httpOnly cookie (not accessible via JavaScript)
5. **Request Validation**: Backend validates token on protected routes
6. **Token Expiration**: Tokens expire after 1 hour

## Security Features

### ✅ Password Security
- Passwords hashed with bcrypt (not reversible)
- Passwords never stored in plain text
- Passwords never sent to frontend

### ✅ Cookie Security
- httpOnly flag: JavaScript cannot access the cookie
- Prevents XSS attacks from stealing tokens
- Automatically sent with requests (credentials: 'include')

### ✅ CORS Configuration
```python
allow_origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://frontend:3000",
]
```
- Only allows requests from known frontend origins
- Prevents unauthorized cross-origin requests

### ✅ HTML Sanitization
```python
safe_content = bleach.clean(content)
```
- Removes malicious HTML/JavaScript from post content
- Prevents XSS attacks through user-generated content

### ✅ JWT Validation
- Tokens signed with SECRET key
- Backend verifies signature on each request
- Invalid/expired tokens rejected

## Production Checklist

### Before Deploying

- [ ] Change `SECRET` in `backend/app/core/security.py` to a strong random string
- [ ] Set `secure=True` in cookies (requires HTTPS)
- [ ] Update CORS origins to your production domain
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL certificate
- [ ] Set strong MongoDB password
- [ ] Enable MongoDB IP whitelist
- [ ] Use strong JWT secret (32+ characters)
- [ ] Add rate limiting to auth endpoints
- [ ] Add request logging and monitoring
- [ ] Set up error tracking (Sentry, etc.)

### Environment Variables (Production)

**Backend (.env)**
```
MONGO_URL=mongodb+srv://prod_user:strong_password@prod-cluster.mongodb.net/blog
SECRET=your-very-long-random-secret-key-32-characters-minimum
```

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
```

### Nginx Configuration (Production)

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Redirect HTTP to HTTPS
    if ($scheme != "https") {
        return 301 https://$server_name$request_uri;
    }
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
    }
}
```

## Common Vulnerabilities & Mitigations

### XSS (Cross-Site Scripting)
- **Risk**: Malicious JavaScript in post content
- **Mitigation**: HTML sanitization with bleach
- **Status**: ✅ Protected

### CSRF (Cross-Site Request Forgery)
- **Risk**: Unauthorized actions from other sites
- **Mitigation**: httpOnly cookies + SameSite=Lax
- **Status**: ✅ Protected

### SQL Injection
- **Risk**: Malicious database queries
- **Mitigation**: Using MongoDB (not SQL) + Pydantic validation
- **Status**: ✅ Protected

### Credential Exposure
- **Risk**: Secrets in frontend code
- **Mitigation**: Only NEXT_PUBLIC_ variables exposed, secrets in backend .env
- **Status**: ✅ Protected

### Man-in-the-Middle
- **Risk**: Intercepting unencrypted traffic
- **Mitigation**: HTTPS/SSL in production
- **Status**: ⚠️ Needs HTTPS in production

### Brute Force
- **Risk**: Repeated login attempts
- **Mitigation**: Rate limiting (not yet implemented)
- **Status**: ⚠️ Should add rate limiting

## Secrets Management

### Development
- Store in `.env` files (not in git)
- Use `.gitignore` to prevent commits

### Production
- Use environment variables from hosting platform
- Use secrets management service (AWS Secrets Manager, etc.)
- Rotate secrets regularly
- Never commit secrets to git

## Monitoring & Logging

### What to Log
- Authentication attempts (success/failure)
- Post creation/deletion
- API errors
- Database errors

### What NOT to Log
- Passwords
- Tokens
- Personal information
- Sensitive data

## Regular Security Tasks

- [ ] Update dependencies monthly
- [ ] Review access logs weekly
- [ ] Rotate secrets quarterly
- [ ] Run security audits annually
- [ ] Monitor for suspicious activity
- [ ] Keep MongoDB updated
- [ ] Keep FastAPI updated
- [ ] Keep Next.js updated

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Next.js Security](https://nextjs.org/docs/advanced-features/security-headers)
- [MongoDB Security](https://docs.mongodb.com/manual/security/)

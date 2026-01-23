# El Akeil Backend API Specifications

## 🔐 Authentication Endpoints

### 1. Chef Registration
**Endpoint:** `POST /api/auth/chef-register`

**Request Body:**
```json
{
  "fullName": "string",
  "email": "string (valid email)",
  "password": "string (min 8 chars)",
  "kitchenName": "string",
  "kitchenAddress": "string",
  "nationalId": "string (14 digits)",
  "role": "chef"
}
```

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Chef registered successfully",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "email": "email@example.com",
    "fullName": "Full Name",
    "role": "chef",
    "kitchenName": "Kitchen Name",
    "kitchenAddress": "Address",
    "nationalId": "14_digit_number",
    "verified": false,
    "createdAt": "2026-01-18T00:00:00Z"
  }
}
```

**Response (Error - 400/409):**
```json
{
  "success": false,
  "message": "Email already registered" | "Validation failed"
}
```

---

### 2. Chef Login
**Endpoint:** `POST /api/auth/chef-login`

**Request Body:**
```json
{
  "email": "string",
  "password": "string",
  "role": "chef"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "email": "email@example.com",
    "fullName": "Full Name",
    "role": "chef",
    "kitchenName": "Kitchen Name",
    "verified": true
  }
}
```

**Response (Error - 401):**
```json
{
  "success": false,
  "message": "Invalid email or password"
}
```

---

### 3. Driver Registration
**Endpoint:** `POST /api/auth/driver-register`

**Request Body:**
```json
{
  "fullName": "string",
  "email": "string (valid email)",
  "password": "string (min 8 chars)",
  "vehicleType": "motorcycle | scooter | car",
  "licenseNumber": "string",
  "nationalId": "string (14 digits)",
  "phoneNumber": "string (10-11 digits)",
  "role": "driver"
}
```

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Driver registered successfully",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "email": "email@example.com",
    "fullName": "Full Name",
    "role": "driver",
    "vehicleType": "motorcycle",
    "licenseNumber": "DL12345678",
    "nationalId": "14_digit_number",
    "phoneNumber": "20123456789",
    "verified": false,
    "createdAt": "2026-01-18T00:00:00Z"
  }
}
```

**Response (Error - 400/409):**
```json
{
  "success": false,
  "message": "Email already registered" | "Validation failed"
}
```

---

### 4. Driver Login
**Endpoint:** `POST /api/auth/driver-login`

**Request Body:**
```json
{
  "email": "string",
  "password": "string",
  "role": "driver"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "email": "email@example.com",
    "fullName": "Full Name",
    "role": "driver",
    "vehicleType": "motorcycle",
    "verified": true
  }
}
```

**Response (Error - 401):**
```json
{
  "success": false,
  "message": "Invalid email or password"
}
```

---

## 🍽️ Food Endpoints (For Future Integration)

### Get Foods by Level
**Endpoint:** `GET /api/foods?level=fast`

**Query Parameters:**
- `level` - fast | home | special | diet

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "food_id",
      "name": "Dish Name",
      "category": "meat",
      "level": "fast",
      "chef": "Chef Name",
      "chefId": "chef_id",
      "price": 50,
      "rating": 4.5,
      "reviews": 120,
      "image": "url_to_image",
      "emoji": "🍔",
      "ingredients": ["ingredient1", "ingredient2"],
      "description": "Description"
    }
  ]
}
```

### Get Foods by Category
**Endpoint:** `GET /api/foods?category=meat`

**Query Parameters:**
- `category` - meat | chicken | seafood | sweets | drinks

### Get Occasion Foods
**Endpoint:** `GET /api/foods?occasion=ramadan`

**Query Parameters:**
- `occasion` - ramadan | eid | events | gatherings

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  role ENUM('customer', 'chef', 'driver', 'admin') NOT NULL,
  phone_number VARCHAR(20),
  national_id VARCHAR(14) UNIQUE,
  verified BOOLEAN DEFAULT FALSE,
  verified_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP
);
```

### Chef Profile Table
```sql
CREATE TABLE chef_profiles (
  id UUID PRIMARY KEY,
  user_id UUID UNIQUE NOT NULL REFERENCES users(id),
  kitchen_name VARCHAR(255) NOT NULL,
  kitchen_address TEXT NOT NULL,
  rating DECIMAL(3,2) DEFAULT 0,
  total_orders INT DEFAULT 0,
  verification_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
  document_url VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Driver Profile Table
```sql
CREATE TABLE driver_profiles (
  id UUID PRIMARY KEY,
  user_id UUID UNIQUE NOT NULL REFERENCES users(id),
  vehicle_type VARCHAR(50) NOT NULL,
  license_number VARCHAR(50) UNIQUE NOT NULL,
  vehicle_registration VARCHAR(50),
  rating DECIMAL(3,2) DEFAULT 0,
  total_deliveries INT DEFAULT 0,
  verification_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
  document_url VARCHAR(255),
  is_available BOOLEAN DEFAULT FALSE,
  current_location POINT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Foods Table
```sql
CREATE TABLE foods (
  id UUID PRIMARY KEY,
  chef_id UUID NOT NULL REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(50) NOT NULL,
  level VARCHAR(50) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  image_url VARCHAR(255),
  emoji VARCHAR(10),
  rating DECIMAL(3,2) DEFAULT 0,
  reviews INT DEFAULT 0,
  is_occasion_food BOOLEAN DEFAULT FALSE,
  occasion_type VARCHAR(50),
  ingredients TEXT,
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔄 Frontend-Backend Integration

### Authorization Header
All protected endpoints should include:
```
Authorization: Bearer {jwt_token}
```

### JWT Payload Example
```json
{
  "sub": "user_id",
  "email": "email@example.com",
  "role": "chef",
  "iat": 1234567890,
  "exp": 1234571490
}
```

---

## ✅ Implementation Checklist

### Chef Authentication
- [ ] Implement chef registration endpoint
- [ ] Hash passwords with bcrypt
- [ ] Generate JWT tokens
- [ ] Store chef profile data
- [ ] Implement chef login endpoint
- [ ] Add email verification (optional)
- [ ] Add password reset flow

### Driver Authentication
- [ ] Implement driver registration endpoint
- [ ] Store driver profile data
- [ ] Implement driver login endpoint
- [ ] Add document verification flow
- [ ] Add vehicle verification flow

### Food Management
- [ ] Create foods table
- [ ] Implement food listing by level
- [ ] Implement food listing by category
- [ ] Implement food listing by occasion
- [ ] Add filtering/search functionality
- [ ] Add pagination

### Role-Based Access Control
- [ ] Enforce role isolation in middleware
- [ ] Block cross-role access
- [ ] Add role-specific routes
- [ ] Implement chef dashboard access
- [ ] Implement driver dashboard access

---

## 🔒 Security Considerations

1. **Password Hashing**
   - Use bcrypt with salt rounds ≥ 10
   - Never store plain passwords

2. **JWT Security**
   - Use strong secret key (min 32 chars)
   - Set expiration (15 mins for access, 7 days for refresh)
   - Validate signature on every request

3. **Rate Limiting**
   - Limit login attempts (5 per minute)
   - Limit registration (1 per hour per IP)
   - Implement CAPTCHA for repeated failures

4. **Data Validation**
   - Validate all inputs server-side
   - Sanitize to prevent SQL injection
   - Check role authorization for every action

5. **CORS Configuration**
   - Allow only trusted origins
   - Don't allow credentials with wildcard origins
   - Specify allowed methods and headers

6. **HTTPS**
   - Force HTTPS in production
   - Use HSTS headers
   - Valid SSL certificate required

---

## 📱 Error Handling

### Common Error Responses

**400 Bad Request**
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "email": "Invalid email format",
    "password": "Password too short"
  }
}
```

**401 Unauthorized**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

**403 Forbidden**
```json
{
  "success": false,
  "message": "Access denied - insufficient permissions"
}
```

**409 Conflict**
```json
{
  "success": false,
  "message": "Email already registered"
}
```

**500 Server Error**
```json
{
  "success": false,
  "message": "Internal server error"
}
```

---

## 🚀 Testing

### Unit Tests
- Test validation functions
- Test password hashing
- Test JWT generation

### Integration Tests
- Test registration flow
- Test login flow
- Test role isolation
- Test data persistence

### E2E Tests
- Test full registration journey
- Test full login journey
- Test role-based redirects
- Test session management

---

## 📋 Migration Path from Current System

If migrating from existing auth:

1. **Keep existing customer auth** - Don't modify
2. **Add new chef endpoints** - Separate from customer
3. **Add new driver endpoints** - Separate from customer
4. **Update middleware** - Check role per route
5. **Test extensively** - Ensure no conflicts
6. **Gradual rollout** - Deploy new pages first, then update old ones

---

## 🔗 Related Files

- Frontend: `/src/Frontend/index.html`
- Chef Register: `/src/Frontend/chef_register.html`
- Chef Login: `/src/Frontend/chef_login.html`
- Driver Register: `/src/Frontend/driver_register.html`
- Driver Login: `/src/Frontend/driver_login.html`
- Styles: `/src/Frontend/assets/css/styles.css`
- Scripts: `/src/Frontend/assets/js/main.js`

---

## 📞 Questions & Support

For API integration issues, refer to the IMPLEMENTATION_GUIDE.md for frontend structure and expected data formats.

All endpoints are documented with request/response examples above.

Ready for development! 🚀

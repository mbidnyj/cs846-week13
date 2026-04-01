# High-Level Implementation Steps: Microblogging Web Application

## Implementation Strategy & Task Breakdown

To efficiently implement the microblogging web application, follow this modular, incremental approach:

### 1. Incremental, Modular Development
- Tackle one major module at a time (e.g., authentication, then posting).
- Complete and test each module before moving to the next.

### 2. Test-Driven Approach
- For each endpoint, write tests as you implement.
- Use both unit and integration tests where possible.

### 3. Iterative Delivery
- After each module, verify with tests and basic manual checks.
- Refactor and improve based on feedback and test results.

### 4. Security First
- Implement password hashing and session validation from the start.
- Never store or return plain-text passwords.

### 5. Suggested Task Phases

#### Phase 1: User & Session Management
- Define data models (User, Session)
- Implement in-memory storage
- Build and test `/register`, `/login`, session management
- Add `/profile/update` and `/profile` endpoints
- Ensure password hashing and error handling

#### Phase 2: Posting System
- Define Post (and Reply) models
- Implement `/post`, `/post/edit`, `/post/delete` endpoints
- Add validation and error handling

#### Phase 3: Additional Features & Hardening
- Add likes, replies, and other future features
- Refactor for persistence (database)
- Add more tests, documentation, and security reviews

Each phase can be further split into actionable todos for implementation and tracking progress.

## 1. User Authentication & Profile Management

### Data Models
- **User**
	- username: string (unique)
	- email: string (unique)
	- password: string (hashed)
	- bio: string (optional)
- **Session**
	- session_id: string (unique, random)
	- user_email: string (reference to User)

### API Endpoints & Specifications

#### 1.1 Registration Endpoint
- **POST** `/register`
	- Request: { username, email, password, bio? }
	- Response: { success: bool, message: string }
	- Validations: required fields, unique username/email, password strength

#### 1.2 Login Endpoint
- **POST** `/login`
	- Request: { email, password }
	- Response: { success: bool, session_token?: string, message: string }
	- Validations: correct credentials

#### 1.3 Session Management
- In-memory dict: { session_id: user_email }
- Generate session token on login, return to client (e.g., as cookie or header)
- Require session token for protected endpoints

#### 1.4 Profile Update Endpoint
- **POST** `/profile/update`
	- Request: { session_token, username?, bio?, password? }
	- Response: { success: bool, updated_profile?: object, message: string }
	- Validations: session token, unique username if changed

#### 1.5 Profile Fetch Endpoint
- **GET** `/profile`
	- Request: { session_token }
	- Response: { username, email, bio }
	- Validations: session token

### Security & Error Handling
- Hash passwords before storing
- Never return password in responses
- Handle missing/invalid session tokens
- Return clear error messages for all validation failures

### Implementation Checklist

- [ ] Define User and Session data models
- [ ] Implement in-memory storage for users and sessions
- [ ] Implement `/register` endpoint with validation and error handling
- [ ] Implement `/login` endpoint with session creation
- [ ] Implement session token generation and validation
- [ ] Implement `/profile/update` endpoint with field validation
- [ ] Implement `/profile` endpoint (exclude password)
- [ ] Hash passwords on registration and update
- [ ] Add error handling for all endpoints


## 2. Posting & Managing Updates

### Data Models
- **Post**
	- id: string (unique, UUID or incremental)
	- author: string (username or user reference)
	- content: string
	- timestamp: datetime
	- edited: boolean (default: false)
	- edited_timestamp: datetime (optional)
	- likes: set of user IDs (for future use)
	- replies: list of Reply objects

- **Reply** (for future use)
	- id: string (unique)
	- author: string (username)
	- content: string
	- timestamp: datetime

### API Endpoints & Specifications

#### 2.1 Add New Post
- **POST** `/post`
	- Request: { session_token, content }
	- Response: { success: bool, post?: object, message: string }
	- Validations: session token, non-empty content

#### 2.2 Edit Post
- **POST** `/post/edit`
	- Request: { session_token, id, content }
	- Response: { success: bool, post?: object, message: string }
	- Validations: session token, post exists, user is author, non-empty content

#### 2.3 Delete Post
- **POST** `/post/delete`
	- Request: { session_token, id }
	- Response: { success: bool, message: string }
	- Validations: session token, post exists, user is author

#### 2.4 Fetch User Posts
- **GET** `/posts/user/<username>`
	- Response: { posts: [ { id, content, timestamp, edited, edited_timestamp } ] }
	- Validations: user exists

### Security & Error Handling
- Require valid session token for all post actions
- Only allow authors to edit/delete their own posts
- Validate input (e.g., content length, non-empty)
- Return clear error messages for all validation failures

### Implementation Checklist

- [ ] Define Post and Reply data models
- [ ] Implement in-memory storage for posts (list or dict)
- [ ] Implement `/post` endpoint with validation and error handling
- [ ] Implement `/post/edit` endpoint (author-only, update content and edited flag/timestamp)
- [ ] Implement `/post/delete` endpoint (author-only, remove post)
- [ ] Implement `/posts/user/<username>` endpoint (fetch and order posts)
- [ ] Add error handling for all endpoints

## 3. Feed Generation & Pagination

### Data Models
- **Feed** (no separate model; uses Post objects)
	- Posts are aggregated from the existing Post data model.

### API Endpoints & Specifications

#### 3.1 Global Feed Endpoint
- **GET** `/feed`
	- Request: { session_token?, offset?, limit? }
	- Response: { posts: [ { id, author, content, timestamp, edited, edited_timestamp } ], total_count: int, offset: int, limit: int }
	- Validations: session token (optional, based on privacy), offset/limit are integers, offset ≥ 0, limit > 0

#### 3.2 Pagination
- Support query parameters: `offset` (start index, default 0), `limit` (number of posts, default 20)
- Apply pagination to sorted posts (newest first)
- Return total post count and current page info

### Security & Error Handling
- Validate offset and limit parameters
- Return clear error messages for invalid parameters
- Optionally require session token for private feeds

### Implementation Checklist

- [ ] Implement `/feed` endpoint to fetch all posts, sorted by timestamp descending
- [ ] Parse and validate `offset` and `limit` query parameters
- [ ] Apply pagination to the post list
- [ ] Return total post count and current page info in response
- [ ] Add error handling for invalid parameters
### 3.2 Pagination
### Security & Error Handling
- Validate offset and limit parameters
- Return clear error messages for invalid parameters
- Optionally require session token for private feeds

### Implementation Checklist

- [ ] Implement `/feed` endpoint to fetch all posts, sorted by timestamp descending
- [ ] Parse and validate `offset` and `limit` query parameters
- [ ] Apply pagination to the post list
- [ ] Return total post count and current page info in response
- [ ] Add error handling for invalid parameters
## 4. Like & Reply Functionality

### Data Models
- **Like**
	- Not a separate model; each Post object has a `likes` set/list of user IDs
- **Reply**
	- id: string (unique)
	- author: string (username or user reference)
	- content: string
	- timestamp: datetime

### API Endpoints & Specifications

#### 4.1 Like Post Endpoint
- **POST** `/post/like`
	- Request: { session_token, id }
	- Response: { success: bool, like_count?: int, message: string }
	- Validations: session token, post exists, user is not author, user has not already liked

#### 4.2 Reply to Post Endpoint
- **POST** `/post/reply`
	- Request: { session_token, id, content }
	- Response: { success: bool, reply?: object, message: string }
	- Validations: session token, post exists, non-empty content

### Security & Error Handling
- Require valid session token for all like/reply actions
- Only allow authenticated users to like or reply
- Prevent duplicate likes from the same user
- Only allow replies to posts (no nested replies)
- Validate input (e.g., content length, non-empty)
- Return clear error messages for all validation failures

### Implementation Checklist

- [ ] Add `likes` set/list and `replies` list to Post data model (if not already present)
- [ ] Implement `/post/like` endpoint with validation and error handling
- [ ] Prevent duplicate likes from the same user
- [ ] Implement `/post/reply` endpoint with validation and error handling
- [ ] Only allow one-level replies (no nested replies)
- [ ] Add error handling for all endpoints


## 5. Profile Viewing

### Data Models
- **User** (reuse from Section 1)
	- username: string
	- bio: string
	- (exclude sensitive fields: password, email)
- **Post** (reuse from Section 2)
	- id, content, timestamp, edited, etc.

### API Endpoints & Specifications

#### 5.1 User Profile & Posts Endpoint
- **GET** `/user/<username>`
	- Request: URL parameter `username`
	- Response: 
		- { 
				username: string, 
				bio: string, 
				posts: [ { id, content, timestamp, edited, edited_timestamp } ] 
			}
	- Validations: user exists, exclude sensitive fields

### Security & Error Handling
- Exclude sensitive fields (password, email) from all responses
- Return clear error message if user not found
- Validate username parameter

### Implementation Checklist

- [ ] Implement `/user/<username>` endpoint
- [ ] Fetch user by username from in-memory storage
- [ ] Exclude sensitive fields from response
- [ ] Fetch and order user’s posts (newest first)
- [ ] Format response for frontend consumption (JSON)
- [ ] Add error handling for user not found and invalid input

## 6. Frontend Integration (API Only)
### 6.1 API Endpoint Documentation
	- Required request parameters (query, path, or body fields)
	- Expected request/response formats (JSON structure, field types)
	- Authentication/session requirements (e.g., session token needed)
	- Example requests and responses (sample JSON)

### API Documentation Requirements
- List all REST API endpoints with:
	- HTTP method (GET, POST, etc.)
	- URL path
	- Brief description of purpose
- For each endpoint, specify:
	- Required request parameters (query, path, or body fields)
	- Expected request/response formats (JSON structure, field types)
	- Authentication/session requirements (e.g., session token needed)
	- Example requests and responses (sample JSON)
- Organize documentation for easy reference by frontend developers
- Provide a summary table of endpoints for quick lookup

### Example API Documentation Structure

| Endpoint         | Method | Description                | Auth Required | Request Params         | Response Example         |
|------------------|--------|----------------------------|---------------|-----------------------|--------------------------|
| /register        | POST   | Register new user          | No            | username, email, ...  | { success, message }     |
| /login           | POST   | User login                 | No            | email, password       | { success, token }       |
| /post            | POST   | Create new post            | Yes           | session_token, content| { success, post }        |
| ...              | ...    | ...                        | ...           | ...                   | ...                      |

#### Example Endpoint Detail

**POST** `/register`
- Request: `{ "username": "string", "email": "string", "password": "string", "bio": "string?" }`
- Response: `{ "success": true, "message": "User registered" }`
- Notes: All fields required except bio. Username/email must be unique.

### Implementation Checklist
- [ ] List all endpoints with method, path, and description
- [ ] For each endpoint, specify required parameters and formats
- [ ] Add authentication/session requirements per endpoint
- [ ] Provide example requests and responses
- [ ] Create a summary table of endpoints
- [ ] Organize documentation for easy reference


Each step above can be expanded into detailed implementation instructions as needed.

---

## Technology Stack & Development Setup

- **Backend Language:** Python
- **Environment:** Use the existing Conda environment named `cs846` (Python is already installed)
- **Third-Party Libraries:**
	- Use only essential libraries to minimize dependencies. Recommended:
		- `Flask` (for REST API server)
		- `Werkzeug` (for password hashing, if not using Flask's built-in)
		- `uuid` (standard library, for unique IDs)
		- `datetime` (standard library, for timestamps)
		- `json` (standard library, for serialization)
		- Avoid additional libraries unless strictly necessary for core functionality.
- **Development Setup:**
	- Activate the environment before development:
		- `conda activate cs846`
	- Install Flask (if not already installed):
		- `conda install flask` or `pip install flask`
	- All code should be compatible with the Python version in `cs846`.
# Project Architecture

## Backend

### Goals
- Authenticate users
- Store and retrieve user food logs and macro goals
- Store user consent for AI agent access
- Expose API endpoints for frontend and agents
- Interact with Supabase (hosted database)

### Tools and Frameworks

#### 1. FastAPI (Python Web Framework)
- Define routes for HTTP requests
- Parse and validate JSON payloads using Pydantic
- Return JSON responses
- Enforce authentication using dependencies (e.g., JWT token validation)
- Auto-generate interactive API docs (Swagger/OpenAPI)

#### 2. Supabase (Hosted PostgreSQL)
- Store all persistent data (user info, macro goals, food logs, agent permissions)
- Provide a GUI dashboard for table/data management
- Replace need to self-host Postgres
- Interact via supabase-py client in Python

#### 3. JWT (JSON Web Tokens)
- Handle authentication: issue token on login, validate on each request
- Token encodes user_id, is signed, and may include expiration
- Token sent in Authorization header for secure requests

#### 4. Pydantic
- Define expected structure of input data
- Enforce types and validate inputs automatically
- Prevent bad data from reaching the database

### Backend Data Flow

#### Step 1: User Signs Up or Logs In
- Frontend sends POST /signup or /login with email/password
- FastAPI validates input (Pydantic)
- If valid: user is stored in Supabase or password is checked
- If successful: JWT token is returned (includes user_id)

#### Step 2: User Enters Macro Goals
- Frontend sends POST /macros (calorie goal, macro %, restrictions)
- FastAPI validates input, extracts user_id from JWT, saves to macro_preferences

#### Step 3: User Logs Food
- Frontend sends POST /food-log (meal type, food, macros)
- FastAPI stores entry in food_logs, associated with user

#### Step 4: User Authorizes Agent Access
- Frontend sends POST /agent-consent
- FastAPI writes to agent_permissions (user_id, agent_id, has_consented, token)

#### Step 5: Agent Generates Meal Plan
- Agent backend sends GET /meal-plan?days=3 with agent token
- FastAPI checks agent permission, queries macro_preferences, returns data

### Database Structure (Supabase)

#### users
| column        | type      |
|--------------|-----------|
| id (PK)      | UUID      |
| email        | text      |
| password_hash| text      |
| created_at   | timestamp |

#### macro_preferences
| column              | type      |
|---------------------|-----------|
| id (PK)             | UUID      |
| user_id (FK)        | UUID      |
| total_calories      | integer   |
| protein_pct         | float     |
| carb_pct            | float     |
| fat_pct             | float     |
| dietary_restrictions| text[]/JSON|
| created_at          | timestamp |

#### food_logs
| column      | type      |
|-------------|-----------|
| id (PK)     | UUID      |
| user_id (FK)| UUID      |
| meal_type   | text      |
| food_name   | text      |
| calories    | integer   |
| protein     | float     |
| carbs       | float     |
| fat         | float     |
| created_at  | timestamp |

#### agent_permissions
| column      | type      |
|-------------|-----------|
| id (PK)     | UUID      |
| user_id (FK)| UUID      |
| agent_id    | text      |
| has_consented| boolean  |
| access_token| text      |
| created_at  | timestamp |

---

## Frontend

### Goals
- Sign up and log in securely
- Submit macro goals
- Log meals
- View daily progress (graphs, summaries)
- Authorize AI agent access
- View generated meal plan

### Tools and Frameworks

#### 1. React.js
- Build reusable, interactive components
- Page-level components for login, dashboard, food logging, agent consent
- Dynamic UI updates

#### 2. Axios or Fetch API
- Send HTTP requests to FastAPI backend
- Authenticate user, submit preferences, log food, retrieve summaries, update agent consent, request meal plan

#### 3. JWT Token Storage
- Store JWT token in localStorage after login
- Attach token to all secure requests

#### 4. React Router
- Manage client-side navigation
- Define routes for login, dashboard, macros, food-log, agent consent, meal plan
- Enable programmatic redirects

#### 5. Recharts or Chart.js
- Visualize macro intake vs. goals
- Render bar/pie/line charts based on backend data

### Component and Route Structure
- /login - LoginPage.js
- /dashboard - Dashboard.js
- /macros - MacroForm.js
- /food-log - FoodLogForm.js
- /agent - AgentConsent.js
- /meal-plan (future) - MealPlan.js
- Shared: Navbar.js, Graph.js

### Frontend Workflow
1. User Login/Register: POST /login or /signup, store token, redirect to /dashboard
2. Macro Goal Submission: POST /macros, redirect to dashboard
3. Logging Food: POST /food-log, dashboard refreshes
4. Displaying Dashboard Data: GET /macros and /food-log?date=today, render summary/graph
5. Agent Consent: POST /agent-consent, show success
6. Viewing Meal Plan: GET /meal-plan?days=3, display suggestions

### JWT Handling in Frontend
- All secure routes attach the token in the Authorization header
- Use a wrapper function to attach token to all requests 
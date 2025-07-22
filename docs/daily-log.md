# Daily Log

## Day 1 – July 19, 2025
**Project:** MyFitnessPal Clone & AI Meal Planner Agent

**Progress:**
Today, I focused on planning and defining the backend architecture for the fitness tracking application. This involved the following:

### Understanding Core Architecture:
- Structured the backend, including user authentication flow, data storage, and API design for frontend/AI agent interaction.

### Choosing Frameworks & Tools:
- FastAPI for backend (automatic validation, docs, performance)
- Supabase for hosted PostgreSQL (user accounts, macro goals, food logs, agent permissions)
- Pydantic for request validation
- JWT for authentication
- dotenv for managing credentials
- supabase-py for Python integration

### Data Modeling & Planning:
- Defined main entities: users, macro_preferences, food_logs, agent_permissions
- Planned FastAPI request validation with Pydantic
- Outlined JWT-based user data security and agent permission handling

### Documentation:
- Drafted architecture plan covering:
  - Framework/tool roles
  - Backend integration
  - API structure/security
  - Data flow (frontend → backend → Supabase)

### Next Steps:
- Build backend project directory
- Create main.py and initial auth.py for signup/login and JWT
- Set up Supabase instance and tables
- Implement API routes for macro preferences and food logs

---

## Day 2 – July 20, 2025
**Project:** MyFitnessPal Clone & AI Meal Planner Agent

**Progress:**
Shifted focus to frontend architecture. Broke down tools/frameworks for UI, clarified backend interaction, and mapped component/page structure.

### Frontend Planning & Documentation:
- Outlined frontend tool usage:
  - React.js for modular UI and routing
  - Axios for HTTP requests (with tokens)
  - JWT Token Storage via localStorage
  - React Router for navigation
  - Charting libraries for macro visualization
- Documented frontend-backend communication, real-time data rendering, agent consent UI, and component/route structure.
- Defined user flow from login to data visualization and agent integration.

### Next Steps:
- Finalize frontend architecture doc
- Start modular development: login/signup flow
- Implement FastAPI endpoints and connect to React login page

---

## Day 3 – July 21, 2025
**Project:** MyFitnessPal Clone & AI Meal Planner Agent

**Progress:**
Completed full architecture doc (backend & frontend). Outlined tools, interactions, and workflows. Began backend build: FastAPI setup, root/health endpoints, dummy auth endpoints, and Pydantic models for validation. Created GitHub repo and resolved venv/commit issues.

### Next Steps:
- Integrate Supabase for persistent user data
- Revisit architecture doc for schema clarity
- Continue modular, incremental development

---

## Day 4 – July 22, 2025
**Project:** MyFitnessPal Clone & AI Meal Planner Agent

**Progress:**
- Set up Supabase project
- Created user_profiles table (user_id, display_name, created_at, updated_at)
- Established 1:1 relationship with auth.users.id
- Fixed schema (removed invalid auth.users() default)
- Configured FastAPI backend to connect to Supabase
- Tested backend connection and /test-table endpoint

### Next Steps:
- Add FastAPI endpoint to insert user_profiles row
- Test with dummy data
- Start Supabase Auth integration
- Research endpoint access restriction via auth tokens
- Plan/create schemas for macro_goals, food_logs, agent_permissions
- (Optional) Connect React frontend to /test-table endpoint 
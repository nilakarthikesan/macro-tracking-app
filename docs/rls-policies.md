# Row Level Security (RLS) Policies Implementation Guide

## Overview
This guide walks through implementing Row Level Security (RLS) policies for the Macro Tracking App to ensure users can only access and modify their own data.

## Tables Requiring RLS Policies

### 1. `user_profiles` Table
- **Purpose**: Store user profile information
- **Key Field**: `user_id` (references `auth.users.id`)

### 2. `macro_goals` Table  
- **Purpose**: Store user's macro goals
- **Key Field**: `user_id` (references `auth.users.id`)

### 3. `food_logs` Table
- **Purpose**: Store user's food log entries
- **Key Field**: `user_id` (references `auth.users.id`)

## Step-by-Step Implementation

### Step 1: Enable RLS on Tables

For each table (`user_profiles`, `macro_goals`, `food_logs`):

1. Go to Supabase Dashboard → Database → Tables
2. Click on the table name
3. Go to the "RLS" tab
4. **Enable RLS** by toggling the switch to ON
5. Click "Save"

### Step 2: Create RLS Policies

#### Policy 1: SELECT Policy (Read Access)
**Purpose**: Users can only read their own data

**SQL for each table:**
```sql
-- For user_profiles table
CREATE POLICY "Users can view own profile" ON user_profiles
FOR SELECT USING (auth.uid() = user_id);

-- For macro_goals table  
CREATE POLICY "Users can view own macro goals" ON macro_goals
FOR SELECT USING (auth.uid() = user_id);

-- For food_logs table
CREATE POLICY "Users can view own food logs" ON food_logs
FOR SELECT USING (auth.uid() = user_id);
```

#### Policy 2: INSERT Policy (Create Access)
**Purpose**: Users can only create records for themselves

**SQL for each table:**
```sql
-- For user_profiles table
CREATE POLICY "Users can create own profile" ON user_profiles
FOR INSERT WITH CHECK (auth.uid() = user_id);

-- For macro_goals table
CREATE POLICY "Users can create own macro goals" ON macro_goals
FOR INSERT WITH CHECK (auth.uid() = user_id);

-- For food_logs table
CREATE POLICY "Users can create own food logs" ON food_logs
FOR INSERT WITH CHECK (auth.uid() = user_id);
```

#### Policy 3: UPDATE Policy (Modify Access)
**Purpose**: Users can only update their own data

**SQL for each table:**
```sql
-- For user_profiles table
CREATE POLICY "Users can update own profile" ON user_profiles
FOR UPDATE USING (auth.uid() = user_id);

-- For macro_goals table
CREATE POLICY "Users can update own macro goals" ON macro_goals
FOR UPDATE USING (auth.uid() = user_id);

-- For food_logs table
CREATE POLICY "Users can update own food logs" ON food_logs
FOR UPDATE USING (auth.uid() = user_id);
```

#### Policy 4: DELETE Policy (Remove Access)
**Purpose**: Users can only delete their own data

**SQL for each table:**
```sql
-- For user_profiles table
CREATE POLICY "Users can delete own profile" ON user_profiles
FOR DELETE USING (auth.uid() = user_id);

-- For macro_goals table
CREATE POLICY "Users can delete own macro goals" ON macro_goals
FOR DELETE USING (auth.uid() = user_id);

-- For food_logs table
CREATE POLICY "Users can delete own food logs" ON food_logs
FOR DELETE USING (auth.uid() = user_id);
```

## How to Apply These Policies

### Option 1: Using Supabase Dashboard (Recommended)
1. Go to Supabase Dashboard → Database → Tables
2. Click on a table (e.g., `user_profiles`)
3. Go to "Policies" tab
4. Click "New Policy"
5. Choose "Create a policy from scratch"
6. Fill in the details:
   - **Policy Name**: "Users can view own profile"
   - **Allowed operation**: SELECT
   - **Target roles**: authenticated
   - **Using expression**: `auth.uid() = user_id`
7. Click "Review" then "Save policy"
8. Repeat for INSERT, UPDATE, DELETE operations
9. Repeat for all tables

### Option 2: Using SQL Editor
1. Go to Supabase Dashboard → SQL Editor
2. Copy and paste the SQL commands above
3. Execute each command for each table

## Testing RLS Policies

### Test 1: Authenticated User Access
1. Login with a user account
2. Try to access your own data via API endpoints
3. Verify you can read/write your own data

### Test 2: Cross-User Access Prevention
1. Login with User A
2. Try to access User B's data (should fail)
3. Verify you get 403 Forbidden or empty results

### Test 3: Unauthenticated Access Prevention
1. Try to access endpoints without authentication
2. Verify you get 401 Unauthorized

## Common Issues and Solutions

### Issue 1: "new row violates row-level security policy"
**Cause**: RLS is enabled but no INSERT policy exists
**Solution**: Create INSERT policy for the table

### Issue 2: "permission denied for table"
**Cause**: RLS is enabled but no SELECT policy exists  
**Solution**: Create SELECT policy for the table

### Issue 3: User can't access their own data
**Cause**: Policy condition might be incorrect
**Solution**: Check that `auth.uid()` matches the `user_id` field type

## Verification Checklist

- [ ] RLS enabled on all tables
- [ ] SELECT policies created for all tables
- [ ] INSERT policies created for all tables  
- [ ] UPDATE policies created for all tables
- [ ] DELETE policies created for all tables
- [ ] Authenticated users can access their own data
- [ ] Users cannot access other users' data
- [ ] Unauthenticated requests are blocked
- [ ] All API endpoints work correctly with RLS

## Security Benefits

With RLS enabled:
- Users can only access their own data
- No risk of data leakage between users
- Database-level security (not just application-level)
- Automatic enforcement for all database operations
- Protection against SQL injection attacks 
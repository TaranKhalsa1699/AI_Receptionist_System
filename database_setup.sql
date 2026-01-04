-- ============================================================================
-- SUPABASE & POSTGRES SETUP GUIDE (ZERO TO PRODUCTION)
-- ============================================================================

-- 1. WHAT IS SUPABASE?
-- Supabase is a wrapper around PostgreSQL. It provides a Realtime API, Auth, 
-- and Dashboard, but under the hood, it is just a standard Postgres database.
-- Anything you can do in Postgres (SQL, Triggers, Views), you can do here.

-- 2. SCHEMA & TABLES
-- We create a table in the 'public' schema. 'public' is the default namespace.
-- We use UUIDs for primary keys because they are secure and unique across systems.

create table if not exists public.patients (
    id uuid default gen_random_uuid() primary key, -- Auto-generates unique ID
    name text not null,                            -- Mandatory Name
    age integer not null,                          -- Mandatory Age
    query text not null,                           -- Mandatory Query
    ward text not null,                            -- Mandatory Ward
    created_at timestamp with time zone default now() -- Auto-timestamp
);

-- 3. ROW LEVEL SECURITY (RLS)
-- RLS is a security feature of Postgres. It acts like a firewall for your table.
-- By default, Supabase enables RLS on new tables created via the UI.
-- If RLS is ON and no Policy exists, NO ONE (except the Service Role) can do ANYTHING.
-- This is why you got the "new row violates row-level security policy" error.

alter table public.patients enable row level security;

-- 4. POLICIES (THE FIX)
-- We need to explicitly allow the 'anon' role (which your backend uses if you provided the PUBLIC KEY)
-- to INSERT rows.
-- 'anon' = Unauthenticated users / Public API requests.

create policy "Backend Insert Policy" 
on public.patients 
for insert 
to anon 
with check (true); 
-- 'with check (true)' means "Allow insert of ANY row". 
-- Since your backend validates data before sending, this is safe for a backend-to-db connection.

-- 5. VERIFICATION QUERIES
-- Run these to confirm everything is working.

-- Check if RLS is enabled (Should say 'true')
select tablename, rowsecurity 
from pg_tables 
where tablename = 'patients';

-- Check active policies (Should see 'Backend Insert Policy')
select * from pg_policies 
where tablename = 'patients';

-- Test Insert (Simulating what your backend does)
insert into public.patients (name, age, query, ward)
values ('Test User', 30, 'Testing Database', 'general');

-- Verify Insert
select * from public.patients order by created_at desc limit 1;

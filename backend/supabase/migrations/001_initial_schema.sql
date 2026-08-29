-- Enable the pgcrypto extension for UUID generation if not already enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. USERS TABLE
-- Maps to Supabase's built-in auth.users, holding our custom application roles
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('parent', 'asha', 'admin')),
    phone TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    preferred_lang TEXT DEFAULT 'hi' CHECK (preferred_lang IN ('hi', 'en', 'mr')),
    area TEXT, -- Assigned area for ASHA workers
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. FAMILIES TABLE
CREATE TABLE families (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    primary_phone TEXT NOT NULL UNIQUE,
    consent_given_at TIMESTAMPTZ,
    consent_version TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. CHILDREN TABLE
CREATE TABLE children (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_id UUID NOT NULL REFERENCES families(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    dob DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. VACCINE SCHEDULE REFERENCE TABLE
CREATE TABLE vaccine_schedule_reference (
    vaccine_code TEXT PRIMARY KEY,
    name_hi TEXT NOT NULL,
    name_en TEXT NOT NULL,
    name_mr TEXT NOT NULL,
    description_hi TEXT,
    description_en TEXT,
    description_mr TEXT,
    due_at_weeks INTEGER NOT NULL,
    schedule_version TEXT NOT NULL,
    last_reviewed_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_by TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. DOSE RECORDS TABLE
CREATE TABLE dose_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_id UUID NOT NULL REFERENCES children(id) ON DELETE CASCADE,
    vaccine_code TEXT NOT NULL REFERENCES vaccine_schedule_reference(vaccine_code),
    status TEXT NOT NULL CHECK (status IN ('due', 'done', 'missed')) DEFAULT 'due',
    administered_date DATE,
    administered_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. CONSENT LOG TABLE
CREATE TABLE consent_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    family_id UUID NOT NULL REFERENCES families(id) ON DELETE CASCADE,
    action TEXT NOT NULL CHECK (action IN ('given', 'withdrawn', 'updated')),
    consent_text_version TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-------------------------------------------------------------------------------
-- ROW LEVEL SECURITY (RLS)
-------------------------------------------------------------------------------
-- Turn on RLS for all sensitive tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE families ENABLE ROW LEVEL SECURITY;
ALTER TABLE children ENABLE ROW LEVEL SECURITY;
ALTER TABLE dose_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE consent_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE vaccine_schedule_reference ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read their own user profile
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

-- Policy: Admins can do everything on vaccine schedules, others can only read
CREATE POLICY "Anyone can read vaccine schedules" ON vaccine_schedule_reference
    FOR SELECT USING (true);

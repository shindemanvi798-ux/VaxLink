from supabase import create_client, Client
from app.core.config import settings

# This client uses the standard anon key. 
# It is used for operations that will be authenticated via Row Level Security (RLS)
# using the token passed by the frontend.
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# This client uses the Service Role key.
# It bypasses Row Level Security completely. 
# USE WITH EXTREME CAUTION. Only use this for admin tasks like creating auth users 
# or system-level updates where RLS shouldn't apply.
supabase_admin: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

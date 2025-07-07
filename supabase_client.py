import logging
from typing import List
from models import User, UserInterest
from supabase import create_client, Client

class SupabaseClient:
    """Client for interacting with Supabase database"""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.client: Client = create_client(supabase_url, supabase_key)
        logging.info("SupabaseClient initialized")
    
    def get_all_users(self) -> List[User]:
        """Fetch all users with their interests from Supabase"""
        try:
            logging.info("Fetching all users from Supabase")
            
            # First, fetch all users from the users table
            users_response = self.client.table("users").select("id, email").execute()
            
            if not users_response.data:
                logging.warning("No users found in database")
                return []
            
            users = []
            for user_data in users_response.data:
                user_id = user_data["id"]
                user_email = user_data["email"]
                
                logging.info(f"Fetching interests for user {user_email} (ID: {user_id})")
                
                # Fetch interests for this user from user_interests table
                interests_response = self.client.table("user_interests").select(
                    "interest, subinterests"
                ).eq("user_id", user_id).execute()
                
                # Parse user interests
                user_interests = []
                for interest_data in interests_response.data:
                    user_interest = UserInterest(
                        interest=interest_data["interest"],
                        subinterests=interest_data["subinterests"]
                    )
                    user_interests.append(user_interest)
                
                # Create user object
                user = User(
                    id=user_id,
                    email=user_email,
                    user_interests=user_interests
                )
                users.append(user)
            
            logging.info(f"Successfully fetched {len(users)} users from Supabase")
            return users
            
        except Exception as e:
            logging.error(f"Error fetching users from Supabase: {e}")
            raise e


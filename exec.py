from dotenv import load_dotenv
import os
import logging
from supabase_client import SupabaseClient
from email_service import EmailService
from utils import setup_logging, load_environment_variables
from summary_agent import ExecutiveSummaryAgent

# Example usage
if __name__ == "__main__":
    # Setup logging
    setup_logging()
    env_vars = load_environment_variables()
    
    try:
        # Initialize services
        logging.info("Initializing services...")
        supabase_client = SupabaseClient(env_vars["SUPABASE_URL"], env_vars["SUPABASE_SERVICE_KEY"])
        agent = ExecutiveSummaryAgent(env_vars["OPENAI_API_KEY"], env_vars["EXA_API_KEY"])
        email_service = EmailService(env_vars["SENDER_EMAIL"], env_vars["SENDER_PASSWORD"])
        
        # Fetch all users from Supabase
        logging.info("Fetching all users from Supabase...")
        users = supabase_client.get_all_users()
        
        if not users:
            logging.warning("No users found in database. Exiting.")
            exit(0)
        
        logging.info(f"Processing {len(users)} users...")
        
        # Process each user
        for user in users:
            try:
                logging.info(f"Processing user: {user.email}")
                
                if not user.user_interests:
                    logging.warning(f"User {user.email} has no interests. Skipping.")
                    continue
                
                # Generate executive summary for all user interests combined
                all_summaries = []
                for user_interest in user.user_interests:
                    logging.info(f"Generating executive summary for interest: {user_interest.interest}")
                    summary = agent.create_executive_summary(user_interest)
                    all_summaries.append(summary)
                
                # Combine all summaries into one email
                combined_summary = "\n".join(all_summaries)
                
                # Send email
                logging.info(f"Sending executive summary via email to {user.email}...")
                email_sent = email_service.send_executive_summary(user, combined_summary)
                
                if email_sent:
                    logging.info(f"Executive summary sent successfully to {user.email}")
                else:
                    logging.error(f"Failed to send email to {user.email}")
                
            except Exception as e:
                logging.error(f"Error processing user {user.email}: {e}")
                continue  # Continue with next user
        
        logging.info("All users processed successfully")
        
        # Cleanup
        email_service.close()
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        print(f"Error: {e}")
        raise


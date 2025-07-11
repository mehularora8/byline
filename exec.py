import logging
import argparse
import json
from byline.utils.supabase_client import SupabaseClient
from byline.services.email_service import EmailService
from byline.utils.setup import setup_logging, load_environment_variables
from byline.services.summary_agent import ExecutiveSummaryAgent
from byline.utils.dataloaders import load_test_users

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executive Summary Agent")
    parser.add_argument("--test", action="store_true", help="Use test data from user_interests.json")
    args = parser.parse_args()
    
    setup_logging()
    env_vars = load_environment_variables()
    
    try:
        logging.info("Initializing services...")
        agent = ExecutiveSummaryAgent(env_vars["OPENAI_API_KEY"])
        email_service = EmailService(env_vars["SENDER_EMAIL"], env_vars["SENDER_PASSWORD"])

        if not args.test:
            supabase_client = SupabaseClient(env_vars["SUPABASE_URL"], env_vars["SUPABASE_SERVICE_KEY"])
            logging.info("Fetching all users from Supabase...")
            users = supabase_client.get_all_users()
        else:
            logging.info("Loading test users from user_interests.json...")
            users = load_test_users("data/user_interests.json")
        
        if not users:
            logging.warning("No users found. Exiting.")
            exit(0)
        
        logging.info(f"Processing {len(users)} users...")
        
        for user in users:
            try:
                logging.info(f"Processing user: {user.email}")
                
                if not user.user_interests:
                    logging.warning(f"User {user.email} has no interests. Skipping.")
                    continue
                
                all_summaries = []
                for user_interest in user.user_interests:
                    logging.info(f"Generating executive summary for interest: {user_interest.interest}")
                    summary = agent.create_executive_summary(user_interest)
                    all_summaries.append(summary)
                
                combined_summary = "\n".join(all_summaries)
                
                logging.info(f"Sending executive summary via email to {user.email}...")
                email_sent = email_service.send_executive_summary(user, combined_summary)
                
                if email_sent:
                    logging.info(f"Executive summary sent successfully to {user.email}")
                else:
                    logging.error(f"Failed to send email to {user.email}")
                
            except Exception as e:
                logging.error(f"Error processing user {user.email}: {e}")
                continue
        
        logging.info("All users processed.")
        
        email_service.close()
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        print(f"Error: {e}")
        raise


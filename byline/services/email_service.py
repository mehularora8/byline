import yagmail
import logging
from datetime import datetime
from byline.models.user_models import User

class EmailService:
    """Service to send executive summary reports via email"""
    
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.yag = yagmail.SMTP(sender_email, sender_password)
        logging.info(f"EmailService initialized with sender: {sender_email}")
    
    def send_executive_summary(self, user: User, summary: str) -> bool:
        """Send executive summary report to user"""
        try:
            logging.info(f"Sending executive summary to user: {user.email}")
            
            subject = self.generate_email_subject()
            
            html_content = self.generate_email_content(summary)
            
            # Send email
            self.yag.send(
                to=user.email,
                subject=subject,
                contents=html_content
            )
            
            logging.info(f"Executive summary email sent successfully to {user.email}")
            return True
            
        except Exception as e:
            error_msg = f"Failed to send email to {user.email}: {str(e)}"
            logging.error(error_msg)
            return False
    
    def close(self):
        """Close the email connection"""
        try:
            self.yag.close()
            logging.info("Email connection closed")
        except Exception as e:
            logging.error(f"Error closing email connection: {e}")

    def generate_email_subject(self) -> str:
        """Generate email subject"""
        return f"Your morning report - {datetime.now().strftime('%Y-%m-%d')}"
    
    def generate_email_content(self, summary: str) -> str:
        """Generate email content"""
        return f"""
        <html>
        <body>
            <h2>Executive Summary: {datetime.now().strftime('%Y-%m-%d')}</h2>
            <hr>
            <div style="white-space: pre-wrap; font-family: Arial, sans-serif;">
            {summary}
            </div>
            <hr>
            <p><em>This report was automatically generated based on your interests.</em></p>
        </body>
        </html>
        """



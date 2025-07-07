import json
from byline.models.user_models import User, UserInterest

def load_test_users(json_file_path: str) -> list:
    """Load users from JSON file for testing"""
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    users = []
    for email, user_data in data.items():
        user_interests = []
        for topic in user_data.get("topics", []):
            user_interests.append(UserInterest(
                interest=topic,
                subinterests=user_data.get("keywords", [])
            ))
        
        users.append(User(
            id=email,
            email=email,
            user_interests=user_interests
        ))
    
    return users
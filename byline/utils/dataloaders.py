import json
from byline.models.user_models import User, UserInterest

def load_test_users(json_file_path: str) -> list:
    """Load users from JSON file for testing"""
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    users = []
    for email, user_data in data.items():
        user_interests = []
        for interest in user_data.get("interests", []):
            user_interests.append(UserInterest(
                interest=interest.get("interest"),
                subinterests=interest.get("subinterests", [])
            ))
        
        users.append(User(
            id=email,
            email=email,
            user_interests=user_interests
        ))
    
    return users
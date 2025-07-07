from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class UserInterest:
    """Simple class to store user interests"""
    interest: str
    subinterests: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "interest": self.interest,
            "subinterests": self.subinterests
        }
    
    def __str__(self) -> str:
        return f"""
        UserInterest(
            interest={self.interest},
            subinterests={self.subinterests}
        )
        """

@dataclass
class User:
    """Simple class to store user interests"""
    id: str
    email: str
    user_interests: List[UserInterest]
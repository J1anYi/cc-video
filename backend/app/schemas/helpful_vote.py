from pydantic import BaseModel


class HelpfulVoteResponse(BaseModel):
    review_id: int
    helpful_count: int
    user_voted: bool


class HelpfulVoteToggleResponse(BaseModel):
    review_id: int
    helpful_count: int
    voted: bool

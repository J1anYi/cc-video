import strawberry
from strawberry.tools import merge_types
from strawberry.fastapi import GraphQLRouter

from app.graphql.queries import UserQuery, MovieQuery, RatingQuery, ReviewQuery
from app.graphql.mutations import AuthMutation, UserMutation, RatingMutation, ReviewMutation
from app.graphql.subscriptions import NotificationSubscription, RatingSubscription


# Merge all queries
Query = merge_types(
    "Query",
    (UserQuery, MovieQuery, RatingQuery, ReviewQuery),
)

# Merge all mutations
Mutation = merge_types(
    "Mutation",
    (AuthMutation, UserMutation, RatingMutation, ReviewMutation),
)

# Merge all subscriptions
Subscription = merge_types(
    "Subscription",
    (NotificationSubscription, RatingSubscription),
)


# Create the schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)


def get_graphql_router():
    """Create GraphQL router with context dependency."""
    from strawberry.fastapi import GraphQLRouter
    from app.database import get_db
    from app.routes.auth import get_current_user
    
    async def get_context(dependencies):
        db = dependencies.get("db")
        user = dependencies.get("user")
        return {"db": db, "user": user}
    
    return GraphQLRouter(
        schema,
        context_getter=get_context,
        graphiql=True,
    )

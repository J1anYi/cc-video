from fastapi import APIRouter, Depends, Request
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.graphql.schema import schema
from app.dependencies import get_current_user_optional


async def get_context(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    user = await get_current_user_optional(request)
    return {"db": db, "user": user, "request": request}


graphql_router = APIRouter()

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

graphql_router.include_router(graphql_app, prefix="/graphql")

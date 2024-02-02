from fastapi import Depends, HTTPException

from auth.schema import UserRole, User, TokenUser
from auth.token_service import verify_access_token


def check_permissions(user_role: UserRole, required_role: UserRole):
    if user_role != required_role:
        raise HTTPException(status_code=403, detail="Insufficient permissions")


async def require_admin_permission(current_user: dict = Depends(verify_access_token)):
    token_user = TokenUser.model_validate(current_user)
    check_permissions(token_user.role, UserRole.ADMIN)

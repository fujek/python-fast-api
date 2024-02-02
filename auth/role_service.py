from fastapi import Depends, HTTPException

from auth.schema import UserRole, User, TokenUser
from auth.token_service import verify_access_token


def check_permissions(user_role: UserRole, required_role: UserRole):
    if user_role != required_role:
        raise HTTPException(status_code=403, detail="Insufficient permissions")


async def require_admin_permission(current_user: TokenUser = Depends(verify_access_token)):
    check_permissions(current_user.role, UserRole.ADMIN)

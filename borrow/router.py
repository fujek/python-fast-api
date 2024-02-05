from typing import Sequence, Optional

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlmodel import Session, select

from auth.schema import TokenUser
from auth.token_service import verify_access_token
from borrow.schema import BorrowInput, Borrow
from db.config import get_session

router = APIRouter(prefix="/api/borrowings")


@router.post("/")
async def borrow_book(borrow_data: BorrowInput, current_user: TokenUser = Depends(verify_access_token),
                      session: Session = Depends(get_session)) -> Borrow:
    borrow = Borrow(book_id=borrow_data.book_id, user_id=current_user.user_id)
    session.add(borrow)
    session.commit()
    session.refresh(borrow)
    return borrow


@router.put("/{borrow_id}/return")
async def return_book(borrow_id: int, current_user: TokenUser = Depends(verify_access_token),
                      session: Session = Depends(get_session)) -> Borrow:
    borrow: Optional[Borrow] = await get_borrow(borrow_id, current_user, session)
    borrow.return_date = datetime.utcnow()
    session.commit()
    return borrow


@router.get("/{borrow_id}")
async def return_book(borrow_id: int, current_user: TokenUser = Depends(verify_access_token),
                      session: Session = Depends(get_session)) -> Borrow:
    borrow = await get_borrow(borrow_id, current_user, session)
    return borrow


async def get_borrow(borrow_id: int, current_user: TokenUser, session: Session) -> Optional[Borrow]:
    borrow: Optional[Borrow] = session.get(Borrow, borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    if borrow.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this borrowing")
    return borrow


@router.get("/")
async def get_user_borrowings(current_user: TokenUser = Depends(verify_access_token),
                              session: Session = Depends(get_session)) -> Sequence[Borrow]:
    query = select(Borrow).where(Borrow.user_id == current_user.user_id)
    borrowings = session.exec(query).all()
    return borrowings

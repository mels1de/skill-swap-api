from fastapi import APIRouter,Depends,HTTPException,status,Security
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate,UserOut,Token
from app.core.security import hash_password,verify_password,create_access_token,verify_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
security = HTTPBearer()

print(" AUTH ROUTER LOADED")

@router.post("/register",response_model=UserOut)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    print(" register called")
    try:
        result = await session.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalars().first()

        if existing_user:
            print(" User already exists!")
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_pw = hash_password(user_data.password)
        new_user = User(email=user_data.email, hashed_password=hashed_pw)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        print(" Registered user:", new_user.email)
        return new_user

    except Exception as e:
        print(" Exception in /register:", e)
        raise HTTPException(status_code=500, detail="Internal error during registration")



@router.post("/login", response_model = Token)
async def login(form_data: OAuth2PasswordRequestForm =Depends(), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: AsyncSession = Depends(get_async_session)
) -> User:
    token = credentials.credentials
    print(f"token: {token}")

    if token.startswith("Bearer "):
        token=token[7:].strip()


    try:
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token invalid")

        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user



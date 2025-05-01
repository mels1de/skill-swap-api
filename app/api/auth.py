from fastapi import APIRouter,Depends,HTTPException,status,Security
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate,UserOut,Token
from app.core.security import hash_password,verify_password,create_access_token,verify_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

async def get_current_user(token: str = Security(oauth2_scheme),session: AsyncSession = Depends(get_async_session)):
    print("Received token:", token)
    if not token:
        raise HTTPException(status_code=401,detail="token is missing")
    payload = verify_access_token(token)
    print("payload",payload)

    if not payload:
        raise HTTPException(status_code=401,detail="invalid token")

    email = payload.get("sub")
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code = 404,detail = "user not found")

    return user

@router.get("/me", response_model=UserOut, dependencies=[Depends(oauth2_scheme)])
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user



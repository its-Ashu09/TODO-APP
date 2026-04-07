from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer # Automatically header se token extract karega 
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from sqlalchemy.future import select
from TODO import token,models
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

async def get_current_user(data: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
      credentials_exception = HTTPException(  
        status_code=status.HTTP_401_UNAUTHORIZED, #if token is invalid then it will return 401 error
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
      )
    
    
      #now token automaticaly goes into data variable and we have to verify it.
      token_data = token.verify_token(data, credentials_exception)

      result = await db.execute(
      select(models.User).where(models.User.id == token_data.user_id)
      )

      user = result.scalar_one_or_none()
      if user is None:
            raise credentials_exception

      return user
    
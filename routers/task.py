from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from TODO import schemas,database,oauth2,models
from typing import List

router = APIRouter(
    tags=["Tasks"]
)

#create tasks
@router.post("/create",response_model=schemas.ShowTask,status_code=status.HTTP_201_CREATED)
async def create(request:schemas.CreateTask,db:AsyncSession=Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
    new_task = models.Task(

        title = request.title,
        description = request.description,
        user_id = current_user.id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task

#get tasks
@router.get("/get", response_model=List[schemas.ShowTask])
async def get_tasks(
    db: AsyncSession = Depends(database.get_db),
    current_user = Depends(oauth2.get_current_user)
):
    result = await db.execute(
        select(models.Task).where(models.Task.user_id == current_user.id)
    )
    tasks = result.scalars().all()

    return tasks

#update tasks
@router.put("/update/{task_id}",response_model=schemas.ShowTask,status_code=status.HTTP_202_ACCEPTED)
async def update(
    
    task_id:int,
    request:schemas.CreateTask,
    db: AsyncSession = Depends(database.get_db),
    current_user = Depends(oauth2.get_current_user)
  ):
                 
                
  result = await db.execute(
     select(models.Task).where(models.Task.id==task_id,models.Task.user_id==current_user.id)

  )
  task = result.scalar_one_or_none()
  if not task:
     raise HTTPException(
        status_code=404,
        detail="Task not found"
     )  
  task.title = request.title
  task.description = request.description

  await db.commit()
  await db.refresh(task)
  
  return task  

@router.delete('/delete/{task_id}',status_code=200)
async def delete_task(task_id:int,db:AsyncSession=Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
   result = await db.execute(
      select(models.Task).where(models.Task.id==task_id,models.Task.user_id==current_user.id)
   )
   task = result.scalar_one_or_none()
   if not task:
      raise HTTPException(
         status_code=404,
         detail="task not found"
      )
   
   await db.delete(task)
   await db.commit()
   
   return {"detail":"Task deleted successfully"}
   
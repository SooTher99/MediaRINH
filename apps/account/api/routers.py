from fastapi import APIRouter, Depends

from random import shuffle

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select


from apps.account.api.models import User, UsersChannelModel, ChannelsModel
from conf.database import get_async_session


router = APIRouter()

# @router.get('/test/')
# async def get_user_test(session: AsyncSession = Depends(get_async_session)):
#     stmt = select(User.id)
#
#     users = await session.scalars(stmt)
#
#     stmt = select(UsersChannelModel).join(User).join(ChannelsModel)
#     print(stmt)
#     users_channel = await session.scalars(stmt)
#     print(users_channel.all())
#     await session.close()
#     return {
#         "status": "success",
#         "data": users.all(),
#         "details": None
#     }

@router.get('/test/')
async def get_user_test(session: Session = Depends(get_async_session)):
    stmt = select(User.id)

    users = session.scalars(stmt).all()

    stmt = select(UsersChannelModel).join(User).join(ChannelsModel)
    users_channel = session.scalars(stmt).all()


    session.close()
    return {
        "status": "success",
        "data": users,
        "details": None
    }

async def insertion_sort(alist: list):
    for i in range(1, len(alist)):
        temp = alist[i]
        j = i - 1
        while j >= 0 and temp < alist[j]:
            alist[j + 1] = alist[j]
            j = j - 1
        alist[j + 1] = temp


@router.get('/test1/')
async def get_user_test():
    random_list_of_nums = list(range(0, 1_000))
    shuffle(random_list_of_nums)
    await insertion_sort(random_list_of_nums)

    return {
        "status": "success",
        "data": random_list_of_nums,
        "details": None
    }
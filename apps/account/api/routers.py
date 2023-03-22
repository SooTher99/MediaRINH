from fastapi import APIRouter
from random import shuffle

router = APIRouter()

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
from fastapi import APIRouter, HTTPException, Depends

from app.data.repositories.readers_repository import ReadersRepository

from app.api.deps import get_readers_repository


router = APIRouter()


@router.get('/recommendation')
async def get_recommendation_for_reader(reader_id: int,
                                        readers_repository: ReadersRepository = Depends(get_readers_repository)):
    """
    Get recommendations for reader
    """
    if reader_id is None:
        raise HTTPException(
            status_code=400,
            detail='Provide reader id'
        )
    reader = readers_repository.get_reader_by_id(reader_id=reader_id)
    if reader is None:
        raise HTTPException(
            status_code=404,
            detail='Reader not found'
        )

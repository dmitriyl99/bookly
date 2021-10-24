from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from app.data.repositories import BooksRepository
from app.core.recommendation import RecommendationSystem

from app.api.deps import get_recommendation_service, get_books_repository


router = APIRouter()


@router.get('/recommendation')
async def get_recommendation_for_reader(books_repository: BooksRepository = Depends(get_books_repository),
                                        rec_service: RecommendationSystem = Depends(get_recommendation_service),
                                        reader_id: Optional[int] = None):
    """
    Get recommendations for reader
    """
    if reader_id == 0:
        reader_id = None
    recommendations, history = rec_service.get_recommendations_for_reader(reader_id=reader_id)
    recommendations_response = []
    history_response = []
    recommendation_books = books_repository.get_books_by_ids(recommendations)
    history_books = books_repository.get_books_by_ids(history)
    for book in recommendation_books:
        recommendations_response.append({
            'id': book[0],
            'title': book[1],
            'author': book[2]
        })
    for book in history_books:
        history_response.append({
            'id': book[0],
            'title': book[1],
            'author': book[2]
        })

    return {
        'data': {
            'recommendations': recommendations_response,
            'history': history_response
        }
    }

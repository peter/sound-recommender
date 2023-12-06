from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

# Root redirects to OpenAPI documentation
@router.get("/")
def root():
    return RedirectResponse(url='/docs')

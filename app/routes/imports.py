from fastapi import APIRouter, UploadFile, File, HTTPException
from services.import_service import import_products_from_excel

router = APIRouter(
    prefix="/imports",
    tags=["Imports"]
)


@router.post("/products")
async def import_products(file: UploadFile = File(...)):

    try:
        result = await import_products_from_excel(file)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected server error during import: {str(e)}"
        )
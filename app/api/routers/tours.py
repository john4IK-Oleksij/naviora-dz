from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from fastapi import Form
from app.models.tour import TourBase,TourCreate, TourUpdate, TourOut, Guide
from app.services.tour_service import TourService
from fastapi.responses import RedirectResponse

router = APIRouter()
service = TourService()
templates = Jinja2Templates(directory="templates")

@router.get("/tours", response_model=list[TourOut])
async def get_tours():
    return service.get_all_tours()

@router.get("/tours/search", response_model=list[TourOut])
async def search_tours(country: str | None = None):
    return service.search_tours(country)

@router.get("/tours/{tour_id}", response_model=TourOut)
async def tours_item(tour_id: str):
    return service.get_tour_by_id(tour_id)

@router.post("/tours/", response_model=TourOut)
async def create_tour(tour: TourCreate):
    return service.create_tour(tour)

@router.put("/tours/{tour_id}", response_model=TourOut)
async def update_tour(tour_id: str, tour: TourUpdate):
    return service.update_tour(tour_id, tour)

@router.delete("/tours/{tour_id}", response_model=TourOut)
async def delete_tour(tour_id: str):
    return service.delete_tour(tour_id)

@router.get("/admin")
async def admin_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={}
    )

@router.post("/admin/tours/edit/{tour_id}")
async def update_tour(
    tour_id: str,
    title: str = Form(...),
    country: str = Form(...),
    durationDays: int = Form(...),
    price: float = Form(...),
    maxGuests: int | None = Form(None),
    cities: str = Form(...),
    guideName: str = Form(...),
    guideLanguage: str = Form(...),
    image: str = Form(...)
):
    tour = TourUpdate(
        title=title,
        country=country.strip().lower(),
        durationDays=durationDays,
        price=price,
        maxGuests=maxGuests,
        cities=[city.strip() for city in cities.split(",")],
        guide=Guide(
            name=guideName,
            language=guideLanguage
        ),
        image=image
    )
    updated_tour = service.update_tour(tour_id, tour)
    return RedirectResponse(
        url="/admin/tours",
        status_code=303
    )


@router.get("/admin/tours")
async def admin_tours_page(request: Request):
    tours = service.get_all_tours()
    return templates.TemplateResponse(
        request=request,
        name="tours.html",
        context={
            "tours": tours,
            "is_admin": True
        }
    )

@router.get("/admin/tours/edit/{tour_id}")
async def edit_tour_page(request: Request, tour_id: str):
    tour = service.get_tour_by_id(tour_id)
    return templates.TemplateResponse(
        request=request,
        name="tour_form.html",
        context={
            "tour": tour
        }
    )

@router.get("/admin/tours/add")
async def add_tour_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tour_form.html",
        context={}
    )

@router.post("/admin/tours/add")
async def create_tour(
    id: str = Form(...),
    title: str = Form(...),
    country: str = Form(...),
    durationDays: int = Form(...),
    price: float = Form(...),
    maxGuests: int | None = Form(None),
    cities: str = Form(...),
    guideName: str = Form(...),
    guideLanguage: str = Form(...),
    image: str = Form(...)
):
    tour = TourCreate(
        id=id,
        title=title,
        country=country.strip().lower(),
        durationDays=durationDays,
        price=price,
        maxGuests=maxGuests,
        cities=[city.strip() for city in cities.split(",")],
        guide=Guide(
            name=guideName,
            language=guideLanguage
        ),
        image=image
    )
    service.create_tour(tour)
    return RedirectResponse(
        url="/admin/tours",
        status_code=303
    )

@router.post("/admin/tours/delete/{tour_id}")
async def delete_tour(tour_id: str):
    service.delete_tour(tour_id)
    return RedirectResponse(
        url="/admin/tours",
        status_code=303
    )

@router.get("/contacts")
async def contacts_page(request: Request):
    message_sent = request.query_params.get("sent") == "1"
    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={
            "message_sent": message_sent
        }
    )

@router.post("/contacts")
async def send_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    message: str = Form(...)
):
    print("Name:", name)
    print("Email:", email)
    print("Phone:", phone)
    print("Message:", message)
    return RedirectResponse(
        url="/contacts?sent=1",
        status_code=303
    )

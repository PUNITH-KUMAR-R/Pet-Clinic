from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request

from app.database import Base, engine
import app.models

from app.database import SessionLocal
from app.models import Doctor, Pet, Appointment
from app.schemas import DoctorCreate, PetCreate, AppointmentCreate

#Create the template object:
templates = Jinja2Templates(directory="templates")
# Create all database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(title="Pet Clinic API")

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Doctor API
@app.post("/doctors")
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        availability=doctor.availability
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor

@app.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    return doctors


@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(doctor)
    db.commit()

    return {"message": "Doctor deleted successfully"}

@app.put("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.name = doctor_data.name
    doctor.specialization = doctor_data.specialization
    doctor.availability = doctor_data.availability

    db.commit()
    db.refresh(doctor)

    return doctor

@app.post("/pets")
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    new_pet = Pet(
        name=pet.name,
        species=pet.species,
        owner=pet.owner
    )

    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return new_pet

@app.get("/pets")
def get_pets(db: Session = Depends(get_db)):
    return db.query(Pet).all()

@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    db.delete(pet)
    db.commit()

    return {"message": "Pet deleted successfully"}

@app.put("/pets/{pet_id}")
def update_pet(
    pet_id: int,
    pet_data: PetCreate,
    db: Session = Depends(get_db)
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet.name = pet_data.name
    pet.species = pet_data.species
    pet.owner = pet_data.owner

    db.commit()
    db.refresh(pet)

    return pet

@app.post("/appointments")
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.doctor_id
    ).first()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    pet = db.query(Pet).filter(
        Pet.id == appointment.pet_id
    ).first()

    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    new_appointment = Appointment(
        doctor_id=appointment.doctor_id,
        pet_id=appointment.pet_id,
        date=appointment.date,
        time=appointment.time
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment

@app.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@app.delete("/appointments/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment deleted"}

@app.put("/appointments/{appointment_id}")
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.doctor_id = appointment_data.doctor_id
    appointment.pet_id = appointment_data.pet_id
    appointment.date = appointment_data.date
    appointment.time = appointment_data.time

    db.commit()
    db.refresh(appointment)

    return appointment

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/doctors-ui", response_class=HTMLResponse)
def doctors_page(request: Request, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()

    return templates.TemplateResponse(
        "doctors.html",
        {
            "request": request,
            "doctors": doctors
        }
    )

@app.get("/pets-ui", response_class=HTMLResponse)
def pets_page(request: Request, db: Session = Depends(get_db)):
    pets = db.query(Pet).all()

    return templates.TemplateResponse(
        "pets.html",
        {
            "request": request,
            "pets": pets
        }
    )

@app.get("/appointments-ui", response_class=HTMLResponse)
def appointments_page(request: Request, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()

    return templates.TemplateResponse(
        "appointments.html",
        {
            "request": request,
            "appointments": appointments
        }
    )

@app.post("/doctors/add")
def add_doctor(
    name: str = Form(...),
    specialization: str = Form(...),
    availability: str = Form(...),
    db: Session = Depends(get_db)
):
    doctor = Doctor(
        name=name,
        specialization=specialization,
        availability=availability
    )

    db.add(doctor)
    db.commit()

    return RedirectResponse(
        url="/doctors-ui",
        status_code=303
    )

@app.post("/doctors/delete/{doctor_id}")
def delete_doctor_ui(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    db.delete(doctor)
    db.commit()

    return RedirectResponse(
        url="/doctors-ui",
        status_code=303
    )

@app.get("/doctors/edit/{doctor_id}", response_class=HTMLResponse)
def edit_doctor_page(
    doctor_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return templates.TemplateResponse(
        "edit_doctor.html",
        {
            "request": request,
            "doctor": doctor
        }
    )

@app.post("/doctors/update/{doctor_id}")
def update_doctor_ui(
    doctor_id: int,
    name: str = Form(...),
    specialization: str = Form(...),
    availability: str = Form(...),
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.name = name
    doctor.specialization = specialization
    doctor.availability = availability

    db.commit()

    return RedirectResponse(
        url="/doctors-ui",
        status_code=303
    )

@app.post("/pets/add")
def add_pet(
    name: str = Form(...),
    species: str = Form(...),
    owner: str = Form(...),
    db: Session = Depends(get_db)
):

    pet = Pet(
        name=name,
        species=species,
        owner=owner
    )

    db.add(pet)
    db.commit()

    return RedirectResponse(
        url="/pets-ui",
        status_code=303
    )

@app.post("/pets/delete/{pet_id}")
def delete_pet_ui(
    pet_id: int,
    db: Session = Depends(get_db)
):

    pet = db.query(Pet).filter(
        Pet.id == pet_id
    ).first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    db.delete(pet)
    db.commit()

    return RedirectResponse(
        url="/pets-ui",
        status_code=303
    )

@app.get("/pets/edit/{pet_id}", response_class=HTMLResponse)
def edit_pet_page(
    pet_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    pet = db.query(Pet).filter(
        Pet.id == pet_id
    ).first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    return templates.TemplateResponse(
        "edit_pet.html",
        {
            "request": request,
            "pet": pet
        }
    )

@app.post("/pets/update/{pet_id}")
def update_pet_ui(
    pet_id: int,
    name: str = Form(...),
    species: str = Form(...),
    owner: str = Form(...),
    db: Session = Depends(get_db)
):

    pet = db.query(Pet).filter(
        Pet.id == pet_id
    ).first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    pet.name = name
    pet.species = species
    pet.owner = owner

    db.commit()

    return RedirectResponse(
        url="/pets-ui",
        status_code=303
    )

@app.post("/appointments/add")
def add_appointment(
    doctor_id: int = Form(...),
    pet_id: int = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    db: Session = Depends(get_db)
):

    appointment = Appointment(
        doctor_id=doctor_id,
        pet_id=pet_id,
        date=date,
        time=time
    )

    db.add(appointment)
    db.commit()

    return RedirectResponse(
        url="/appointments-ui",
        status_code=303
    )

@app.post("/appointments/delete/{appointment_id}")
def delete_appointment_ui(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return RedirectResponse(
        url="/appointments-ui",
        status_code=303
    )

@app.get("/appointments/edit/{appointment_id}",
         response_class=HTMLResponse)
def edit_appointment_page(
    appointment_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return templates.TemplateResponse(
        "edit_appointment.html",
        {
            "request": request,
            "appointment": appointment
        }
    )

@app.post("/appointments/update/{appointment_id}")
def update_appointment_ui(
    appointment_id: int,
    doctor_id: int = Form(...),
    pet_id: int = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.doctor_id = doctor_id
    appointment.pet_id = pet_id
    appointment.date = date
    appointment.time = time

    db.commit()

    return RedirectResponse(
        url="/appointments-ui",
        status_code=303
    )


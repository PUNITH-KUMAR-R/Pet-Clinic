from pydantic import BaseModel

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    availability: str


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True


class PetCreate(BaseModel):
    name: str
    species: str
    owner: str


class PetResponse(PetCreate):
    id: int

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    doctor_id: int
    pet_id: int
    date: str
    time: str


class AppointmentResponse(AppointmentCreate):
    id: int

    class Config:
        from_attributes = True
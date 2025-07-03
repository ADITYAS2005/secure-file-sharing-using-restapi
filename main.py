from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from . import models, schemas, database, auth, utils
from .database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Client User: Sign up
@app.post("/client/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        role=user.role,
        is_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = utils.create_download_token(
        user_id=db_user.id,
        file_id=0,
        expires_minutes=60*24
    )
    verify_link = f"http://localhost:8000/client/verify-email/{token}"
    return {"verify_link": verify_link}

# Client User: Verify email
@app.get("/client/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    payload = utils.verify_download_token(token)
    user_id = int(payload["sub"])
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.is_verified = True
        db.commit()
        return {"message": "Email verified"}
    raise HTTPException(status_code=400, detail="Invalid token")

# Login (both Ops and Client users)
@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    
    if user.role == schemas.RoleEnum.client and not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")
    
    access_token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Ops User: Upload file
@app.post("/ops/upload-file")
def upload_file(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != schemas.RoleEnum.ops:
        raise HTTPException(status_code=403, detail="Only Ops users can upload files.")
    
    ext = file.filename.split(".")[-1]
    if ext not in ["pptx", "docx", "xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    
    upload_dir = "./uploads"
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, file.filename)

    with open(filepath, "wb") as f:
        f.write(file.file.read())

    db_file = models.File(
        filename=file.filename,
        filepath=filepath,
        uploader_id=current_user.id
    )
    db.add(db_file)
    db.commit()
    return {"message": "File uploaded successfully."}

# Client User: List uploaded files
@app.get("/client/files", response_model=list[schemas.FileOut])
def list_files(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != schemas.RoleEnum.client:
        raise HTTPException(status_code=403, detail="Only clients can list files.")
    
    files = db.query(models.File).all()
    return files

# Client User: Generate secure download link
@app.get("/client/download-file/{file_id}")
def get_download_link(
    file_id: int,
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != schemas.RoleEnum.client:
        raise HTTPException(status_code=403, detail="Only clients can download files.")
    
    token = utils.create_download_token(
        user_id=current_user.id,
        file_id=file_id,
        expires_minutes=15
    )
    download_url = f"http://localhost:8000/client/secure-download/{token}"
    return {"download-link": download_url}

# Client User: Secure download endpoint
@app.get("/client/secure-download/{token}")
def secure_download(
    token: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    payload = utils.verify_download_token(token)
    if int(payload["sub"]) != current_user.id:
        raise HTTPException(status_code=403, detail="Token is not valid for this user.")
    
    file_id = payload["file_id"]
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found.")
    
    return FileResponse(path=file.filepath, filename=file.filename)

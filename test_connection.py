from app.database import engine, Base
from app.models import Note   # yahan import karna zaroori hai — kyun?

Base.metadata.create_all(bind=engine)
print("✅ Tables created (or already exist)")

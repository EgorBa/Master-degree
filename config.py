import dotenv
import os

dotenv.load_dotenv()

DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_COLUMN = os.getenv("DATABASE_COLUMN")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_N = os.getenv("DATABASE_N")

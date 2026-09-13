import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")
PROFILE_FOLDER = os.path.join(BASE_DIR, "data", "profiles")
GENERATED_FOLDER = os.path.join(BASE_DIR, "data", "generated")

ALLOWED_EXTENSIONS = {"xlsx", "xls"}

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
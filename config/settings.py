from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
DATABASE_URL = "postgresql://localhost/courstack"
JWT_SECRET = "89c955a5-6c12-4bf0-b55f-9f9c35f33feb"
UPLOAD_FOLDER = BASE_DIR / "upload"
QINIU_AK = "eAv2YAZwRlBZHju1nYXJi5QyW5D0ByhP97sIrbvO"
QINIU_SK = "Rd-y4xT5ANK5IEgx37_A76F5JymyRrqzeTxS1Qmt"
QINIU_RTC_APPID = "fmujzfeyf"

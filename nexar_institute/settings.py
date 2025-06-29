from pathlib import Path
import os
import dotenv
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / '.env'
dotenv.load_dotenv(dotenv_path=dotenv_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", ".now.sh"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My apps
    'core.apps.CoreConfig',
    'programs.apps.ProgramsConfig',
    'admissions.apps.AdmissionsConfig',
    'contact.apps.ContactConfig',
    'cms.apps.CmsConfig',
    'whitenoise.runserver_nostatic',
    'cloudinary',
    'cloudinary_storage', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nexar_institute.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Add 'templates' directory to DIRS
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{'cms_tags': 'cms.templatetags.cms_tags',}
        },
    },
]

WSGI_APPLICATION = 'nexar_institute.wsgi.application'

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'HOST': os.getenv('PGHOST'),
        'PORT': os.getenv('PGPORT', '5432'),
        'OPTIONS': {
            'sslmode': os.getenv('PGSSLMODE', 'require'),
            'channel_binding': os.getenv('PGCHANNELBINDING', 'require'),
        }
    }
}

import psycopg2
try:
    conn = psycopg2.connect(
        dbname=os.getenv('PGDATABASE'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        host=os.getenv('PGHOST'),
        port=os.getenv('PGPORT', '5432'),
        sslmode=os.getenv('PGSSLMODE', 'require'),
        #options='-c channel_binding=require'
    )
    conn.close()
except Exception as e:
    print("❌ DATABASE CONNECTION FAILED:", e)

"""

# MySQL Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # Use os.getenv to read from environment variables
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


SQL Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka' # Set to Zambia's timezone
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

# Cloudinary Configuration
# ========================
cloudinary.config(
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key = os.getenv('CLOUDINARY_API_KEY'),
  api_secret = os.getenv('CLOUDINARY_API_SECRET'),
  secure = True 
)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Static files settings (Keep your Whitenoise setup)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = BASE_DIR / "staticfiles_build"

# Static files settings (Keep your Whitenoise setup)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration (for contact form - configure for your provider)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Use SMTP in production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # For development: prints email to console
EMAIL_HOST = 'smtp.example.com' # Replace with your SMTP host
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com' # Replace with your email
EMAIL_HOST_PASSWORD = 'your-email-password' # Replace with your password
DEFAULT_FROM_EMAIL = 'webmaster@nexarinstitute.com' # Or your email
ADMIN_EMAIL = 'admin@nexarinstitute.com' # Email to send contact forms to
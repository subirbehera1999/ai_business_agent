# ==============================================================================
# File: app/config/settings.py
# Purpose: Loads, validates, and exposes all environment variables as typed
#          settings using Pydantic BaseSettings. Single source of truth for
#          all configuration across the entire application.
# ==============================================================================

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ------------------------------------------------------------------------------
# Application Settings
# ------------------------------------------------------------------------------

class AppSettings(BaseSettings):
    """Core application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_ENV: str = Field(default="production", description="Deployment environment")
    APP_NAME: str = Field(default="AI Business Agent")
    APP_VERSION: str = Field(default="1.0.0")
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    APP_SECRET_KEY: str = Field(..., min_length=32, description="App secret key")
    APP_DEBUG: bool = Field(default=False)
    ALLOWED_ORIGINS: str = Field(default="")

    @field_validator("APP_ENV")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"APP_ENV must be one of {allowed}")
        return v

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse comma-separated ALLOWED_ORIGINS into a list."""
        if not self.ALLOWED_ORIGINS:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


# ------------------------------------------------------------------------------
# Database Settings
# ------------------------------------------------------------------------------

class DatabaseSettings(BaseSettings):
    """PostgreSQL database configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    DATABASE_URL: str = Field(..., description="PostgreSQL async connection string")
    DATABASE_POOL_SIZE: int = Field(default=10, ge=1, le=100)
    DATABASE_MAX_OVERFLOW: int = Field(default=20, ge=0, le=100)
    DATABASE_POOL_TIMEOUT: int = Field(default=30, ge=5, le=120)
    DATABASE_ECHO: bool = Field(default=False)

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v


# ------------------------------------------------------------------------------
# OpenAI Settings
# ------------------------------------------------------------------------------

class OpenAISettings(BaseSettings):
    """OpenAI API configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    OPENAI_API_KEY: str = Field(..., description="OpenAI secret API key")
    OPENAI_MODEL: str = Field(default="gpt-4o")
    OPENAI_MAX_TOKENS: int = Field(default=1000, ge=100, le=8000)
    OPENAI_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=2.0)
    OPENAI_REQUEST_TIMEOUT: int = Field(default=30, ge=5, le=120)

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        if not v.startswith("sk-"):
            raise ValueError("OPENAI_API_KEY must start with 'sk-'")
        return v


# ------------------------------------------------------------------------------
# Razorpay Settings
# ------------------------------------------------------------------------------

class RazorpaySettings(BaseSettings):
    """Razorpay payment gateway configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    RAZORPAY_KEY_ID: str = Field(..., description="Razorpay key ID")
    RAZORPAY_KEY_SECRET: str = Field(..., description="Razorpay key secret")
    RAZORPAY_WEBHOOK_SECRET: str = Field(..., description="Razorpay webhook signing secret")
    RAZORPAY_CURRENCY: str = Field(default="INR")

    @field_validator("RAZORPAY_KEY_ID")
    @classmethod
    def validate_razorpay_key_id(cls, v: str) -> str:
        if not v.startswith("rzp_"):
            raise ValueError("RAZORPAY_KEY_ID must start with 'rzp_'")
        return v


# ------------------------------------------------------------------------------
# WhatsApp Settings
# ------------------------------------------------------------------------------

class WhatsAppSettings(BaseSettings):
    """WhatsApp Cloud API configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    WHATSAPP_API_TOKEN: str = Field(..., description="WhatsApp Cloud API token")
    WHATSAPP_PHONE_NUMBER_ID: str = Field(..., description="WhatsApp sender phone number ID")
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = Field(..., description="WhatsApp Business Account ID")
    WHATSAPP_API_VERSION: str = Field(default="v19.0")
    WHATSAPP_API_BASE_URL: str = Field(default="https://graph.facebook.com")

    @property
    def whatsapp_messages_url(self) -> str:
        """Construct the full WhatsApp messages endpoint URL."""
        return (
            f"{self.WHATSAPP_API_BASE_URL}/{self.WHATSAPP_API_VERSION}"
            f"/{self.WHATSAPP_PHONE_NUMBER_ID}/messages"
        )


# ------------------------------------------------------------------------------
# Google Settings
# ------------------------------------------------------------------------------

class GoogleSettings(BaseSettings):
    """Google API configuration for Reviews and Sheets."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    GOOGLE_API_KEY: str = Field(..., description="Google API key")
    GOOGLE_CLIENT_ID: str = Field(..., description="Google OAuth client ID")
    GOOGLE_CLIENT_SECRET: str = Field(..., description="Google OAuth client secret")
    GOOGLE_REDIRECT_URI: str = Field(..., description="Google OAuth redirect URI")
    GOOGLE_PLACES_API_KEY: str = Field(..., description="Google Places API key")
    GOOGLE_SERVICE_ACCOUNT_JSON_PATH: str = Field(
        ..., description="Path to Google service account JSON"
    )


# ------------------------------------------------------------------------------
# Admin Settings
# ------------------------------------------------------------------------------

class AdminSettings(BaseSettings):
    """Admin monitoring and alerting configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ADMIN_WHATSAPP_NUMBER: str = Field(..., description="Admin WhatsApp number with country code")
    ADMIN_EMAIL: str = Field(..., description="Admin email address")
    ADMIN_SECRET_TOKEN: str = Field(..., min_length=16, description="Admin internal API token")

    @field_validator("ADMIN_WHATSAPP_NUMBER")
    @classmethod
    def validate_whatsapp_number(cls, v: str) -> str:
        if not v.startswith("+"):
            raise ValueError("ADMIN_WHATSAPP_NUMBER must include country code (e.g., +91...)")
        return v


# ------------------------------------------------------------------------------
# Scheduler Settings
# ------------------------------------------------------------------------------

class SchedulerSettings(BaseSettings):
    """Background scheduler and cron configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    SCHEDULER_REVIEW_POLL_INTERVAL_MINUTES: int = Field(default=15, ge=5, le=60)
    SCHEDULER_SALES_ANALYSIS_CRON: str = Field(default="0 7 * * *")
    SCHEDULER_WEEKLY_REPORT_CRON: str = Field(default="0 8 * * 1")
    SCHEDULER_MONTHLY_REPORT_CRON: str = Field(default="0 8 1 * *")
    SCHEDULER_QUARTERLY_REPORT_CRON: str = Field(default="0 8 1 1,4,7,10 *")
    SCHEDULER_WEEKLY_CONTENT_CRON: str = Field(default="0 9 * * 1")
    SCHEDULER_EXPIRY_CHECK_CRON: str = Field(default="0 6 * * *")
    SCHEDULER_HEALTH_REPORT_CRON: str = Field(default="0 8 * * *")
    SCHEDULER_JOB_LOCK_TTL_SECONDS: int = Field(default=900, ge=60, le=3600)


# ------------------------------------------------------------------------------
# Usage Limit Settings
# ------------------------------------------------------------------------------

class UsageLimitSettings(BaseSettings):
    """Default daily usage caps enforced before subscription plan overrides."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    MAX_REVIEWS_PER_DAY: int = Field(default=100, ge=1)
    MAX_AI_REPLIES_PER_DAY: int = Field(default=200, ge=1)
    MAX_COMPETITOR_SCANS_PER_DAY: int = Field(default=10, ge=1)
    MAX_REPORTS_PER_DAY: int = Field(default=5, ge=1)


# ------------------------------------------------------------------------------
# Retry Policy Settings
# ------------------------------------------------------------------------------

class RetrySettings(BaseSettings):
    """External API retry and backoff configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    RETRY_MAX_ATTEMPTS: int = Field(default=3, ge=1, le=10)
    RETRY_BACKOFF_DELAYS: str = Field(default="2,5,10")

    @property
    def backoff_delays_list(self) -> List[int]:
        """Parse comma-separated delay string into a list of integers."""
        return [int(d.strip()) for d in self.RETRY_BACKOFF_DELAYS.split(",") if d.strip()]


# ------------------------------------------------------------------------------
# Security Settings
# ------------------------------------------------------------------------------

class SecuritySettings(BaseSettings):
    """JWT and encryption configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    JWT_SECRET_KEY: str = Field(..., min_length=32, description="JWT signing secret")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, ge=5, le=1440)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30, ge=1, le=90)
    ENCRYPTION_KEY: str = Field(..., description="Fernet encryption key (base64 encoded)")

    @field_validator("JWT_ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: str) -> str:
        allowed = {"HS256", "HS384", "HS512"}
        if v not in allowed:
            raise ValueError(f"JWT_ALGORITHM must be one of {allowed}")
        return v


# ------------------------------------------------------------------------------
# Logging Settings
# ------------------------------------------------------------------------------

class LoggingSettings(BaseSettings):
    """Logging and error tracking configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")
    LOG_FILE_PATH: str = Field(default="/var/log/ai_business_agent/app.log")
    LOG_ROTATION: str = Field(default="daily")
    LOG_RETENTION_DAYS: int = Field(default=30, ge=1, le=365)
    SENTRY_DSN: str = Field(default="")

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()


# ------------------------------------------------------------------------------
# Feedback Settings
# ------------------------------------------------------------------------------

class FeedbackSettings(BaseSettings):
    """Testimonial and feedback collection configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    FEEDBACK_GOOGLE_FORM_URL: str = Field(..., description="Google Form URL for feedback")
    FEEDBACK_REQUEST_DELAY_DAYS: int = Field(default=30, ge=1, le=365)


# ------------------------------------------------------------------------------
# Rate Limiting Settings
# ------------------------------------------------------------------------------

class RateLimitSettings(BaseSettings):
    """API rate limiting configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, ge=1)
    RATE_LIMIT_BURST: int = Field(default=10, ge=1)


# ------------------------------------------------------------------------------
# Batch Processing Settings
# ------------------------------------------------------------------------------

class BatchSettings(BaseSettings):
    """Batch processing size configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    BATCH_SIZE_BUSINESSES: int = Field(default=20, ge=1, le=100)
    BATCH_SIZE_RECORDS: int = Field(default=50, ge=1, le=500)


# ==============================================================================
# Master Settings — Aggregates all setting groups
# ==============================================================================

class Settings(BaseSettings):
    """
    Master settings object that composes all subsystem configurations.

    Loaded once at startup via get_settings() and cached for the
    application lifetime using lru_cache.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────────
    APP_ENV: str = Field(default="production")
    APP_NAME: str = Field(default="AI Business Agent")
    APP_VERSION: str = Field(default="1.0.0")
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    APP_SECRET_KEY: str = Field(..., min_length=32)
    APP_DEBUG: bool = Field(default=False)
    ALLOWED_ORIGINS: str = Field(default="")

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: str = Field(...)
    DATABASE_POOL_SIZE: int = Field(default=10, ge=1, le=100)
    DATABASE_MAX_OVERFLOW: int = Field(default=20, ge=0, le=100)
    DATABASE_POOL_TIMEOUT: int = Field(default=30, ge=5, le=120)
    DATABASE_ECHO: bool = Field(default=False)

    # ── OpenAI ───────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = Field(...)
    OPENAI_MODEL: str = Field(default="gpt-4o")
    OPENAI_MAX_TOKENS: int = Field(default=1000, ge=100, le=8000)
    OPENAI_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=2.0)
    OPENAI_REQUEST_TIMEOUT: int = Field(default=30, ge=5, le=120)

    # ── Razorpay ─────────────────────────────────────────────────────────────
    RAZORPAY_KEY_ID: str = Field(...)
    RAZORPAY_KEY_SECRET: str = Field(...)
    RAZORPAY_WEBHOOK_SECRET: str = Field(...)
    RAZORPAY_CURRENCY: str = Field(default="INR")

    # ── WhatsApp ─────────────────────────────────────────────────────────────
    WHATSAPP_API_TOKEN: str = Field(...)
    WHATSAPP_PHONE_NUMBER_ID: str = Field(...)
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = Field(...)
    WHATSAPP_API_VERSION: str = Field(default="v19.0")
    WHATSAPP_API_BASE_URL: str = Field(default="https://graph.facebook.com")

    # ── Google ───────────────────────────────────────────────────────────────
    GOOGLE_API_KEY: str = Field(...)
    GOOGLE_CLIENT_ID: str = Field(...)
    GOOGLE_CLIENT_SECRET: str = Field(...)
    GOOGLE_REDIRECT_URI: str = Field(...)
    GOOGLE_PLACES_API_KEY: str = Field(...)
    GOOGLE_SERVICE_ACCOUNT_JSON_PATH: str = Field(...)

    # ── Admin ────────────────────────────────────────────────────────────────
    ADMIN_WHATSAPP_NUMBER: str = Field(...)
    ADMIN_EMAIL: str = Field(...)
    ADMIN_SECRET_TOKEN: str = Field(..., min_length=16)

    # ── Scheduler ────────────────────────────────────────────────────────────
    SCHEDULER_REVIEW_POLL_INTERVAL_MINUTES: int = Field(default=15, ge=5, le=60)
    SCHEDULER_SALES_ANALYSIS_CRON: str = Field(default="0 7 * * *")
    SCHEDULER_WEEKLY_REPORT_CRON: str = Field(default="0 8 * * 1")
    SCHEDULER_MONTHLY_REPORT_CRON: str = Field(default="0 8 1 * *")
    SCHEDULER_QUARTERLY_REPORT_CRON: str = Field(default="0 8 1 1,4,7,10 *")
    SCHEDULER_WEEKLY_CONTENT_CRON: str = Field(default="0 9 * * 1")
    SCHEDULER_EXPIRY_CHECK_CRON: str = Field(default="0 6 * * *")
    SCHEDULER_HEALTH_REPORT_CRON: str = Field(default="0 8 * * *")
    SCHEDULER_JOB_LOCK_TTL_SECONDS: int = Field(default=900, ge=60, le=3600)

    # ── Usage Limits ─────────────────────────────────────────────────────────
    MAX_REVIEWS_PER_DAY: int = Field(default=100, ge=1)
    MAX_AI_REPLIES_PER_DAY: int = Field(default=200, ge=1)
    MAX_COMPETITOR_SCANS_PER_DAY: int = Field(default=10, ge=1)
    MAX_REPORTS_PER_DAY: int = Field(default=5, ge=1)

    # ── Retry Policy ─────────────────────────────────────────────────────────
    RETRY_MAX_ATTEMPTS: int = Field(default=3, ge=1, le=10)
    RETRY_BACKOFF_DELAYS: str = Field(default="2,5,10")

    # ── Security ─────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, ge=5, le=1440)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30, ge=1, le=90)
    ENCRYPTION_KEY: str = Field(...)

    # ── Logging ──────────────────────────────────────────────────────────────
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")
    LOG_FILE_PATH: str = Field(default="/var/log/ai_business_agent/app.log")
    LOG_ROTATION: str = Field(default="daily")
    LOG_RETENTION_DAYS: int = Field(default=30, ge=1, le=365)
    SENTRY_DSN: str = Field(default="")

    # ── Feedback ─────────────────────────────────────────────────────────────
    FEEDBACK_GOOGLE_FORM_URL: str = Field(...)
    FEEDBACK_REQUEST_DELAY_DAYS: int = Field(default=30, ge=1, le=365)

    # ── Rate Limiting ─────────────────────────────────────────────────────────
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, ge=1)
    RATE_LIMIT_BURST: int = Field(default=10, ge=1)

    # ── Batch Processing ──────────────────────────────────────────────────────
    BATCH_SIZE_BUSINESSES: int = Field(default=20, ge=1, le=100)
    BATCH_SIZE_RECORDS: int = Field(default=50, ge=1, le=500)

    # ── Computed Properties ───────────────────────────────────────────────────

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse comma-separated ALLOWED_ORIGINS into a list."""
        if not self.ALLOWED_ORIGINS:
            return []
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    @property
    def backoff_delays_list(self) -> List[int]:
        """Parse comma-separated RETRY_BACKOFF_DELAYS into a list of ints."""
        return [int(d.strip()) for d in self.RETRY_BACKOFF_DELAYS.split(",") if d.strip()]

    @property
    def whatsapp_messages_url(self) -> str:
        """Construct the full WhatsApp messages endpoint URL."""
        return (
            f"{self.WHATSAPP_API_BASE_URL}/{self.WHATSAPP_API_VERSION}"
            f"/{self.WHATSAPP_PHONE_NUMBER_ID}/messages"
        )

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    # ── Cross-field Validators ────────────────────────────────────────────────

    @model_validator(mode="after")
    def validate_production_requirements(self) -> "Settings":
        """Enforce stricter checks in production environment."""
        if self.APP_ENV == "production":
            if self.APP_DEBUG:
                raise ValueError("APP_DEBUG must be False in production")
            if not self.SENTRY_DSN:
                # Warn but don't hard-fail — Sentry is recommended not mandatory
                pass
            if not self.ALLOWED_ORIGINS:
                raise ValueError("ALLOWED_ORIGINS must be set in production")
        return self

    @field_validator("APP_ENV")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"APP_ENV must be one of {allowed}")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()

    @field_validator("JWT_ALGORITHM")
    @classmethod
    def validate_jwt_algorithm(cls, v: str) -> str:
        allowed = {"HS256", "HS384", "HS512"}
        if v not in allowed:
            raise ValueError(f"JWT_ALGORITHM must be one of {allowed}")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        if not v.startswith("sk-"):
            raise ValueError("OPENAI_API_KEY must start with 'sk-'")
        return v

    @field_validator("RAZORPAY_KEY_ID")
    @classmethod
    def validate_razorpay_key(cls, v: str) -> str:
        if not v.startswith("rzp_"):
            raise ValueError("RAZORPAY_KEY_ID must start with 'rzp_'")
        return v

    @field_validator("ADMIN_WHATSAPP_NUMBER")
    @classmethod
    def validate_admin_whatsapp(cls, v: str) -> str:
        if not v.startswith("+"):
            raise ValueError("ADMIN_WHATSAPP_NUMBER must include country code (e.g., +91...)")
        return v


# ==============================================================================
# Cached Settings Loader
# ==============================================================================

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached singleton instance of Settings.

    Use this function everywhere in the application to access configuration.
    The lru_cache ensures the .env file is read only once at startup.

    Usage:
        from app.config.settings import get_settings
        settings = get_settings()
        print(settings.DATABASE_URL)
    """
    return Settings()
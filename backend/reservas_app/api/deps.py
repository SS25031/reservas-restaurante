"""Dependencias compartidas de la capa API."""

from fastapi import Depends
from sqlalchemy.orm import Session

from reservas_app.db import get_db
from reservas_app.services.onboarding_service import OnboardingService


def get_onboarding_service(db: Session = Depends(get_db)) -> OnboardingService:
    return OnboardingService(db)

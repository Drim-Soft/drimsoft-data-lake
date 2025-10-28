# ETL/models/__init__.py
from sqlalchemy.ext.declarative import declarative_base

# ======================================================
# DEFINICIÓN DE BASES SEPARADAS POR BASE DE DATOS
# ======================================================

BaseDrimsoft = declarative_base()
BasePlanifika = declarative_base()
BaseProyectos = declarative_base()
BaseSuscripciones = declarative_base()

# ======================================================
# IMPORTAR MODELOS CON SUS BASES RESPECTIVAS
# ======================================================

# --- SUSCRIPCIONES ---
from .suscripciones_models import (
    Invoice, Subscription, SubscriptionStatus,
    PaymentMethod, Currency
)

# --- DRIMSOFT ---
from .drimsoft_models import (
    UserDrimsoft, TicketSupport, TicketStatus,
    RoleDrimsoft, UserStatusDrimsoft
)

# --- PLANIFIKA ---
from .planifika_models import (
    UserPlanifika
)

# --- PROYECTOS ---
from .proyectos_models import (
    Project, Task, Phase, UserRoleProject,
    Methodology, ProjectStatus, TaskStatus,
    RoleProyecto, UserTask, PublicMessage
)

# ======================================================
# EXPORTACIÓN GLOBAL
# ======================================================

__all__ = [
    # Bases
    "BaseDrimsoft", "BasePlanifika", "BaseProyectos", "BaseSuscripciones",

    # Modelos Drimsoft
    "UserDrimsoft", "TicketSupport", "TicketStatus", "RoleDrimsoft", "UserStatusDrimsoft",

    # Modelos Planifika
    "UserPlanifika",

    # Modelos Proyectos
    "Project", "Task", "Phase", "UserRoleProject",
    "Methodology", "ProjectStatus", "TaskStatus",
    "RoleProyecto", "UserTask", "PublicMessage",

    # Modelos Suscripciones
    "Invoice", "Subscription", "SubscriptionStatus",
    "PaymentMethod", "Currency",
]

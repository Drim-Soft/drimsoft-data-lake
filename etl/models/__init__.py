from sqlalchemy.orm import declarative_base

BaseDrimsoft = declarative_base()
BasePlanifika = declarative_base()
BaseProyectos = declarative_base()
BaseSuscripciones = declarative_base()

from .suscripciones_models import (
    Invoice, Subscription, SubscriptionStatus, PaymentMethod, Currency
)

from .drimsoft_models import (
    UserDrimsoft, TicketSupport, TicketStatus, RoleDrimsoft, UserStatusDrimsoft
)

from .planifika_models import UserPlanifika

from .proyectos_models import (
    Project, Task, Phase, UserRoleProject,
    Methodology, ProjectStatus, TaskStatus, RoleProyecto
)

__all__ = [
    "BaseDrimsoft", "BasePlanifika", "BaseProyectos", "BaseSuscripciones",
    "UserDrimsoft", "TicketSupport", "TicketStatus", "RoleDrimsoft", "UserStatusDrimsoft",
    "UserPlanifika",
    "Project", "Task", "Phase", "UserRoleProject",
    "Methodology", "ProjectStatus", "TaskStatus", "RoleProyecto",
    "Invoice", "Subscription", "SubscriptionStatus", "PaymentMethod", "Currency",
]
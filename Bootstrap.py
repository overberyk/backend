# Bootstrap.py
"""
Rutinas que corren al iniciar la aplicación: crear tablas, roles base y
el usuario admin inicial si no existe.
"""

from sqlalchemy.orm import Session

from Config import SessionLocal, engine, adminEmail, adminPassword, hashPassword
from Models.Base import Base
from Models.User import Role, User

BASE_ROLES = ["admin", "seller", "client"]

WEAK_PASSWORDS = {
    "admin1234", "admin123", "password", "12345678",
    "test1234", "changeme", "admin", "123456",
}


def _ensureRoles(db: Session) -> dict[str, Role]:
    roles = {}
    for name in BASE_ROLES:
        role = db.query(Role).filter(Role.name == name).first()
        if role is None:
            role = Role(name=name)
            db.add(role)
            db.commit()
            db.refresh(role)
        roles[name] = role
    return roles


def _ensureAdminUser(db: Session, adminRole: Role) -> None:
    if not adminEmail or not adminPassword:
        print(
            "[bootstrap] ADMIN_EMAIL/ADMIN_PASSWORD no están definidas: "
            "se omite la creación del admin inicial."
        )
        return

    existing = db.query(User).filter(User.email == adminEmail).first()
    if existing is not None:
        print(f"[bootstrap] Usuario admin ya existe ({adminEmail}), no se crea de nuevo.")
        return

    if adminPassword.lower() in WEAK_PASSWORDS or len(adminPassword) < 8:
        print(
            "[bootstrap] ADVERTENCIA: ADMIN_PASSWORD es débil o muy corta. "
            "Se crea igual el usuario (por si estás en desarrollo local), "
            "pero cambiala antes de exponer esto a producción."
        )

    admin = User(
        firstName="Admin",
        lastName="",
        email=adminEmail,
        passwordHash=hashPassword(adminPassword),
        roleId=adminRole.roleId,
    )
    db.add(admin)
    db.commit()
    print(f"[bootstrap] Usuario admin creado: {adminEmail}")


def runBootstrap() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        roles = _ensureRoles(db)
        _ensureAdminUser(db, roles["admin"])
    finally:
        db.close()

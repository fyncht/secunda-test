from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models


def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # 1) Buildings
    b1 = models.Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.7558, longitude=37.6173)
    b2 = models.Building(address="г. Санкт-Петербург, ул. Блюхера 32/1", latitude=59.9343, longitude=30.3351)
    db.add_all([b1, b2])
    db.flush()

    # 2) Activities (дерево, 3 уровня)
    food = models.Activity(name="Еда")
    meat = models.Activity(name="Мясная продукция", parent=food)
    dairy = models.Activity(name="Молочная продукция", parent=food)
    auto = models.Activity(name="Автомобили")
    cargo = models.Activity(name="Грузовые", parent=auto)
    passenger = models.Activity(name="Легковые", parent=auto)
    parts = models.Activity(name="Запчасти", parent=passenger)
    accessories = models.Activity(name="Аксессуары", parent=passenger)
    db.add_all([food, meat, dairy, auto, cargo, passenger, parts, accessories])
    db.flush()

    # 3) Organizations
    org1 = models.Organization(
        name="ООО Рога и Копыта",
        building=b2,
        activities=[dairy, meat],
        phones=[models.Phone(number="2-222-222"), models.Phone(number="3-333-333")]
    )
    org2 = models.Organization(
        name="Завод Молочка",
        building=b1,
        activities=[dairy],
        phones=[models.Phone(number="8-923-666-13-13")]
    )
    org3 = models.Organization(
        name="АвтоМир",
        building=b2,
        activities=[cargo, accessories],
        phones=[models.Phone(number="7-777-777")]
    )
    db.add_all([org1, org2, org3])
    db.commit()
    db.close()
    print("Seed completed")


if __name__ == "__main__":
    seed()

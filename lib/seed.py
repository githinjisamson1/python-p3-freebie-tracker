#!/usr/bin/env python3
from sqlalchemy import create_engine
from models import Company, Dev, Freebie, company_devs as CompanyDevs
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random

fake = Faker()

if __name__ == "__main__":
    engine = create_engine("sqlite:///freebies.db")

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

    for _ in range(10):
        company = Company(name=fake.company(), founding_year=fake.year())
        session.add(company)
        session.commit()

    for _ in range(10):
        dev = Dev(name=fake.unique.name())
        session.add(dev)
        session.commit()

    company_ids = [company.id for company in session.query(Company).all()]
    dev_ids = [dev.id for dev in session.query(Dev).all()]

    for _ in range(10):
        freebie = Freebie(
            item_name=fake.color_name(),
            value=fake.random_int(min=0, max=100),
            dev_id=random.choice(dev_ids),
            company_id=random.choice(company_ids),
        )
        session.add(freebie)
        session.commit()

    # !!! Table is not callable
    # seed company_devs table using already existing IDs
    # for _ in range(10):
    #     company_dev = CompanyDevs(
    #         company_id=random.choice(company_ids), dev_id=random.choice(dev_ids)
    #     )
    #     session.add(company_dev)
    #     session.commit()

    # After creating companies and devs
    # Create relationships between companies and devs
    for _ in range(20):  # Create 20 associations as an example
        company = random.choice(session.query(Company).all())
        dev = random.choice(session.query(Dev).all())

        # Add the developer to the company's devs list
        if dev not in company.devs:  # Avoid duplicate associations
            company.devs.append(dev)
            session.add(company)  # Add the updated company object to the session

        # Commit the relationships
        session.commit()

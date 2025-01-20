from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Table Object
company_devs = Table(
    "company_devs",
    Base.metadata,
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
    Column("dev_id", Integer, ForeignKey("devs.id"), primary_key=True),
    extend_existing=True,
)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", backref=backref("company"))
    devs = relationship("Dev", secondary=company_devs, back_populates="companies")

    # remember we have dev, oompany columns
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(dev=dev, company=self, item_name=item_name, value=value)
        return freebie

    def oldest_company(self):
        return self.founding_year

    # session.query(Company).order_by(asc(Company.founding_year)).first()

    def __repr__(self):
        return f"<Company {self.name}>"


class Dev(Base):
    __tablename__ = "devs"

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship("Freebie", backref=backref("dev"))
    companies = relationship("Company", secondary=company_devs, back_populates="devs")

    def received_one(self, item_name):
        for f in self.freebies:
            if f.item_name == item_name:
                return True
            else:
                return False

    def give_away(self, dev, freebie):
        # Dev.give_away(dev, freebie) accepts a Dev instance and a Freebie instance, changes the freebie's dev to be the given dev; your code should only make the change if the freebie belongs to the dev who's giving it away
        if freebie.dev == self:
            freebie.dev = dev
            return freebie
        else:
            return None

    def __repr__(self):
        return f"<Dev {self.name}>"


class Freebie(Base):
    __tablename__ = "freebies"

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    dev_id = Column(Integer(), ForeignKey("devs.id"))
    company_id = Column(Integer(), ForeignKey("companies.id"))

    def print_details(self):
        print(f"{self.dev.name} owns a {self.item_name} from {self.company.name}")

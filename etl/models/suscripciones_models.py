from sqlalchemy import Column, Integer, String, Date, Numeric
from .bases import BaseSuscripciones

class Currency(BaseSuscripciones):
    __tablename__ = 'currency'
    idcurrency = Column(Integer, primary_key=True)
    name = Column(String)

class Subscription(BaseSuscripciones):
    __tablename__ = 'subscription'
    idsubscription = Column(Integer, primary_key=True)
    name = Column(String)

class SubscriptionStatus(BaseSuscripciones):
    __tablename__ = 'subscriptionstatus'
    idsubscriptionstatus = Column(Integer, primary_key=True)
    name = Column(String)

class PaymentMethod(BaseSuscripciones):
    __tablename__ = 'paymentmethod'
    idpaymentmethod = Column(Integer, primary_key=True)
    name = Column(String)

class Invoice(BaseSuscripciones):
    __tablename__ = 'invoice'
    idinvoice = Column(Integer, primary_key=True)
    idsubscription = Column(Integer)
    idsubscriptionstatus = Column(Integer)
    idpaymentmethod = Column(Integer)
    idcurrency = Column(Integer)
    idorganization = Column(Integer)
    total = Column(Numeric)
    startdate = Column(Date)
    enddate = Column(Date)
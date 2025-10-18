from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class Subscription(Base):
    __tablename__ = 'subscription'
    idsubscription = Column(Integer, primary_key=True)
    name = Column(String)

class SubscriptionStatus(Base):
    __tablename__ = 'subscriptionstatus'
    idsubscriptionstatus = Column(Integer, primary_key=True)
    name = Column(String)

class PaymentMethod(Base):
    __tablename__ = 'paymentmethod'
    idpaymentmethod = Column(Integer, primary_key=True)
    name = Column(String)

class Invoice(Base):
    __tablename__ = 'invoice'
    idinvoice = Column(Integer, primary_key=True, autoincrement=True)
    idsubscription = Column(Integer, ForeignKey('subscription.idsubscription'))
    idsubscriptionstatus = Column(Integer, ForeignKey('subscriptionstatus.idsubscriptionstatus'))

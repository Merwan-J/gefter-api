from ast import List
from dataclasses import dataclass
from uuid import UUID
from injector import inject
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

from api.core.exceptions import NotFoundError
from api.core.repository import DatabaseEngineProvider
from api.invoice_shares.models import InvoiceShare


@inject
@dataclass
class InvoiceShareRepository:
    engine_provider: DatabaseEngineProvider

    def __post_init__(self):
        self.engine: Engine = self.engine_provider.get_engine()

    def get_invoice_share_by_id(self, invoice_share_id: UUID) -> InvoiceShare:
        with Session(self.engine) as session:
            query = select(InvoiceShare).where(InvoiceShare.id == invoice_share_id)
            try:
                return session.exec(query).one()
            except NoResultFound:
                raise NotFoundError("Invoice share not found")

    def get_invoice_shares_by_invoice_id(self, invoice_id: UUID) -> List[InvoiceShare]:
        with Session(self.engine) as session:
            query = select(InvoiceShare).where(InvoiceShare.invoice_id == invoice_id)
            return session.exec(query)

    def get_invoice_shares_by_debtor_id(self, debtor_id: UUID) -> List[InvoiceShare]:
        with Session(self.engine) as session:
            query = select(InvoiceShare).where(InvoiceShare.debtor_id == debtor_id)
            return session.exec(query)

    def get_invoice_shares_by_creditor_id(
        self, creditor_id: UUID
    ) -> List[InvoiceShare]:
        with Session(self.engine) as session:
            query = select(InvoiceShare).where(InvoiceShare.creditor_id == creditor_id)
            return session.exec(query)

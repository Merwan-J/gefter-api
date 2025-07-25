from dataclasses import dataclass
from injector import inject

from api.core.repository import DatabaseEngineProvider
from api.invoice_shares.models import InvoiceShare


@inject
@dataclass
class InvoiceShareRepository:
    engine_provider: DatabaseEngineProvider

    def save(self, invoice_share: InvoiceShare) -> InvoiceShare:
        with self.engine_provider.get_session() as session:
            session.add(invoice_share)
            session.commit()
            session.refresh(invoice_share)
            return invoice_share

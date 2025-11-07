from dataclasses import dataclass
from typing import List
from uuid import UUID
from injector import inject
from api.core.exceptions import BaseAPIException, InternalServerError

from api.invoice_shares.repository import InvoiceShareRepository
from api.invoice_shares.models import InvoiceShare


@inject
@dataclass
class InvoiceShareService:
    invoice_share_repository: InvoiceShareRepository

    def get_invoice_share_by_id(self, invoice_share_id: UUID) -> InvoiceShare:
        try:
            return self.invoice_share_repository.get_invoice_share_by_id(
                invoice_share_id
            )
        except BaseAPIException:
            raise
        except Exception:
            raise InternalServerError("Unable to fetch invoice share")

    def get_invoice_shares_by_invoice_id(self, invoice_id: UUID) -> List[InvoiceShare]:
        try:
            return self.invoice_share_repository.get_invoice_shares_by_invoice_id(
                invoice_id
            )
        except BaseAPIException:
            raise
        except Exception:
            raise InternalServerError("Unable to fetch invoice shares")

    def get_invoice_shares_by_debtor_id(self, debtor_id: UUID) -> List[InvoiceShare]:
        try:
            return self.invoice_share_repository.get_invoice_shares_by_debtor_id(
                debtor_id
            )
        except BaseAPIException:
            raise
        except Exception:
            raise InternalServerError("Unable to fetch invoice shares")

    def get_invoice_shares_by_creditor_id(
        self, creditor_id: UUID
    ) -> List[InvoiceShare]:
        try:
            return self.invoice_share_repository.get_invoice_shares_by_creditor_id(
                creditor_id
            )
        except BaseAPIException:
            raise

    def get_invoice_shares_by_user_id(self, user_id: UUID) -> List[InvoiceShare]:
        try:
            return self.invoice_share_repository.get_invoice_shares_by_user_id(user_id)
        except BaseAPIException:
            raise
        except Exception:
            raise InternalServerError("Unable to fetch invoice shares")

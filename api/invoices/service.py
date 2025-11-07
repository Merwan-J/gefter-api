from dataclasses import dataclass
from typing import List
from uuid import UUID
from injector import inject

from api.core.exceptions import (
    BaseAPIException,
    UnauthorizedError,
    BadRequestError,
    InternalServerError,
)
from api.invoices.models import (
    Invoice,
    InvoiceCreate,
    InvoiceDetailRead,
    InvoiceRead,
)
from api.invoices.repository import InvoiceRepository
from api.invoice_shares.repository import InvoiceShareRepository
from api.invoice_shares.models import InvoiceShareStatus
from api.invoices.models import InvoiceStatus
from api.balances.service import BalanceService


@inject
@dataclass
class InvoiceService:
    invoice_repository: InvoiceRepository
    invoice_share_repository: InvoiceShareRepository
    balance_service: BalanceService

    def create_invoice(self, invoice_create: InvoiceCreate) -> Invoice:
        try:
            if not invoice_create.invoice_shares:
                raise BadRequestError("Invoice must have at least one share")

            # Validate total shares equal invoice amount
            # total_shares = sum(share.amount for share in invoice_create.invoice_shares)
            # if total_shares != invoice_create.amount:
            #     raise BadRequestError(
            #         f"Sum of invoice shares ({total_shares}) must equal invoice amount ({invoice_create.amount})"
            #     )

            try:
                invoice = self.invoice_repository.create_invoice_with_shares(invoice_create)
                
                # Update balances based on invoice shares
                # For each share: increase creator's owed_to_user, and increase debtor's user_owes
                for share in invoice.invoice_shares:
                    self.balance_service.add_to_owed_to_user(share.creditor_id, share.amount)
                    self.balance_service.add_to_user_owes(share.debtor_id, share.amount)
                
            except Exception as e:
                print(f"Unable to create invoice: {e}")
                raise InternalServerError("Unable to create invoice")

            return invoice

        except BaseAPIException:
            raise
        except Exception:
            raise InternalServerError("Unable to create invoice")

    def get_invoice_detail(
        self, invoice_id: UUID, current_user_id: UUID
    ) -> InvoiceDetailRead:
        try:
            invoice = self.invoice_repository.get_invoice_detail(invoice_id)

            is_creator = invoice.creator_id == current_user_id
            is_debtor = any(
                share.debtor_id == current_user_id for share in invoice.invoice_shares
            )

            if not (is_creator or is_debtor):
                raise UnauthorizedError("User not authorized to view the given invoice")

            return InvoiceDetailRead.model_validate(invoice)

        except BaseAPIException:
            raise
        except Exception as e:
            print(f"Unable to fetch invoice details: {e}")
            raise InternalServerError("Unable to fetch invoice details")

    def get_invoices(self, user_id: UUID) -> List[InvoiceRead]:
        try:
            invoices = self.invoice_repository.get_invoices(user_id)
            return [InvoiceRead.model_validate(invoice) for invoice in invoices]
        except BaseAPIException:
            raise
        except Exception as e:
            print(f"Unable to fetch invoices: {e}")
            raise InternalServerError("Unable to fetch invoices")

    def pay_invoice_share(self, invoice_id: UUID, invoice_share_id: UUID) -> InvoiceDetailRead:
        try:
            self.invoice_share_repository.set_status_paid(invoice_share_id)

            remaining = self.invoice_share_repository.count_unpaid_shares(invoice_id)

            if remaining == 0:
                self.invoice_repository.update_invoice_status(invoice_id, InvoiceStatus.PAID)
            else:
                self.invoice_repository.update_invoice_status(invoice_id, InvoiceStatus.PARTIALLY_PAID)

            invoice = self.invoice_repository.get_invoice_detail(invoice_id)

            return InvoiceDetailRead.model_validate(invoice)

        except BaseAPIException:
            raise
        except Exception as e:
            print(f"Unable to pay invoice share: {e}")
            raise InternalServerError("Unable to pay invoice share")

    def get_invoice_detail(self, invoice_id: UUID) -> InvoiceDetailRead:
        try:
            invoice = self.invoice_repository.get_invoice_detail(invoice_id)
            return InvoiceDetailRead.model_validate(invoice)

        except Exception as e:
            print(f"Unable to get invoice by id: {e}")
            raise InternalServerError("Unable to get invoice by id")

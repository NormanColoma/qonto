from application.application_command import ApplicationCommand


class ProcessTransfersCommand(ApplicationCommand):
    def __init__(self, organization_iban: str, credit_transfers: [dict]):
        self.organization_iban = organization_iban
        self.credit_transfers = credit_transfers

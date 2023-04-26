from app.models.audit import Audit


class AuditController:

    @staticmethod
    def add(audit_data):
        # Log an action in the audit trail
        return Audit.add(audit_data)

    @staticmethod
    def get_audit_trail():
        # Get the full audit trail
        return Audit.get_all()

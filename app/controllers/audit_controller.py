from models.audit import Audit


class AuditController:

    @staticmethod
    def add(audit_data):
        # Log an action in the audit trail
        return Audit.add(audit_data)

    @staticmethod
    def get_records():
        # Get the full audit trail
        return Audit.get_all()

    @staticmethod
    def add_audit_listener(callback):
        # Create a listener for audit trail updates
        return Audit.add_audit_listener(callback)

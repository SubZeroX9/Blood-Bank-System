from app.models.record_copy import RecordCopy
from app.utils.pdf_exporter import export_record_copy_to_pdf


class RecordCopyController:

    @staticmethod
    def create_record_copy(record_copy_data):
        # Add the record copy to the database
        record_copy_id = RecordCopy.add(record_copy_data)

        # Export the record copy to a PDF file
        export_record_copy_to_pdf(record_copy_id, record_copy_data)

        return record_copy_id

    @staticmethod
    def get_record_copy_by_id(record_copy_id):
        # Get record copy by ID from the database
        return RecordCopy.get_by_id(record_copy_id)

    @staticmethod
    def get_all_record_copies():
        # Get all record copies from the database
        return RecordCopy.get_all()

    @staticmethod
    def update_record_copy(record_copy_id, record_copy_data):
        # Update the record copy in the database
        RecordCopy.update(record_copy_id, record_copy_data)

        # Update the exported PDF file
        export_record_copy_to_pdf(record_copy_id, record_copy_data)

        return record_copy_id

    @staticmethod
    def delete_record_copy(record_copy_id):
        # Delete the record copy from the database
        RecordCopy.delete(record_copy_id)

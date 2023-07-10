import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from ..donor import Donor
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from firebase.firebase_config import db


class DocumentReferenceMock:
    def __init__(self, id='123456789'):
        self.id = id

    def update(self, data):
        pass

    def delete(self):
        pass

    def collection(self, collection_path):
        return CollectionReferenceMock()

class CollectionReferenceMock:
    def __init__(self):
        self.document_mock = DocumentReferenceMock()

    def add(self, document_data):
        return (self.document_mock, {})

    def document(self, doc_id=None):
        if doc_id is None:
            return self.document_mock
        else:
            return DocumentReferenceMock(doc_id)

    def where(self, field_path, op_string, value):
        return QuerySnapshotMock()

    def stream(self):
        return iter([QueryDocumentSnapshotMock()])

class QueryDocumentSnapshotMock:
    def __init__(self):
        self.exists = True
        self.id = '123456789'

    def to_dict(self):
        return {}

    def get(self):
        return self.to_dict()

    @property
    def reference(self):
        return DocumentReferenceMock()

class QuerySnapshotMock:
    def __init__(self):
        pass

    def stream(self):
        return iter([QueryDocumentSnapshotMock()])

class FirestoreMock:
    def __init__(self):
        self.collection_mock = CollectionReferenceMock()

    def collection(self, collection_path):
        return self.collection_mock

mock_db = FirestoreMock()

@patch('firebase.firebase_config.db')
def test_add(mock_db):
    doc_ref_mock = MagicMock()
    type(doc_ref_mock).id = PropertyMock()
    mock_db.collection.return_value.add.return_value = [MagicMock(), doc_ref_mock]

    donor = {'name': 'John Doe', 'age': 30, 'blood_type': 'O+'}
    result = Donor.add(donor)
    assert result is not None, "Expected an ID, but got None"


@patch('firebase.firebase_config.batch', new_callable=MagicMock)
@patch('firebase.firebase_config.db')
def test_add_new_donor_history(mock_db, mock_batch):
    mock_db.collection().document.return_value = MagicMock()
    donor = {'name': 'John Doe', 'age': 30, 'blood_type': 'O+'}
    donor_history = {'last_donation': '2023-01-01', 'illness_history': 'none'}
    Donor.add_new_donor_history(donor, donor_history)
    #check count (2)
    assert mock_batch.set.call_count == 0

@patch('firebase.firebase_config.db')
def test_is_donor_reg(mock_db):
    mock_db.collection.return_value.where.return_value.stream.return_value = [MagicMock()]
    result = Donor.is_donor_reg('123456789')
    assert result is True, "Expected True, but got False"

@patch('firebase.firebase_config.db')
def test_get_all(mock_db):
    mock_db.collection.return_value.stream.return_value = [MagicMock()]
    result = Donor.get_all()
    assert isinstance(result, dict), "Expected a dictionary, but got {}".format(type(result))

@patch('firebase.firebase_config.db')
def test_get_donations_quantity(mock_db):
    mock_stream = MagicMock()
    mock_stream.reference.get.return_value.to_dict.return_value = {"num_of_dons": 2}
    mock_db.collection.return_value.where.return_value.stream.return_value = [mock_stream]
    result = Donor.get_donations_quantity('123456789')
    assert result == 2, "Expected 2, but got {}".format(result)

@patch('firebase.firebase_config.batch', new_callable=MagicMock)
@patch('firebase.firebase_config.db')
def test_update_donor_history(mock_db, mock_batch):
    mock_db.collection().document().get.return_value = MagicMock(exists=True)
    mock_db.collection().where().stream.return_value = iter([MagicMock()])
    donor_history = {'last_donation': '2023-01-01', 'illness_history': 'none'}
    Donor.update_donor_history('123456789', donor_history)
    #check count (2)
    assert mock_batch.set.call_count == 0

@patch('firebase.firebase_config.db')
def test_delete(mock_db):
    mock_db.collection.return_value.document.return_value.delete.return_value = None
    result = Donor.delete('123456789')
    assert result == '123456789', "Expected '123456789', but got {}".format(result)
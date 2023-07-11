import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from ..audit import Audit
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from firebase.firebase_config import db

class DocumentReferenceMock:
    def __init__(self, id='123456789'):
        self.id = id
        self._document_path = f"projects/projectId/databases/(default)/documents/collectionId/{id}"
        self.last_set_data = None

    def update(self, data):
        pass

    def delete(self):
        pass

    def set(self, data):
        self.last_set_data = data

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

    def on_snapshot(self, callback):
        pass

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


@patch('firebase.firebase_config.db.collection', return_value=CollectionReferenceMock())
def test_add(mock_collection):
    audit_data = {'action': 'test action', 'timestamp': '2021-09-30T00:00:00Z'}
    Audit.add(audit_data)
    assert mock_collection.called

@patch('firebase.firebase_config.db.collection', return_value=CollectionReferenceMock())
def test_get_all(mock_collection):
    result = Audit.get_all()
    assert mock_collection.called
    assert isinstance(result, dict)

@patch('firebase.firebase_config.db.collection', return_value=CollectionReferenceMock())
def test_add_audit_listener(mock_collection):
    callback = MagicMock()
    Audit.add_audit_listener(callback)
    assert mock_collection.called

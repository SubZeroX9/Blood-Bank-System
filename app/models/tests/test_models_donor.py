import pytest
from models.donor import Donor
from unittest.mock import Mock, patch
from firebase.firebase_config import db


@pytest.fixture
def mock_db():
    with patch.object(db, 'collection') as mock_collection:
        yield mock_collection


def test_add(mock_db):
    donor = {'name': 'John Doe', 'age': 30, 'blood_type': 'O+'}
    mock_doc_ref = Mock()
    mock_doc_ref.__getitem__.return_value = '12345'
    mock_db.return_value.add.return_value = mock_doc_ref
    donor_id = Donor.add(donor)
    mock_db.assert_called_once_with('donors')
    mock_db.return_value.add.assert_called_once_with(donor)
    assert donor_id == '12345'


def test_add_new_donor_history(mock_db):
    donor = {'name': 'John Doe', 'age': 30, 'blood_type': 'O+'}
    donor_history = {'last_donation_date': '2021-01-01', 'donation_count': 1}
    mock_doc_ref = Mock()
    mock_db.return_value.document.return_value = mock_doc_ref
    Donor.add_new_donor_history(donor, donor_history)
    mock_db.assert_called_once_with('donors')
    mock_db.return_value.document.assert_called_once_with()
    mock_batch = mock_db.return_value.batch.return_value
    mock_batch.set.assert_any_call(mock_doc_ref, donor)
    mock_batch.set.assert_any_call(mock_doc_ref.collection(
        'medical_history').document(), donor_history)
    mock_batch.commit.assert_called_once_with()


def test_is_donor_reg(mock_db):
    donor_id = '12345'
    mock_doc_ref = Mock()
    mock_doc_ref.exists.return_value = True
    mock_db.return_value.where.return_value.stream.return_value = [
        mock_doc_ref]
    assert Donor.is_donor_reg(donor_id)
    mock_db.assert_called_once_with('donors')
    mock_db.return_value.where.assert_called_once_with(
        field_path='id', op_string='==', value=donor_id)
    mock_doc_ref.exists.assert_called_once_with()


def test_get_all(mock_db):
    mock_doc1 = Mock()
    mock_doc1.id = '12345'
    mock_doc1.to_dict.return_value = {
        'name': 'John Doe', 'age': 30, 'blood_type': 'O+'}
    mock_doc2 = Mock()
    mock_doc2.id = '67890'
    mock_doc2.to_dict.return_value = {
        'name': 'Jane Doe', 'age': 25, 'blood_type': 'A+'}
    mock_db.return_value.stream.return_value = [mock_doc1, mock_doc2]
    donors = Donor.get_all()
    mock_db.assert_called_once_with('donors')
    assert donors == {'12345': {'name': 'John Doe', 'age': 30, 'blood_type': 'O+'},
                      '67890': {'name': 'Jane Doe', 'age': 25, 'blood_type': 'A+'}}


def test_update(mock_db):
    donor_id = '12345'
    donor_data = {'name': 'John Doe', 'age': 30, 'blood_type': 'O+'}
    mock_doc_ref = Mock()
    mock_db.return_value.document.return_value = mock_doc_ref
    Donor.update(donor_id, donor_data)
    mock_db.assert_called_once_with('donors')
    mock_db.return_value.document.assert_called_once_with(donor_id)
    mock_doc_ref.update.assert_called_once_with(donor_data)

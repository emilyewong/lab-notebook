from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import LabNote, LabResult

# Create your tests here.
def create_lab_note(title, date, body):
    # Create a lab note with the given values
    return LabNote.objects.create(note_title=title, note_date=date, note_body=body)
    
class LabNoteIndexViewTests(TestCase):
    def test_no_lab_notes(self):
        #The index page shows no lab records
        url = reverse('lab_notebook:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['note_list'], [])
    
    def test_two_lab_notes(self):
        #The index page shows two lab records
        create_lab_note(title="Test note1", date="2017-06-25", body="This is a test")
        create_lab_note(title="Test note2", date="2017-06-26", body="This is a test")
        url = reverse('lab_notebook:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(
            response.context['note_list'],
            ['<LabNote: Test note1>', '<LabNote: Test note2>']
        )
        
class LabNoteDetailViewTests(TestCase):
    def test_no_lab_note(self):
        #Returns a 404 not found if lab note not found
        url = reverse('lab_notebook:detail', args=[99])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_lab_note(self):
        #Shows selected note
        note = create_lab_note(title="Test note", date="2017-07-25", body="This is a note")
        url = reverse('lab_notebook:detail', args=[note.id])
        response = self.client.get(url)
        self.assertContains(response, note.note_title)

class LabNoteRecordViewTests(TestCase):
    def test_record_form(self):
        #Shows new record form
        url = reverse('lab_notebook:record')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

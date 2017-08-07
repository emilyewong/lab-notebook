from django.shortcuts import get_object_or_404, render

from .models import LabNote, LabResult

# Create your views here.
def index(request):
    # get all notes in db ordered by date
    note_list = LabNote.objects.order_by('note_date')
    # create data package and pass to index page for rendering
    context = {'note_list': note_list}
    return render(request, 'lab_notebook/index.html', context)
    
def detail(request, lab_note_id):
    # get note details based on primary key, or 404 error if not found
    note = get_object_or_404(LabNote, pk=lab_note_id)
    # get all standard sample results related to the note
    results = LabResult.objects.filter(note_id=lab_note_id, standard=1)
    # create data array for Google Charts
    chartData = [['Concentration', 'Absorbance']]
    for item in results:
        # convert strings to floats
        chartData.append([float(item.concentration), float(item.absorbance)])
    # create data package and pass to detail page for rendering
    context = {'note': note, 'chartData': chartData}
    return render(request, 'lab_notebook/detail.html', context)
    
def record(request):
    # render new record form
    return render(request, 'lab_notebook/record.html')
    
def save(request):
    # handle save of new record if POST
    if request.method == 'POST':
        try:
            # grab input values (ideally these would be sanitized)
            title = request.POST.get('title')
            date = request.POST.get('date')
            body = request.POST.get('body')
    
            # create array of sample values
            sample_values = []
            for i in range(1,6):
                concId = 'concentration-' + str(i);
                absId = 'absorbance-' + str(i);
                sample_values.append([request.POST.get(concId), request.POST.get(absId)])
            
            sample_values.append([request.POST.get('concentration-unknown'), request.POST.get('absorbance-unknown')])
    
            # create new LabNote entry and save
            new_note = LabNote(
                note_title=title,
                note_date=date,
                note_body=body)
            new_note.save()
            
            # create new LabResult entry for standard samples and save
            i = 0
            while i < len(sample_values) - 1:
                new_result = LabResult(concentration=sample_values[i][0], absorbance=sample_values[i][1], standard=1, note_id=new_note)
                new_result.save()
                i+=1
                
            # create new LabResult entry for unknown sample and save
            j = len(sample_values) - 1
            new_result_unknown = LabResult(concentration=sample_values[j][0], absorbance=sample_values[j][1], standard=0, note_id=new_note)
            new_result_unknown.save()
            
            # display details page after save complete
            results = LabResult.objects.filter(note_id=new_note, standard=1)
            chartData = [['Concentration', 'Absorbance']]
            for item in results:
                chartData.append([float(item.concentration), float(item.absorbance)])
            context = {'note': new_note, 'chartData': chartData}
            return render(request, 'lab_notebook/detail.html', context)
        except:
            # go to index page if error occurs
            note_list = LabNote.objects.order_by('note_date')
            context = {'note_list': note_list}
            return render(request, 'lab_notebook/index.html', context)
    else:
        # show index page if not POST
        note_list = LabNote.objects.order_by('note_date')
        context = {'note_list': note_list}
        return render(request, 'lab_notebook/index.html', context)
    

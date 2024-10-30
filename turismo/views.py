from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import AnimaisForm, Animais, IdentificarForm, Identificar
from .detector import ObjectDetector
import os
from django.core.files.storage import FileSystemStorage
# Create your views here.

def index(request):
	template = loader.get_template('turismo/index.html')
	return HttpResponse( template.render({}, request) )

def listar(request):
    animais = Animais.objects.all().order_by('nomeCientifico');
    template = loader.get_template('turismo/listar.html')
    return HttpResponse(template.render({'animais':animais}, request))

def cadastrar(request):
    if request.POST:
        form = AnimaisForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('Salvo com sucesso!')
            return redirect('index')
        else:
            return redirect('cadastrar')
    else:
        template = loader.get_template('turismo/inserir.html')
        context = {
            'form': AnimaisForm(),
        }
        return HttpResponse(template.render(context, request))
    
def identificar(request):
    if request.method == 'POST' and request.FILES.get('image'):
        imageGet           = request.FILES['image']
        fs                 = FileSystemStorage()
        local              = os.path.join(fs.location,'test.png')
        if os.path.exists(local):
            os.remove(local)
            
        filename           = fs.save('test.png', imageGet)
        uploaded_image_url = fs.url(filename)
        input_image_path   = os.path.join(fs.location, filename)

        detector    = ObjectDetector()
        results     = detector.predict(input_image_path)
        detector.draw_boxes(input_image_path, results)

        output_image_url = fs.url(filename)
        # Renderizar a página com os URLs das imagens
        response =  render(request, 'turismo/identificacao.html', {'uploaded_image_url': output_image_url})
        #os.remove(input_image_path)

        return response
    
    else:
        return render(request, 'turismo/identificacao.html', {'uploaded_image_url': None})
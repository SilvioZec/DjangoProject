from django.shortcuts import render, redirect
from .models import Student, School
from .forms import StudentForm
from django.http import HttpResponse
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def profile(request):
    if request.user.is_staff:
        return redirect('/admin/')
    if not request.user.is_authenticated:
        return redirect('account_login')  # redirecionar para a página de login
    
    #excluir registo
    if request.method == 'POST' and 'delete_student_id' in request.POST:
        student_id = request.POST.get('delete_student_id')
        # Lógica para excluir o aluno com o id fornecido
        Student.objects.filter(id=student_id).delete()
        messages.success(request, 'Aluno excluído com sucesso.')

    current_user = request.user
    students = Student.objects.filter(user=current_user)
    context = {
        'students': students,
    }
    return render(request, 'profile.html', context)  # enviar dados dos alunos aqui

def register_student_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Obter as informações preenchidas no formulário
            student = form.save(commit=False)
            
            # Setup do Geopy
            geolocator = Nominatim(user_agent="my_geocoder")
            
            # Obter as coordenadas geográficas do aluno
            end1 = f"{student.address}. {student.postal} {student.city}, {student.country}"
            location1 = geolocator.geocode(end1, timeout=10)
            
            if location1 is None:
                messages.error(request, f"Invalid address: {end1}")
                return render(request, 'register_student.html', {'form': form})
            
            coordenadas1 = (location1.latitude, location1.longitude)
            
            # Obter as informações da escola selecionada pelo usuário
            school_id = form.cleaned_data['school'].id
            selected_school = School.objects.get(pk=school_id)

            end2 = f"{selected_school.address}. {selected_school.postal} {selected_school.city}, {selected_school.country}"
            location2 = geolocator.geocode(end2, timeout=10)
            
            if location2 is None:
                messages.error(request, f"Invalid address: {end2}")
                return render(request, 'register_student.html', {'form': form})
            
            coordenadas2 = (location2.latitude, location2.longitude)
            
            
            # Calcular a distância entre os dois endereços
            distancia = geodesic(coordenadas1, coordenadas2).kilometers
            student.distance = distancia

            student.user_id = request.user.id  # Preenchendo user_id com o ID do usuário em sessão
            
            student.save()  # Salvar o objeto do aluno com a distância calculada
            
            messages.error(request, f"Student successfully registered")
            return render(request, 'register_student.html', {'form': form})
    else:
        form = StudentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'register_student.html', context)


@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'POST':
        Student.objects.filter(id=student_id).delete()
        return JsonResponse({'message': 'Register deleted'})
    
@login_required
def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
             # Obter as informações preenchidas no formulário
            student = form.save(commit=False)
            
            # Setup do Geopy
            geolocator = Nominatim(user_agent="my_geocoder")
            
            # Obter as coordenadas geográficas do aluno
            end1 = f"{student.address}. {student.postal} {student.city}, {student.country}"
            location1 = geolocator.geocode(end1, timeout=10)
            
            if location1 is None:
                messages.error(request, f"Invalid address: {end1}")
                return render(request, 'edit_student.html', {'form': form})
            
            coordenadas1 = (location1.latitude, location1.longitude)
            
            # Obter as informações da escola selecionada pelo usuário
            school_id = form.cleaned_data['school'].id
            selected_school = School.objects.get(pk=school_id)

            end2 = f"{selected_school.address}. {selected_school.postal} {selected_school.city}, {selected_school.country}"
            location2 = geolocator.geocode(end2, timeout=10)
            
            if location2 is None:
                messages.error(request, f"Invalid address: {end2}")
                return render(request, 'edit_student.html', {'form': form})
            
            coordenadas2 = (location2.latitude, location2.longitude)
            
            
            # Calcular a distância entre os dois endereços
            distancia = geodesic(coordenadas1, coordenadas2).kilometers
            student.distance = distancia

            student.user_id = request.user.id  # Preenchendo user_id com o ID do usuário em sessão
            
            student.save()  # Salvar o objeto do aluno com a distância calculada
            
            form.save()
            messages.success(request, 'Student information updated successfully.')
            return redirect('profile')
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student_id': student_id
    }
    return render(request, 'edit_student.html', context)
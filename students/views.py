from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student
from .forms import RegisterForm, StudentForm

# Регистрация (без изменений)
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data['password']
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'students/register.html', {'form': form})

# ГЛАВНАЯ СТРАНИЦА: Теперь это список уникальных групп
@login_required
def student_list(request):
    # Получаем список уникальных названий групп, исключая пустые значения
    groups = Student.objects.exclude(group__isnull=True).exclude(group__exact='').values_list('group', flat=True).distinct()
    return render(request, "students/index.html", {"groups": groups})

# ДОБАВЛЕНИЕ: После сохранения кидаем сразу в папку группы
@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Создаем объект, но не сохраняем в базу сразу
            student = form.save(commit=False)
            
            # 2. Очищаем название группы от лишних пробелов
            if student.group:
                student.group = student.group.strip()
            
            # 3. Сохраняем уже чистый объект
            student.save()
            
            # 4. Редирект в группу
            return redirect('group_detail', group_name=student.group)
    else:
        form = StudentForm()
    
    return render(request, 'students/add_student.html', {'form': form})

@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            # Повторяем логику очистки для редактирования
            updated_student = form.save(commit=False)
            if updated_student.group:
                updated_student.group = updated_student.group.strip()
            updated_student.save()
            
            return redirect('group_detail', group_name=updated_student.group)
    else:
        form = StudentForm(instance=student)
        
    return render(request, "students/edit_student.html", {"student": student, "form": form})
# УДАЛЕНИЕ: После удаления студента логичнее вернуться в его группу, а не на главную
@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    group_name = student.group
    student.delete()
    if group_name:
        return redirect('group_detail', group_name=group_name)
    return redirect("student_list")

# ДЕТАЛИ (без изменений)
@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "students/detail.html", {"student": student})

# ГРУППА: Показывает студентов конкретной группы
@login_required
def group_detail(request, group_name):
    students = Student.objects.filter(group=group_name)
    return render(request, "students/group_detail.html", {
        "group_name": group_name,
        "students": students
    })
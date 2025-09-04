from django.shortcuts import render, redirect
from .models import Newregester, Teacher , Student , Class , Event , Role ,Permission, RolePermission
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import  render, get_object_or_404, redirect
from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

def handler404(request, exception):
    return render(request, '404.html', status=404)

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.session.get('role') != role:
                return redirect('login')  # or show 403 if you prefer
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def user_logout(request):
    logout(request)
    return redirect('login')



# Create your views here.
def home(request):
    return render(request, 'home.html')

def loginpage(request):
    return render(request, 'login.html')

def registerpage(request):
    return render(request, 'register.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def teacher(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher.html', {'teachers': teachers})

def student(request):
    students = Student.objects.all()
    return render(request, 'student.html', {'student': students})

def classes(request):
    classes = Class.objects.all()
    return render(request, 'classes.html', {'classes': classes})

def events(request):
    all_events = Event.objects.all()
    return render(request, 'events.html', {'events': all_events})

def settings_page(request):
    return render(request, 'settings.html')

@role_required('student')
def student_dashboard(request):
    return render(request, 'student_dashboard.html', {'role': 'student'})

@role_required('teacher')
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html', {'role': 'teacher'})

@role_required('parent')
def parent_dashboard(request):
    return render(request, 'parent_dashboard.html', {'role': 'parent'})

@role_required('admin')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', {'role': 'admin'})

@role_required('admin')
def teacher_list(request):
    # later, fetch teacher records from your model
    return render(request, 'teacher.html')

@role_required('admin')
def add_teacher(request):
    if request.method == 'POST':
        # handle teacher creation logic here
        pass
    return render(request, 'add_teacher.html')

@role_required('admin')
def edit_teacher(request, id):
    # handle update logic
    return render(request, 'edit_teacher.html')

@role_required('admin')
def delete_teacher(request, id):
    # handle deletion logic
    return redirect('teacher')

@role_required('admin')
def student_list(request):
    # later, fetch student records from your model
    return render(request, 'student.html')

@role_required('admin')
def add_student(request):
    if request.method == 'POST':
        # handle student creation logic here
        pass
    return render(request, 'add_student.html')

@role_required('admin')
def edit_student(request, id):
    # handle update logic
    return render(request, 'edit_student.html')

@role_required('admin')
def delete_student(request, id):
    # handle deletion logic
    return redirect('students')

def permission_list(request):
    permissions = Permission.objects.all()
    roles  = Role.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        slug = request.POST.get("slug")
        status = request.POST.get("status") == "1"
        permission = Permission.objects.create(name=name, slug=slug, status=status)

        
        for role in roles:
            RolePermission.objects.create(
                role=role,              # assuming FK field is "role"
                permission=permission,  # assuming FK field is "permission"
                status=True             # default status for new assignment
            )


        return redirect('permission_list')
    return render(request, 'permission.html', {"permissions": permissions})

def edit_permission(request, permission_id):
    permission = get_object_or_404(Permission, id=permission_id)
    if request.method == "POST":
        permission.name = request.POST.get("name")
        permission.slug = request.POST.get("slug")
        permission.status = request.POST.get("status") == "1"
        permission.save()
        return redirect('permission_list')
    return render(request, 'edit_permission.html', {"permission": permission})

def delete_permission(request, permission_id):
    permission = get_object_or_404(Permission, id=permission_id)
    permission.delete()
    return redirect('permission_list')
def role_list(request):
    roles = Role.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        slug = request.POST.get("slug")
        status = request.POST.get("status") == "1"
        Role.objects.create(name=name, slug=slug, status=status)
        return redirect('role_list')
    return render(request, 'role.html', {"roles": roles})

def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == "POST":
        role.name = request.POST.get("name")
        role.slug = request.POST.get("slug")
        role.status = request.POST.get("status") == "1"
        role.save()
        return redirect('role_list')
    return render(request, 'edit_role.html', {"role": role})

def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    role.delete()
    return redirect('role_list')

def rolepermission_list(request):
    roles = Role.objects.all()
    permission = Permission.objects.all()
    rolepermission = RolePermission.objects.all()
    if request.method == "POST":
        role_id = request.POST.get("role_id")
        permission_id = request.POST.get("permission_id")
        status = "1"
        Role.objects.create(role_id=role_id, permission_id=permission_id, status=status)
        return redirect('rolepermission_list')
    return render(request, 'rolepermission.html', {"roles": roles,"permission" : permission,"rolepermission" : rolepermission})

def edit_rolepermission(request, rolepermission_id):
    rolepermission = get_object_or_404(RolePermission, id=rolepermission_id)
    if request.method == "POST":
        rolepermission.name = request.POST.get("name")
        rolepermission.permission_id = request.POST.get("permission_id")
        rolepermission.status = request.POST.get("status") == "1"
        rolepermission.save()
        return redirect('role_permission_list')

    roles = Role.objects.all()
    permissions = Permission.objects.all()
    return render(request, 'edit_rolepermission.html', {
        "rolepermission": rolepermission,
        "roles": roles,
        "permissions": permissions
    })


def delete_rolepermission(request, rolepermission_id):
    rolepermission = RolePermission.objects.filter(id=rolepermission_id).first()
    if rolepermission:
        rolepermission.delete()
    return redirect('role_permission_list')
def newregister(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        first_name = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        # Make sure 'role' exists in your model or remove this field
        Newregester.objects.create(
            user_name=user_name,
            first_name=first_name,
            email=email,
            password=make_password(password),  # hash password
            role=role
        )
        return redirect('login')  # redirect after registration
    return render(request, 'register.html')


def add_teacher(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        Teacher.objects.create(name=name, email=email, subject=subject)
    return redirect('teacher')

def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        teacher.name = request.POST['name']
        teacher.email = request.POST['email']
        teacher.subject = request.POST['subject']
        teacher.save()
    return redirect('teacher')

def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher')
    teachers = Teacher.objects.all()
    return render(request, 'teacher.html', {'teachers': teachers})


def add_student(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        regnum = request.POST['regnum']
        sec = request.POST['sec']
        # Create student
        Student.objects.create(name=name, email=email, regnum=regnum, sec=sec)
        return redirect('students')
    students = Student.objects.all()
    return render(request, 'student.html', {'students': students})

def edit_student(request, id):
    student = get_object_or_404(student, id=id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.subject = request.POST['subject']
        student.save()
    return redirect('students')

def delete_student(request, id):
    student = get_object_or_404(student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('students')
    students = Student.objects.all()
    return render(request, 'student.html', {'student': students})

def add_class(request):
    if request.method == "POST":
        name = request.POST['name']
        section = request.POST['section']
        class_teacher = request.POST['class_teacher']
        room_number = request.POST['room_number']
        Class.objects.create(
            name=name,
            section=section,
            class_teacher=class_teacher,
            room_number=room_number
        )
    return redirect('classes')

def edit_class(request, id):
    class_obj = get_object_or_404(Class, id=id)
    if request.method == "POST":
        class_obj.name = request.POST['name']
        class_obj.section = request.POST['section']
        class_obj.class_teacher = request.POST['class_teacher']
        class_obj.room_number = request.POST['room_number']
        class_obj.save()
    return redirect('classes')

def delete_class(request, id):
    class_obj = get_object_or_404(Class, id=id)
    if request.method == "POST":
        class_obj.delete()
    return redirect('classes')

def add_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        description = request.POST.get('description')
        Event.objects.create(name=name, date=date, location=location, description=description)
        return redirect('events')
    return redirect('events')

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.date = request.POST.get('date')
        event.location = request.POST.get('location')
        event.description = request.POST.get('description')
        event.save()
        return redirect('events')
    return redirect('events')

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
    return redirect('events')

def checklogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = Newregester.objects.filter(user_name=username).first()
        if user and check_password(password, user.password):

            request.session['user_id'] = user.id
            request.session['username'] = user.user_name
            request.session['role'] = user.role

            # role-based redirect
            role_redirects = {
                'student': 'student_dashboard',
                'teacher': 'teacher_dashboard',
                'parent': 'parent_dashboard',
                'admin': 'admin_dashboard'
            }
            return redirect(role_redirects.get(user.role, 'dashboard.html'))
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

from datetime import timezone

from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.dateparse import parse_datetime

from .models import *
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'home.html')
# Create your views here.

def loginn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, "Email is not registered")
            return render(request, 'login.html')
        em = user.email
        if not em.endswith('@gmail.com'):
            messages.warning(request, "Only Students can login.")
            return redirect('login')

        user = authenticate(request, username=user.username, password=password)
        if user:
            login(request, user)
            return redirect('studentpage')

        messages.warning(request, "Invalid email or password")
    return render(request, 'login.html')

def loginAdmin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, "Email is not registered")
            return render(request, 'loginAdmin.html')
        em=user.email
        if not em.endswith('@admin.com') :
            messages.warning(request, "Only Admins can login.")
            return redirect('loginadmin')

        user = authenticate(request, username=user.username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')

        messages.warning(request, "Invalid email or password")

    return render(request, 'loginAdmin.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        rollno = request.POST.get('rollno')
        number = request.POST.get('number')
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        user=User.objects.filter(username=username)

        if user.exists():
            messages.warning(request,"!User Already Exists")
            return redirect('register')
        if not email.endswith('@gmail.com') :
            messages.warning(request, "Only Students Can Register Here.")
            return redirect('register')

        if password!=rpassword:
            messages.warning(request,"Password does not match")
            return redirect('register')
        user_obj = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user_obj.save()
        profile = Profile.objects.create(
            user=user_obj,
            firstname = firstname,
            lastname = lastname,
            rollno=rollno,
            number = number,
        );
        profile.save()
        messages.success(request,"User created successfully")
        return redirect('register')
    return render(request, 'register.html')

def registerAdmin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')
        user=User.objects.filter(username=username)

        if user.exists():
            messages.warning(request,"!User Already Exists")
            return redirect('registeradmin')
        if not email.endswith('@admin.com'):
            messages.warning(request, "Only Admins can register Here.")
            return redirect('register')

        if password!=rpassword:
            messages.warning(request,"Password does not match")
            return redirect('registeradmin')
        user_obj=User.objects.create_user(username=username,email=email,password=password)
        user_obj.save()
        profile = Profile.objects.create(
            user=user_obj
        );
        profile.save()
        messages.success(request,"User created successfully")
        return redirect('loginadmin')
    return render(request, 'registeradmin.html')

def homee(request):
    return render(request, 'home.html')

def selectType(request):
    data = NewStudent.objects.all()
    return render(request, 'selectType.html', {'data': data})

def base(request):
    return render(request, 'base.html')

def studentm(request):
    data=NewStudent.objects.all()
    return render(request, 'studentm.html',{'data':data})

def newStudent(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        rollno = request.POST.get('rollno')
        course = request.POST.get('course')

        NewStudent.objects.create(fullname=fullname,rollno=rollno,course=course)
        messages.success(request,"Student created successfully")
        return redirect('studentm')
    return redirect('studentm')

def delete(request, id):
    student = NewStudent.objects.get(rollno=id)
    student.delete()
    return redirect('studentm')

def edit(request, id):
    student = NewStudent.objects.get(rollno=id)
    return render(request, 'edit.html',{'student':student})

def update(request, id):
    nname = request.POST.get('fullname')
    nrollno = request.POST.get('rollno')
    ncourse = request.POST.get('course')
    student=NewStudent.objects.get(rollno=id)
    student.fullname=nname
    student.rollno=nrollno
    student.course=ncourse
    student.save()
    return redirect('/studentm')
def studenttm(request):
    query = request.GET.get('search')
    data = []

    if query:
        query = query.strip()
        data = NewStudent.objects.filter(fullname__iexact=query)  # case-insensitive exact match
    return render(request, 'studentm.html', {'data': data, 'query': query})

def dashboard_view(request):
    student_count = NewStudent.objects.count()
    context = {
        'student_count': student_count,

    }

    return render(request, 'base.html', context)

def results(request):
    data = NewStudent.objects.all()
    return render(request, 'results.html', {'data': data})

def studentpage(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'studentPage.html', {'user':request.user, 'profile': profile})

def studentProfile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'studentProfile.html', {'profile': profile})

def update_marks(request, student_id):
    student = get_object_or_404(NewStudent, rollno=student_id)

    if request.method == "POST":
        subject = request.POST.get("subject")
        marks = request.POST.get("marks")

        _, created = StudentMarks.objects.update_or_create(
            student=student,
            subject=subject,
            defaults={"marks": marks}
        )

        messages.success(request, "Marks added." if created else "Marks updated.")
        return redirect("view_marks", student_id=student.rollno)

    return render(request, "resultedit.html", {"student": student})

def view_marks(request, student_id):
    student = get_object_or_404(NewStudent, rollno=student_id)  # or use 'id' if you're using ID
    marks = StudentMarks.objects.filter(student=student)
    total_marks = sum(mark.marks for mark in marks)
    subject_count = marks.count()

    average = total_marks / subject_count if subject_count > 0 else 0

    failed_any = any(mark.marks < 35 for mark in marks)
    status = "Fail" if failed_any else "Pass"
    if status == "Fail":
        grade = "F"
    elif average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "E"

    return render(request, 'view_marks.html', {'student': student, 'marks': marks, 'status': status,'grade': grade})


def student_result_view(request):
    profile = Profile.objects.get(user=request.user)
    student_rollno = profile.rollno

    try:
        student = NewStudent.objects.get(rollno=student_rollno)
        marks = StudentMarks.objects.filter(student=student)

        total = sum(m.marks for m in marks)
        count = marks.count()
        avg = total / count if count > 0 else 0

        is_fail = any(m.marks < 35 for m in marks)

        if is_fail:
            status = "Fail"
            grade = ""
        else:
            if avg >= 90:
                grade = "A"
            elif avg >= 80:
                grade = "B"
            elif avg >= 70:
                grade = "C"
            elif avg >= 60:
                grade = "D"
            else:
                grade = "E"
            status = f"Pass with Grade {grade}"

        context = {
            'student': student,
            'marks': marks,
            'status': status
        }

    except NewStudent.DoesNotExist:
        context = {
            'error': "No result found for your roll number."
        }

    return render(request, 'studentResult.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback

# Show feedback form and handle submission
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Feedback.objects.create(student=request.user, message=message)
            return render(request, 'feedback_form.html', {'message': 'Feedback submitted successfully!'})
    return render(request, 'feedback_form.html')


# Admin view to see all feedback
@login_required
def view_feedbacks(request):
    if request.user.is_authenticated and request.user.email == 'admin@admin.com':
        feedbacks = Feedback.objects.all().order_by('-submitted_at')
        return render(request, 'admin_feedback.html', {'feedbacks': feedbacks})
    return redirect('dashboard')

from django.utils import timezone

def submit_leave(request):
    message = None

    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        reason = request.POST.get('message')

        if leave_date and reason:
            Leave.objects.create(
                student=request.user,
                submitted_at=timezone.now(),
                leave_date=leave_date,
                message=reason,
                status='Pending'
            )
            message = 'Leave submitted successfully!'

    # ✅ Always fetch the leaves of the current student
    leaves = Leave.objects.filter(student=request.user).order_by('-submitted_at')

    return render(request, 'studentLeave.html', {'message': message, 'leaves': leaves})



# Admin view to see all feedback
@login_required
def view_leave(request):
    if request.user.is_authenticated and request.user.email == 'admin@admin.com':
        leaves = Leave.objects.all().order_by('-submitted_at')
        return render(request, 'admin_leave.html', {'leaves': leaves})
    return redirect('dashboard')

def approve_leave_by_time(request, submitted_at):
    try:
        submitted_at_dt = parse_datetime(submitted_at)
        leave = Leave.objects.get(submitted_at=submitted_at_dt)
    except (Leave.DoesNotExist, ValueError, TypeError):
        raise Http404("Leave not found.")

    leave.status = "Approved"
    leave.save()
    messages.success(request, "Leave approved based on time.")
    return redirect('adminleave')

def apply_leave(request):
    message = None

    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        reason = request.POST.get('message')

        Leave.objects.create(
            student=request.user,
            submitted_at=timezone.now(),
            leave_date=leave_date,
            message=reason,
            status='Pending'
        )
        message = "Leave applied successfully!"

    leaves = Leave.objects.filter(student=request.user).order_by('-submitted_at')
    return render(request, 'studentLeave.html', {'message': message, 'leaves': leaves})
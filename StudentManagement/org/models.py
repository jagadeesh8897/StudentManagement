from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Project(models.Model):
    username=models.CharField(max_length=100)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    rpassword=models.CharField(max_length=100)

    def __str__(self):

        return self.username
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    rollno = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.user.username}'


class NewStudent(models.Model):
    fullname=models.CharField(max_length=100)
    rollno=models.CharField(max_length=100)
    course=models.CharField(max_length=100)


    def __str__(self):
        return self.fullname
    class Meta:
        db_table = 'newstudent'

class StudentMarks(models.Model):
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.fullname} - {self.subject}"

class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.student.username}"
class Leave(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    leave_date = models.DateField(null=True, blank=True)  # required for your form
    message = models.TextField()
    status = models.CharField(max_length=20, default="Pending")

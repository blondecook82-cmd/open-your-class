from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.
from .utils import BaseTimeStamp

class TheUser(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'

    ROLE_CHOICES = (
        (STUDENT, 'Apprenant'),
        (TEACHER, 'Enseignant'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT
    )

class Course(BaseTimeStamp):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    ''' gratuit/payant : version ulterieure '''
    # is_paid = models.BooleanField(default=True)
    # def can_access() if user is authenticated and user is 'student'

    def __str__(self):
        return f' cours {self.name} du teacher {self.teacher.username}'


class Chapter(BaseTimeStamp):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='chapters'
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']

class Lesson(BaseTimeStamp):
    chapter = models.ForeignKey(
        Chapter, 
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    explication = models.TextField()
    video_course = models.FileField(
        upload_to='courses/lessons/%d/%m/%Y',
        validators=[FileExtensionValidator(
            allowed_extensions=['mp4', 'mkv'],
            message='cette extension n\'est pas autorisé. [mp4 ou mkv] sont autorisés.'
        )]
        
    )

    def __str__(self):
        return f'{self.title} du chapitre {self.chapter.order}' 


class Enrollment(BaseTimeStamp):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    class Meta:
        ordering = ['-date_pub']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                # l etudian reserve des cours payants une seule fois ...
                name='unique_student_course_enrollment'
            )
        ]
        verbose_name_plural = 'Cours reservés'

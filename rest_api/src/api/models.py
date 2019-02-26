from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).get_queryset()\
                    .filter(available=True, deleted=False)

class ExamSheet(models.Model):
    title = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(User, related_name='exam_sheets', null=True, on_delete=models.SET_NULL)
    available = models.BooleanField(null=False, default=False)
    deleted = models.BooleanField(null=False, default=False)
    version = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    availables = AvailableManager()

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.title

    def delete(self):
        self.deleted = True
        self.save()

    def save(self):
        if self.version == -1:
            raise ValidationError('Zero value is not allowed.')
        elif self.author.is_staff is False:
            raise ValidationError('Only teacher cad add or edit exam sheet.')
        else:
            self.version += 1
            super(ExamSheet, self).save()

class Question(models.Model):
    POINTS_CHOICES = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five')
    )

    examsheet = models.ForeignKey(ExamSheet, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(null=False)
    points = models.IntegerField(choices=POINTS_CHOICES)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField(null=False)
    is_correct = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.text

class ExamResult(models.Model):
    author = models.ForeignKey(User, related_name='written_exams', null=True, on_delete=models.SET_NULL)
    exam = models.ForeignKey(ExamSheet, related_name='filled_exam_sheets', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    earned_points = models.PositiveIntegerField()
    points_to_get = models.PositiveIntegerField()

    def save(self):
        if self.author.is_staff is True:
            raise ValidationError('Only schoolboy can write an exam.')
        elif self.earned_points > self.points_to_get:
            raise ValidationError('The maximum value of earned points has been exceeded.')
        else:
            super(ExamResult, self).save()

    @property
    def get_mark(self):
        if self.earned_points > 0:
            return round((self.earned_points/self.points_to_get)*100)
        else:
            return 0
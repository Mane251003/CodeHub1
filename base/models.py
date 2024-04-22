from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Topic(models.Model):
    name=models.CharField(max_length=16)

    def __str__(self):
        return self.name
    
class Question(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    write_question=models.TextField(max_length=50, null=False)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['updated', 'created']

    def __str__(self) :
        return self.write_question
    
class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    question=models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    comment=models.TextField(max_length=50)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    


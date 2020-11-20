from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import related
from imagekit.models import ProcessedImageField
from django.urls import reverse

# Create your models here.
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format = 'JPEG',
        options = {'quality' : 100},
        blank = True,
        null = True
    )

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])

    def __str__(self):
        return self.username
        
#creator(user A) follows following(user B)
class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username   

class Post(models.Model):
    author = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'my_posts'
    ) 
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality' : 100},
        blank = True,
        null = True
    )
    posted_on = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        blank = True,
        null = True,
    )
    def get_like_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("post_detail", args = [str(self.id)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments',)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add = True, editable = False)

    def __str__(self):
        return self.comment
    
class Like(models.Model):
    post = models.ForeignKey(#relationshipe of insta's user and post
        Post,
        on_delete = models.CASCADE, #if post be deleted, like will be deleted
        related_name = 'likes' #user can see how many likes on his post
          )
    user = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'likes' #user can see how many post likes he did on other user's post
    )

    class Meta:
        unique_together = ("post", "user") #a post only have a user
    
    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title




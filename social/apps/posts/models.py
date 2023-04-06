from django.db import models


class UserPost(models.Model):
    author = models.ForeignKey(
        to="auth_user.CustomUser",
        related_name="user_posts",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=128
    )

    content = models.TextField()

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.author}: {self.title}'


class Like(models.Model):
    user = models.ForeignKey(
        to="auth_user.CustomUser",
        related_name="user_likes",
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        to="posts.UserPost",
        related_name="likes",
        on_delete=models.CASCADE
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} liked {self.post}'

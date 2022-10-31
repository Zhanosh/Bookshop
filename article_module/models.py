from django.db import models
from django.utils.text import slugify
from Acount_module.models import UserAcount


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(max_length=30000, verbose_name='Desctiption')
    image = models.ImageField(upload_to='articles_image', verbose_name='Image')
    create_date = models.DateField(auto_now=True, verbose_name='Create date')
    author = models.ForeignKey(UserAcount, on_delete=models.CASCADE, verbose_name='Author')
    slug = models.CharField(max_length=150, verbose_name='Url', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(self, *args, **kwargs)

    def __str__(self):
        return self.title

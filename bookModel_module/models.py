from django.db import models
from django.utils.text import slugify
from Acount_module.models import UserAcount


class BookSubjectModel(models.Model):
    subject_name = models.CharField(max_length=200, verbose_name='Category name')

    def save(self, *args, **kwargs):
        self.url = slugify(self.subject_name)
        super(BookSubjectModel, self).save(self, *args, **kwargs)

    def __str__(self):
        return self.subject_name


class BookCategoryModels(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, db_index=True, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.url = slugify(self.title)
        super(BookCategoryModels, self).save(self, *args, **kwargs)

    def __str__(self):
        return self.title


class BookModels(models.Model):
    name = models.CharField(max_length=300, verbose_name='Book name', null=False, blank=False, )
    price = models.FloatField(verbose_name='Price', null=False, blank=False)
    description = models.TextField(max_length=2000, verbose_name='Descriptions')
    image = models.ImageField(upload_to='bookimage', verbose_name='Book image', null=False, blank=False)
    author = models.CharField(max_length=150, verbose_name='Author', null=False, blank=False)
    publisher = models.CharField(max_length=150, verbose_name='Published')
    translator = models.CharField(max_length=150, verbose_name='Translator', null=True, blank=True)
    language = models.CharField(max_length=100, verbose_name='Language', null=False, blank=False)
    year_of_publication = models.DateField(verbose_name='Create date', null=False, blank=False)
    number_of_pages = models.IntegerField(verbose_name='Pages', null=False, blank=False)
    subject = models.ManyToManyField('BookSubjectModel', verbose_name='Subject', null=True, blank=True)
    category = models.ManyToManyField('BookCategoryModels', verbose_name='Category')
    slug = models.CharField(max_length=150, null=True, blank=True, verbose_name='Url', unique=True)
    active = models.BooleanField(verbose_name='Active:On/Off', default=False)
    offer = models.BooleanField(verbose_name='Offer', default=False)
    offer_price = models.FloatField(verbose_name='Offer Price', null=True, blank=True)
    favorite=models.ManyToManyField(UserAcount,)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BookModels, self).save(self, *args, **kwargs)

    def __str__(self):
        return self.name

from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView, TemplateView
from bookModel_module.models import BookModels, BookSubjectModel, BookCategoryModels
from Package.conventor import group_list
from order_module.models import Order
from django.db.models import Q
from article_module.models import Article
from template_module.froms import EmailSendForm
from Package.send_mail import send_email


def header_partial(request):
    return render(request, 'shared/header-partial.html')


def footer_partial(request):
    return render(request, 'shared/footer-partial.html')


def book_categories_component(request):
    book_categories = BookCategoryModels.objects.all()
    context = {
        'categories': book_categories
    }
    return render(request, 'template_module/shop/component/book-category-component.html', context)


def searchView(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        books = BookModels.objects.filter(name__contains=searched)
        return render(request, 'template_module/serch-page.html', {
            'searched': searched,
            'books': books,
        })
    else:
        return render(request, 'template_module/serch-page.html')


# -----------------------------------------------------------------------


class HomePageView(TemplateView):
    template_name = 'template_module/index.html'

    def get_context_data(self, **kwargs):
        request = self.request
        context = super(HomePageView, self).get_context_data()
        email_input_form = EmailSendForm(request.POST, request.FILES)
        context['email_input'] = email_input_form
        # user_email = email_input_form.cleaned_data.get('email')
        # if email_input_form.is_valid():
        #     send_email('فعالسازی حساب کاربری', user_email.email, {'user': user_email}, 'email-msg/send-email-massege.html')

        lastest_product = BookModels.objects.filter(active=True).order_by('-id')[:5]
        context['lastest_product'] = group_list(lastest_product)
        offer_book = BookModels.objects.filter(active=True, offer=True).order_by('price')[:8]
        context['offer_book'] = group_list(offer_book)
        new_book_slider = BookModels.objects.filter(active=True).order_by('-year_of_publication')[:2]
        context['new_book_slider'] = group_list(new_book_slider)
        article = Article.objects.all().order_by('-create_date')[:3]
        context['articles_list'] = group_list(article)
        curent_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                  user_id=request.user.id)
        total_amount = 0
        for order_detail in curent_order.orderdetail_set.all():
            if order_detail.product.offer:
                total_amount += order_detail.product.offer_price * order_detail.count
            else:
                total_amount += order_detail.product.price * order_detail.count
        context['sum'] = float(total_amount)
        # global fav
        # books = BookModels.objects.filter(favorite=request.user.id)
        # context['books'] = books
        # book = (BookModels)
        # if book.favorite.filter(id=request.user.id).exists():
        #     context['fav'] = True
        return context


class ContactUs(TemplateView):
    template_name = 'template_module/Contact-us-page.html'

    def get_context_data(self, **kwargs):
        request = self.request
        context = super(ContactUs, self).get_context_data()
        curent_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                user_id=request.user.id)
        total_amount = 0
        for order_detail in curent_order.orderdetail_set.all():
            if order_detail.product.offer:
                total_amount += order_detail.product.offer_price * order_detail.count
            else:
                total_amount += order_detail.product.price * order_detail.count
        context['sum'] = float(total_amount)
        return context


class About(TemplateView):
    template_name = 'template_module/about-page.html'

    def get_context_data(self, **kwargs):
        request = self.request
        context = super(About, self).get_context_data()
        curent_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                user_id=request.user.id)
        total_amount = 0
        for order_detail in curent_order.orderdetail_set.all():
            if order_detail.product.offer:
                total_amount += order_detail.product.offer_price * order_detail.count
            else:
                total_amount += order_detail.product.price * order_detail.count
        context['sum'] = float(total_amount)
        return context


class ShopList(ListView):
    template_name = 'template_module/shop/shop-page.html'
    model = BookModels
    context_object_name = 'books'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        request = self.request
        context = super(ShopList, self).get_context_data()
        context['all'] = BookModels.objects.all()
        curent_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                  user_id=request.user.id)
        total_amount = 0
        for order_detail in curent_order.orderdetail_set.all():
            if order_detail.product.offer:
                total_amount += order_detail.product.offer_price * order_detail.count
            else:
                total_amount += order_detail.product.price * order_detail.count
        context['sum'] = float(total_amount)
        search_post = request.GET.get('search')
        if search_post:
            context['posts'] = BookModels.objects.filter(
                Q(name__icontains=search_post) & Q(author__icontains=search_post))
        else:
            # If not searched, return default posts
            context['posts'] = BookModels.objects.all().order_by("-year_of_publication")
        return context

    def get_queryset(self):
        request = self.request
        query = super(ShopList, self).get_queryset()
        category_name = self.kwargs.get('cat')
        if category_name is not None:
            query = query.filter(category__title__iexact=category_name)
        return query


class ShopDetail(DetailView):
    template_name = 'template_module/shop/shop-detail-page.html'
    model = BookModels
    context_object_name = 'book'

    def get_queryset(self):
        query = super(ShopDetail, self).get_queryset()
        return query

    def get_context_data(self, **kwargs):
        request = self.request
        context = super(ShopDetail, self).get_context_data()
        curent_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                  user_id=request.user.id)
        total_amount = 0
        for order_detail in curent_order.orderdetail_set.all():
            if order_detail.product.offer:
                total_amount += order_detail.product.offer_price * order_detail.count
            else:
                total_amount += order_detail.product.price * order_detail.count
        context['sum'] = float(total_amount)

        return context

from django.db import models
from django.utils.safestring import mark_safe

from app_loging.models import User

STATUS_CHOISE = (
    ('в процессе', 'Обработка'),
    ('в доставке', 'В доставке'),
    ('доставлено', 'Доставлено'),
)

STATUS = (
    ('черновик', 'Черновик'),
    ('недоступно', 'Недоступно'),
    ('отклонено', 'Отклонено'),
    ('опубликовано', 'Опубликовано'),
)

RATING = (
    (1, '⭐✩✩✩✩'),
    (2, '⭐⭐✩✩✩'),
    (3, '⭐⭐⭐✩✩'),
    (4, '⭐⭐⭐⭐✩'),
    (5, '⭐⭐⭐⭐⭐'),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    title = models.CharField(max_length=500, default='The Best Category')
    image = models.ImageField(upload_to='category', default='category.jpg')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def category_image(self):
        return mark_safe('<img src="%s" width = "50" height = "50">' % (self.image.url))

    def __str__(self):
        return self.title


class Vendor(models.Model):
    title = models.CharField(max_length=500, default='The Best Vendor')
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    description = models.TextField(null=True)
    available = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Продавцы'
        verbose_name = 'Продавец'

    def vendor_image(self):
        return mark_safe('<img src="%s" width = "50" height = "50">' % (self.image.url))

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=500, default='The Best Product')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = models.TextField(null=True)
    price = models.IntegerField(default='199')
    old_price = models.IntegerField(default='299')
    product_status = models.CharField(choices=STATUS, max_length=100, default='черновик')
    feachured = models.BooleanField(default=False, verbose_name='Опубликовано')
    quantity = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, related_name='vendor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='category')

    class Meta:
        verbose_name_plural = 'Продукты'
        verbose_name = 'Продукт'

    def products_image(self):
        return mark_safe('<img src="%s" width = "50" height = "50">' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    image = models.ImageField(upload_to='product-images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Продуктовые изображения'
        verbose_name = 'Продуктовая иконка'


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='product')
    review = models.TextField(max_length=1000)
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    def __str__(self):
        return self.product.title

    def get_ratings(self):
        return self.rating


class Contact(models.Model):
    objects = models.manager.Manager()
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE)

    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'


class Order(models.Model):
    objects = models.manager.Manager()
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='user', blank=True,
                             on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='Статус', choices=STATUS_CHOISE, max_length=15)
    contact = models.ForeignKey(Contact, verbose_name='Контакт',
                                blank=True, null=True,
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказов'
        verbose_name_plural = "Список заказов"
        ordering = ('-dt',)

    def __str__(self):
        return str(self.dt)


class OrderItem(models.Model):
    objects = models.manager.Manager()
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)

    product_name = models.ForeignKey(Product, verbose_name='Информация о продукте', related_name='ordered_items',
                                     blank=True,
                                     on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Список заказанных позиций"

    def __str__(self):
        return str(self.order.id)


class Projects(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    stack = models.CharField(max_length=1000)
    git = models.URLField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='projects', default='project.jpg')

    class Meta:
        verbose_name_plural = 'Проекты'
        verbose_name = 'Проект'

    def project_image(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50">' % (self.image))

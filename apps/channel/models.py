from django.db import models
from utils.validators import FileMimeValidator


def upload_to(instance, filename):
    return f'channel/{instance.pk}/img_channel/{filename}'


def upload_content_to(instance, filename):
    return f'channel/content/{filename}'


class RoleUserChannel(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class ChannelsModel(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='Описание')
    img = models.ImageField('Картинка канала', upload_to=upload_to, blank=True, null=True,
                            validators=[FileMimeValidator()])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')
    is_private = models.BooleanField(default=False, verbose_name='Приватный?')

    class Meta:
        verbose_name = "Каналы"
        verbose_name_plural = "Канал"

    def __str__(self):
        return self.name


class UsersChannelModel(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    channel = models.ForeignKey('channel.ChannelsModel', on_delete=models.CASCADE, verbose_name='Канал')
    enable_notification = models.BooleanField(default=False, verbose_name='Уведомления')
    role = models.CharField(verbose_name='Роль', choices=RoleUserChannel.choices, max_length=64)

    class Meta:
        verbose_name = "Пользователи каналов"
        verbose_name_plural = "Пользователь канала"

    def __str__(self):
        return f"{self.pk}"


class ContentAbstractModel(models.Model):
    user_channel = models.ForeignKey('channel.UsersChannelModel', on_delete=models.CASCADE,
                                     verbose_name='Пользователь канала')
    count_like = models.PositiveIntegerField(default=0, verbose_name='Количество лайков')

    # hashtag

    class Meta:
        abstract = True


class ArticleModel(ContentAbstractModel):
    title = models.CharField(max_length=256, verbose_name='Название')
    full_text = models.TextField(verbose_name='Полный тест')
    previous_text = models.CharField(verbose_name='Сокращенный текст', max_length=1024)

    class Meta:
        verbose_name = "Публикации каналов"
        verbose_name_plural = "Публикация канала"

    def __str__(self):
        return f"{self.title}"


class MediaModel(ContentAbstractModel):
    text = models.CharField(max_length=256, verbose_name='Название', blank=True, null=True)
    source_media = models.FileField('Исходное медиа', upload_to=upload_content_to)
    compressed_media = models.FileField('сжатое медиа', upload_to=upload_content_to)

    class Meta:
        verbose_name = "Медиа каналов"
        verbose_name_plural = "Медиа канала"

    def __str__(self):
        return f"{self.text}"

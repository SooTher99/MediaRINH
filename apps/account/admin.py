from django.contrib import admin
from apps.account.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        password = self.cleaned_data.get('password')
        validate_password(password=password)


class UserModelsAdmin(admin.ModelAdmin):
    """Настройки админки для User"""

    form = UserForm
    list_display = ('id', 'username', "first_name", "last_name", 'email', 'is_active', 'post_agreement', 'is_superuser')
    list_display_links = ('id', 'username')
    search_fields = ('id', 'email', 'username')
    list_filter = ('is_active', 'is_superuser')

    readonly_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "post_agreement",
        "avatar",
        "is_superuser",
        "is_staff",
        "last_login",
        "date_joined",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "post_agreement",
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "avatar",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                    "is_active",
                )
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ()
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        return obj.save()


admin.site.register(User, UserModelsAdmin)
admin.site.unregister(Group)

def send_notification_email(user_email, subject, message):
    send_mail(
        subject,
        message,
        'admin@example.com',  # Replace with your email
        [user_email],
        fail_silently=False,
    )
from django.contrib import admin
from .models import BlogPost, Comment

@admin.action(description='Block selected users')
def block_users(modeladmin, request, queryset):
    queryset.update(is_active=False)  # Assuming a boolean `is_active` in the user model
    for user in queryset:
        send_notification_email(user.email, "Account Blocked", "Your account has been blocked by the admin.")

@admin.action(description='Block selected posts')
def block_posts(modeladmin, request, queryset):
    queryset.delete()  # Delete posts
    # Optionally notify authors about deletion
    for post in queryset:
        send_notification_email(post.author.email, "Post Deleted", "Your post has been deleted by the admin.")

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    actions = [block_posts]

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment)

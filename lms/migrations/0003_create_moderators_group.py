from django.db import migrations

def create_moderators_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Создаем группу "Модераторы"
    moderators_group, created = Group.objects.get_or_create(name='Модераторы')

    # Добавляем права для моделей Course и Lesson
    course_ct = ContentType.objects.get(app_label='lms', model='course')
    lesson_ct = ContentType.objects.get(app_label='lms', model='lesson')

    permissions = Permission.objects.filter(
        content_type__in=[course_ct, lesson_ct],
        codename__in=[
            'change_course', 'view_course',
            'change_lesson', 'view_lesson'
        ]
    )

    # Назначаем права группе "Модераторы"
    moderators_group.permissions.set(permissions)

class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0002_initial"),  # Замените на актуальную зависимость вашей миграции
    ]

    operations = [
        migrations.RunPython(create_moderators_group),
    ]

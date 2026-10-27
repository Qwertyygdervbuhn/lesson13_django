from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from .models import Course


class CourseTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="test_owner")
    def test_create(self):
        course = Course.objects.create(owner=self.owner, title="Python",
                                       slug="python", capacity=12)
        self.assertEqual(Course.objects.get(pk=course.pk).title, "Python")
    def test_default_status(self):
        course = Course.objects.create(
            owner=self.owner, title="Draft Course", slug="draft-course", capacity=10
        )
        self.assertEqual(course.status, Course.Status.DRAFT)
    def test_validation(self):
        course = Course(owner=self.owner, title="Bad", slug="bad", capacity=0)
        with self.assertRaises(ValidationError):
            course.full_clean()
    def test_database_constraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Course.objects.create(owner=self.owner, title="Bad",
                                      slug="bad", capacity=0)
    def test_filter(self):
        Course.objects.create(owner=self.owner, title="Live", slug="live",
                              status=Course.Status.PUBLISHED)
        self.assertEqual(Course.objects.filter(
            status=Course.Status.PUBLISHED).count(), 1)
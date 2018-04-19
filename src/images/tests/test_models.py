from django.test import TestCase
from django.contrib.auth.models import User

from buckets.models import Bucket, Label
from images.models import *
from projects.models import Project


class ImageModelTest(TestCase):

    def setUp(self):
        self.setUsers()
        self.setProjects()
        self.setBuckets()
        self.setLabels()
        self.setImages()

    def setUsers(self):
        self.user_1 = User.objects.create_user(username='user1', email='user@example.com', password='userexample')
        self.user_2 = User.objects.create_user(username='user2', email='user2@example.com', password='userexample')

    def setProjects(self):
        self.project_1 = Project.objects.create(name="Project 1", description='My custom project 1', user=self.user_1)

    def setLabels(self):
        self.label_1 = Label.objects.create(name='Kitchen', project=self.project_1)
        self.label_2 = Label.objects.create(name='Bathroom', project=self.project_1)

    def setBuckets(self):
        self.bucket_1 = Bucket.objects.create(name='my bucket', user=self.user_1, project=self.project_1)
        self.bucket_2 = Bucket.objects.create(name='my bucket 2', user=self.user_1, project=self.project_1)

    def setImages(self):
        self.image_1 = Image.objects.create(file='img1.jpg', hash='1111', bucket=self.bucket_1)
        self.image_2 = Image.objects.create(file='img2.jpg', hash='2222', bucket=self.bucket_1)
        self.image_3 = Image.objects.create(file='img3.jpg', hash='3333', bucket=self.bucket_1)
        self.image_4 = Image.objects.create(file='img4.jpg', hash='4444', bucket=self.bucket_2)

    def setVotes(self):
        Vote.objects.create(user=self.user_1, image=self.image_1, bucket=self.bucket_1, label=self.label_1, choice=True)
        Vote.objects.create(user=self.user_1, image=self.image_2, bucket=self.bucket_1, label=self.label_1, choice=False)
        Vote.objects.create(user=self.user_1, image=self.image_3, bucket=self.bucket_1, label=self.label_1, choice=False)

        Vote.objects.create(user=self.user_2, image=self.image_2, bucket=self.bucket_1, label=self.label_2, choice=True)
        Vote.objects.create(user=self.user_2, image=self.image_3, bucket=self.bucket_1, label=self.label_2, choice=False)

    def setImagesHashes(self):
        self.image_5 = Image.objects.create(file='img5.jpg', hash='5555', bucket=self.bucket_1)
        self.image_6 = Image.objects.create(file='img6.jpg', hash='6666', bucket=self.bucket_1)
        self.image_7 = Image.objects.create(file='img7.jpg', hash='5555', bucket=self.bucket_2)
        self.image_8 = Image.objects.create(file='img8.jpg', hash='8888', bucket=self.bucket_2)

        Vote.objects.create(user=self.user_1, image=self.image_5, bucket=self.bucket_1, label=self.label_1, choice=True)

    def test_get_random_image_with_no_vote(self):
        """
        A user who voted on an image with a specific label, will not have this image propose again.
        """
        Vote.objects.create(user=self.user_1, image=self.image_1, bucket=self.bucket_1, label=self.label_1, choice=True)

        q = Image.objects.get_samples_with_no_vote(bucket=self.bucket_1, label=self.label_1.id, number=8, user=self.user_1)
        q = q.values_list('id', flat=True)

        self.assertQuerysetEqual(q, ['2', '3'], ordered=False)

    def test_get_random_image_with_no_vote_other_label(self):
        """
        A user who voted on an image with a specific label, will not have this image propose again.
        """
        Vote.objects.create(user=self.user_1, image=self.image_1, bucket=self.bucket_1, label=self.label_2, choice=True)

        q = Image.objects.get_samples_with_no_vote(bucket=self.bucket_1, label=self.label_1.id, number=8, user=self.user_1)
        q = q.values_list('id', flat=True)

        self.assertQuerysetEqual(q, ['1', '2', '3'], ordered=False)

    def test_get_random_image_with_no_vote_other_user(self):
        """
        A user who voted on an image with a specific label, will not have this image propose again.
        """
        Vote.objects.create(user=self.user_1, image=self.image_1, bucket=self.bucket_1, label=self.label_1, choice=True)

        # q = Image.objects.get_samples_with_no_vote(bucket=self.bucket_1, label=self.label_1.id, number=8, user=self.user_2)
        # q = q.values_list('id', flat=True)

        # self.assertEqual(q, ['1', '2', '3'])

    def test_get_random_image_with_no_vote_other_user(self):
        """
        A user who voted on an image with a specific label, will not have this image propose again.
        """
        self.setVotes()

        user1_label1_images = Image.objects.get_samples_with_no_vote(bucket=self.bucket_1, label=self.label_1.id, number=8, user=self.user_1)
        self.assertEqual(user1_label1_images, [])

        user1_label2_images = Image.objects.get_samples_with_no_vote(bucket=self.bucket_1, label=self.label_2.id, number=8, user=self.user_1)
        user1_label2_images = user1_label2_images.values_list('id', flat=True)
        self.assertEqual(list(user1_label2_images), [1, 2, 3])

        user2_label1_images = Image.objects.get_samples_with_no_vote(bucket=self.bucket_1, label=self.label_1.id, number=8, user=self.user_2)
        user2_label1_images = user2_label1_images.values_list('id', flat=True)
        self.assertEqual(list(user2_label1_images), [1, 2, 3])

        user2_label2_images = Image.objects.get_samples_with_no_vote(bucket=self.bucket_1, label=self.label_2.id, number=8, user=self.user_2)
        user2_label2_images = user2_label2_images.values_list('id', flat=True)
        self.assertEqual(list(user2_label2_images), [1])

    def test_samples_with_same_hash(self):
        """
        The user will not have to vote on an image with a label in another bucket if the hash is the same.
        """
        self.setImagesHashes()

        user1_label1_images = Image.objects.get_samples_with_no_vote(bucket=self.bucket_2, label=self.label_1.id, number=8, user=self.user_1)
        user1_label1_images = user1_label1_images.values_list('id', flat=True)
        self.assertEqual(list(user1_label1_images), [4, 8])


class VoteModelTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='user1', email='user@example.com', password='userexample')
        self.project_1 = Project.objects.create(name="Project 1", description='My custom project 1', user=self.user_1)
        self.label_1 = Label.objects.create(name='Kitchen', project=self.project_1)
        self.bucket_1 = Bucket.objects.create(name='my bucket', user=self.user_1, project=self.project_1)
        self.image_1 = Image.objects.create(file='img1.jpg', hash='1111', bucket=self.bucket_1)

    def test_a_user_cant_vote_twice_on_the_same_image_with_the_same_label(self):
        Vote.objects.create(user=self.user_1, image=self.image_1, bucket=self.bucket_1, label=self.label_1, choice=True)
        Vote.objects.create(user=self.user_1, image=self.image_1, bucket=self.bucket_1, label=self.label_1, choice=True)

        self.assertEqual(Vote.objects.count(), 1)


class UploadImageTest(TestCase):
    def setUp(self):
        self.setUsers()
        self.setProjects()
        self.setBuckets()
        self.setImages()

    def setUsers(self):
        self.user_1 = User.objects.create_user(username='user1', email='user@example.com', password='userexample')

    def setProjects(self):
        self.project_1 = Project.objects.create(name="Project 1", description='My custom project 1', user=self.user_1)

    def setBuckets(self):
        self.bucket_1 = Bucket.objects.create(name='my bucket', user=self.user_1, project=self.project_1)

    def setImages(self):
        self.image_1 = Image.objects.create(file='img1.jpg', hash='1111', bucket=self.bucket_1)
        self.image_2 = Image.objects.create(file='img2.jpg', hash='2222', bucket=self.bucket_1)

    def test_upload_images(self):
        """
        When a user upload images, a image with a same hash will not be upload
        """
        Image.objects.create(file='img3.jpg', hash='1111', bucket=self.bucket_1)

        images = Image.objects.filter(bucket=self.bucket_1).values_list('id', flat=True)

        self.assertEqual(list(images), [1, 2])

from rest_framework import serializers
from courses.models import Category, Course, Lesson, Tag, User, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url
        return req


class CourseSerializer(ItemSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'created_date', 'Category']


class TagSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ItemSerializer):
    tags = TagSerialzier(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'created_date', 'tags']


class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerialzier(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags']


class AuthenticatedLessonDetailsSerializer(LessonDetailsSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return lesson.like_set.filter(active=True, user=request.user).exists()

    class Meta:
        model = LessonDetailsSerializer.Meta.model
        fields = LessonDetailsSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'user']

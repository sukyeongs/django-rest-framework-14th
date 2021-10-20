from rest_framework import serializers
from .models import Profile, Post, Image, Comment


class PostSerializer(serializers.ModelSerializer):
    post_author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'post_author', 'post_content', 'comments']

    def get_post_author(self, obj):
        return obj.post_author.username

    def get_comments(self, obj):
        queries = obj.post_comments.all()
        comments = []
        for query in queries:
            comment = {'comment_author': query.comment_author.username, 'comment_content': query.comment_content}
            comments.append(comment)
        return comments

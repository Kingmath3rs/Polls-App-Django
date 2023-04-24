from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from comment.models import Comment
from comment.serializers import CommentSerializer
from poll.models import Poll


class CreateAndList(APIView):
    def get(self, request):
        context = {}
        comments = Comment.objects.all()
        context['comments'] = CommentSerializer(comments, many=True).data
        return Response(context, status=HTTP_200_OK)

    def post(self, request):
        context = {}
        comment = Comment(
            title=request.data.get('title'),
            content=request.data.get('content'),
            poll_id=request.data.get('poll'),
            owner=request.user
        )
        comment.save()
        context['poll'] = CommentSerializer(comment).data
        return Response(context, status=HTTP_200_OK)

    class CommentSingle(APIView):
        def get(self, request, pk):
            context = {}
            try:
                comment = Comment.objects.get(id=pk)
                context['comment'] = CommentSerializer(comment).data
                status_code = HTTP_200_OK

            except:
                context['msg'] = "comment bilaakh"
                status_code = HTTP_404_NOT_FOUND
            return Response(context,status=status_code)

        def put(self, request, pk):
            context = {}
            try:
                comment = Comment.objects.get(id=pk)
                comment.title = request.data.get('title', comment.title)
                comment.content = request.data.get('desc', comment.content)
                comment.save()
                context['comment'] = CommentSerializer(comment).data
                status_code = HTTP_200_OK
            except:
                context['msg'] = "Comment bilaakh"
                status_code = HTTP_404_NOT_FOUND
            return Response(context,status=status_code)

        def delete(self, request, pk):
            context = {}
            try:
                comment = Comment.objects.get(id=pk)
                comment.delete()
                context['msg'] = "Comment siiiiktir"
                status_code = HTTP_200_OK
            except:
                context['msg'] = "Comment bilaakh"
                status_code = HTTP_404_NOT_FOUND
            return Response(context,status=status_code)

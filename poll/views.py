from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from poll.models import Poll
from poll.serializers import PollSerializer


class CreateAndList(APIView):
    def get(self, request):
        context = {}
        polls = Poll.objects.all()
        context['polls'] = PollSerializer(polls, many=True).data
        return Response(context, status=HTTP_200_OK)

    def post(self, request):
        context = {}
        poll = Poll(
            title=request.data.get('title'),
            desc=request.data.get('desc'),
            time_left=request.data.get('time_left'),
            owner=request.user
        )
        poll.save()
        context['poll'] = PollSerializer(poll).data
        return Response(context, status=HTTP_200_OK)


class PollSingle(APIView):
    def get(self, request, pk):
        context = {}
        try:
            poll = Poll.objects.get(id=pk)
            context['poll'] = PollSerializer(poll).data
            status_code = HTTP_200_OK

        except:
            context['msg'] = "poll bilaakh"
            status_code = HTTP_404_NOT_FOUND
        return Response(context, status=status_code)

    def put(self, request, pk):
        context = {}
        try:
            poll = Poll.objects.get(id=pk)
            poll.title = request.data.get('title', poll.title)
            poll.desc = request.data.get('desc', poll.desc)
            poll.time_left = request.data.get('time_left', poll.time_left)
            poll.save()
            context['poll'] = PollSerializer(poll).data
            status_code = HTTP_200_OK
        except:
            context['msg'] = "Poll bilaakh"
            status_code = HTTP_404_NOT_FOUND
        return Response(context, status=status_code)

    def post(self, request, pk):
        context = {}
        try:
            poll = Poll.objects.get(id=pk)
            if request.user not in poll.voters:
                vote = request.data.get('vote')
                poll.voters.add(request.user)
                if vote == 1:
                    poll.total_vote += 1
                if vote == -1:
                    poll.total_vote += -1
                status_code = HTTP_200_OK
            else:
                context['msg'] = 'toosh koni? Siiiik'
                status_code = HTTP_403_FORBIDDEN
        except:
            context['msg'] = "user bilaakh"
            status_code = HTTP_404_NOT_FOUND
        return Response(context, status=status_code)

    def delete(self, request, pk):
        context = {}
        try:
            poll = Poll.objects.get(id=pk)
            poll.delete()
            context['msg'] = "Poll siiiiktir"
            status_code = HTTP_200_OK
        except:
            context['msg'] = "Poll bilaakh"
            status_code = HTTP_404_NOT_FOUND
        return Response(context, status=status_code)

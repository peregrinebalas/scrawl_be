from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Wall, Comment
from .serializers import CommentsSerializer, WallSerializer
import json

class ChatConsumer(WebsocketConsumer):

    def get_comments(self, data):
        wall = WallSerializer(Wall.objects.get(pk=data['pk']))
        comments = wall['comments']
        content = {
            'command': 'get_comments',
            'messages': comments
        }
        self.send_comments(content)

    def new_comment(self, data):
        wall = Wall.objects.get(pk=data['pk'])
        comment = wall.Comment.objects.create(
            wall=wall,
            comment=data['comment']
        )
        content = {
            'command': 'new_comment',
            'comment': CommentsSerializer(comment)
        }
        return self.send_wall_comment(content)

    commands = {
        "get_comments": get_comments,
        "new_comment": new_comment
    }

    def connect(self):
        self.wall_pk = self.scope['url_route']['kwargs']['pk']
        self.wall_group_pk = 'comments_%s' % self.wall_pk

        async_to_sync(self.channel_layer.group_add)(
            self.wall_group_pk,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.wall_group_pk,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_wall_comment(self, comment):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.wall_group_pk,
            {
                'type': 'wall_comment',
                'comment': comment
            }
        )

    def send_comments(self, comments):
        self.send(text_data=json.dumps(comments))

    # Receive message from room group
    def wall_comment(self, event):
        comment = event['comment']
        # Send message to WebSocket
        async_to_sync(self.send(text_data=json.dumps({
            'comment': comment
        })))

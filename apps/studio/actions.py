from turbo_response import TurboStream


def setVideoTopic(self, topic, video):
    if topic not in video.topics.all():
        video.topics.add(topic)
        html = TurboStream(f"yt--topic--{topic.id}").remove.render()
        self.send(text_data=html)


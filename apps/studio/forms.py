from django import forms

from .models import VideoDraft
from apps.channel.models import Video, Channel, Playlist
from guardian.shortcuts import get_objects_for_user


class ChannelCreationForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'description']


class VideoDraftForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        permissions = [
            'channel.add_playlist',
            'channel.change_playlist',
            'channel.delete_playlist',
            'channel.view_playlist']

        queryset = get_objects_for_user(user, perms=permissions, klass=Playlist, with_superuser=False)
        self.fields['playlist'].queryset = queryset

    class Meta:
        model = VideoDraft
        fields = ['title', 'description', 'thumbnail', 'playlist']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border border-gray-400 rounded',
                                            'data-action': 'input->studio#onDraftInputChange',
                                            'data-studio-target': 'VideoEditionInputField'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-400 rounded',
                                                 'data-controller': 'textarea-autogrow', 'rows': '4',
                                                 'data-textarea-autogrow-resize-debounce-delay-value': '500',
                                                 'data-studio-target': 'VideoEditionInputField'}),
            'thumbnail': forms.ClearableFileInput(attrs={'data-studio-target': 'VideoEditionInputField', 'hidden': True}),
            'playlist': forms.Select(attrs={'class': 'border border-gray-400 rounded',
                                            'data-studio-target': 'VideoEditionInputField'})
        }


class TopicCheckbox(forms.CheckboxSelectMultiple):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        if value:
            option["attrs"]["data-topic"] = value.instance.name
        return option


class VideoForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        permissions = [
            'channel.add_playlist',
            'channel.change_playlist',
            'channel.delete_playlist',
            'channel.view_playlist']

        queryset = get_objects_for_user(user, perms=permissions, klass=Playlist, with_superuser=False)
        self.fields['playlist'].queryset = queryset

    class Meta:
        model = Video
        fields = ['title', 'description', 'thumbnail', 'playlist']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border border-gray-300 rounded',
                                            'data-studio-target': 'VideoEditionInputField',
                                            'data-action': 'input->studio#onInputChange'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 rounded',
                                                 'data-controller': 'textarea-autogrow', 'rows': '4',
                                                 'data-textarea-autogrow-resize-debounce-delay-value': '500',
                                                 'data-studio-target': 'VideoEditionInputField',
                                                 'data-action': 'input->studio#onInputChange'}),
            'thumbnail': forms.ClearableFileInput(attrs={'hidden': True, 'data-studio-target': 'VideoEditionInputField',
                                                      'data-action': 'input->studio#triggerSubmit', 'accept': 'image/*'}),

            'playlist': forms.Select(attrs={'class': 'border border-gray-300 rounded text-gray-800', 'data-studio-target': 'VideoEditionInputField',
                                            'data-action': 'input->studio#onInputChange'}),
        }


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your playlist name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write a quick description of your playlist',
                                                 'data-controller': 'textarea-autogrow', 'rows': '4',
                                                 'data-textarea-autogrow-resize-debounce-delay-value': '500'})
        }

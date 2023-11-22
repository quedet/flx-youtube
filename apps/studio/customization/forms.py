from django import forms
from apps.channel.models import Channel, ChannelPicture, ChannelBanner


class ChannelBasicInfoForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter a channel name', 'class': 'border border-gray-400 rounded',}))
    pseudo = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter a channel handle', 'class': 'border border-gray-400 rounded',}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'border border-gray-400 rounded',
        'placeholder': 'Enter a channel description', 'data-controller': 'textarea-autogrow', 'rows': '4',
         'data-textarea-autogrow-resize-debounce-delay-value': '500',
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Channel
        fields = ['name', 'pseudo', 'description']


class ChannelPictureForm(forms.ModelForm):
    class Meta:
        model = ChannelPicture
        fields = ['original', 'cropX', 'cropY', 'cropWidth', 'cropHeight', 'type']


class ChannelBannerForm(forms.ModelForm):
    class Meta:
        model = ChannelBanner
        fields = ['original', 'cropX', 'cropY', 'cropWidth', 'cropHeight', 'type']

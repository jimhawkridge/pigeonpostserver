from base64 import b64encode, b64decode
from io import BytesIO

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
from django.shortcuts import render, get_object_or_404

from .models import Message
from .images import scale_and_dither, build_image, to_thermal


@csrf_exempt
def get_message(request, pk=None):
    if pk is None:
        message = Message.objects.filter(ackd=False).order_by('id').first()
    else:
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            message = None

    if message is None:
        raise Http404

    if request.method == 'DELETE':
        message.ackd = True
        message.save()
        return HttpResponse(status=204)

    # text = '\x1bl{}{}\r\n\r\n\r\n'.format(chr(settings.MARGIN), message.text)
    text = b64decode(message.text)
    text = text + '\r\n\r\n\r\n'
    response = '{}\r\n{}\r\n{}\r\n\r\n\r\n'.format(message.id, len(text), text)
    return HttpResponse(response)


def send(request):
    return render(request, 'send.html')


def status(request):
    return render(request, 'status.html')


def imageupload(request):
    data = request.FILES['image'].read()
    stream = BytesIO(data)
    out_stream = scale_and_dither(stream)
    request.session['image'] = b64encode(out_stream.getvalue())
    out_stream.close()

    return HttpResponse('')


def getimage(request):
    return HttpResponse(b64decode(request.session['image']), content_type='image/jpeg')


def enqueue(request):
    data = b64decode(request.session['image'])
    stream = BytesIO(data)
    text = request.POST.get('text', '')

    im = build_image(stream, text)
    im = im.rotate(90)
    im.save('test.png')
    thermal = b64encode(to_thermal(im))
    Message.objects.create(text=thermal)

    return HttpResponse('')


def get_status(request, pk=None):
    message = get_object_or_404(Message, pk=pk)
    return HttpResponse('true' if message.ackd else 'false')

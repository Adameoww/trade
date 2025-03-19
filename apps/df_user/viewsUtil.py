from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
from django.http import JsonResponse,HttpResponse

def verify_code(request):
    import random
    bgcolor = (224,224,224)
    width = 100
    height = 34
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('arial.ttf', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verifycode'] = rand_str
    buf = BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')

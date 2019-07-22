'''
    对图片的处理：模糊，转格式，生成验证码等
'''
import random
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import PIL.ImageFilter as ImageFilter

im = Image.open('./tr.jpg')
# 获得尺寸
w, h = im.size

# 缩放50%
im.thumbnail((w//2, h//2))
# 保存
im.save('./micor_tr.jpg', 'jpeg')

# 模糊效果
im = Image.open('./tr.jpg')
im2 = im.filter(ImageFilter.BLUR)
im2.save('./blur_tr.jpg', 'jpeg')

# 验证码

# 随机字母:


def rndChar():
    return chr(random.randint(65, 90))

# 随机颜色1:


def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:


def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


# 240 x 60:
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
font = ImageFont.truetype('/usr/share/fonts/TTF/oriya.ttf', 36)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素:
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor())
# 输出文字:
for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
# 模糊:
image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')

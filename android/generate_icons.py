from PIL import Image, ImageDraw, ImageFilter
import os

# Android mipmap 标准尺寸
SIZES = {
    'mdpi': 48,
    'hdpi': 72,
    'xhdpi': 96,
    'xxhdpi': 144,
    'xxxhdpi': 192,
}

# 自适应图标前景图尺寸（容器内的实际可见区域，108dp视口中的72dp）
FOREGROUND_SIZES = {
    'mdpi': 162,   # 72 * 48/48 * (108/72) 简化为实际px
    'hdpi': 243,
    'xhdpi': 324,
    'xxhdpi': 486,
    'xxxhdpi': 648,
}

ICON_108DP = 108  # 自适应图标视口

source_path = os.path.join(os.path.dirname(__file__), 'app', 'src', 'main', 'res', 'ic_source.jpg')
output_base = os.path.join(os.path.dirname(__file__), 'app', 'src', 'main', 'res')

img = Image.open(source_path).convert('RGBA')

# 1. 生成普通圆形图标（用于旧版Android和回退）
for density, size in SIZES.items():
    out_dir = os.path.join(output_base, f'mipmap-{density}')
    os.makedirs(out_dir, exist_ok=True)

    # 裁剪为正方形（取最短边居中裁剪）
    min_side = min(img.size)
    left = (img.width - min_side) // 2
    top = (img.height - min_side) // 2
    square = img.crop((left, top, left + min_side, top + min_side))

    # 缩放到目标尺寸
    resized = square.resize((size, size), Image.LANCZOS)

    # 创建圆形遮罩
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # 应用圆形遮罩
    result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    result.paste(resized, (0, 0), mask)

    # 保存为 PNG
    out_path = os.path.join(out_dir, 'ic_launcher.png')
    result.save(out_path, 'PNG')
    print(f'[OK] ic_launcher.png -> mipmap-{density} ({size}x{size})')

    # 也生成圆形版本
    out_path_round = os.path.join(out_dir, 'ic_launcher_round.png')
    result.save(out_path_round, 'PNG')
    print(f'[OK] ic_launcher_round.png -> mipmap-{density} ({size}x{size})')

# 2. 生成自适应图标的前景图（用于 Android 8+）
# 自适应图标背景用纯色（取图片主色调）
# 先缩略采样来获取主色
small = img.resize((32, 32), Image.LANCZOS)
pixels = list(small.getdata())
avg_r = sum(p[0] for p in pixels) // len(pixels)
avg_g = sum(p[1] for p in pixels) // len(pixels)
avg_b = sum(p[2] for p in pixels) // len(pixels)
bg_color = (avg_r, avg_g, avg_b)
print(f'[INFO] 自适应图标背景色: RGB({avg_r},{avg_g},{avg_b})')

# 生成自适应图标背景
for density, size in SIZES.items():
    bg = Image.new('RGBA', (size, size), bg_color)
    bg_dir = os.path.join(output_base, f'mipmap-{density}')
    bg.save(os.path.join(bg_dir, 'ic_launcher_background.png'), 'PNG')

# 生成自适应图标前景（缩小到72%放在108dp视口中央）
for density, size in SIZES.items():
    fg_size = int(size * 0.72)  # 前景占自适应图标的72%
    fg_dir = os.path.join(output_base, f'mipmap-{density}')

    # 从原始图片裁剪正方形并缩放到前景尺寸
    min_side = min(img.size)
    left = (img.width - min_side) // 2
    top = (img.height - min_side) // 2
    square = img.crop((left, top, left + min_side, top + min_side))
    fg_img = square.resize((fg_size, fg_size), Image.LANCZOS)

    # 创建圆形前景
    mask = Image.new('L', (fg_size, fg_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, fg_size, fg_size), fill=255)

    result = Image.new('RGBA', (fg_size, fg_size), (0, 0, 0, 0))
    result.paste(fg_img, (0, 0), mask)

    # 放在108dp视口中央
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    offset = (size - fg_size) // 2
    canvas.paste(result, (offset, offset), result)
    canvas.save(os.path.join(fg_dir, 'ic_launcher_foreground.png'), 'PNG')
    print(f'[OK] ic_launcher_foreground.png -> mipmap-{density} ({fg_size}x{fg_size})')

# 3. 删除临时的自适应图标xml，改用纯背景+前景方式
# 更新mipmap-anydpi-v26下的ic_launcher.xml
anydpi_dir = os.path.join(output_base, 'mipmap-anydpi-v26')
os.makedirs(anydpi_dir, exist_ok=True)

with open(os.path.join(anydpi_dir, 'ic_launcher.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n')
    f.write('    <background android:drawable="@mipmap/ic_launcher_background"/>\n')
    f.write('    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n')
    f.write('</adaptive-icon>\n')
print('[OK] 更新 adaptive-icon XML 配置')

# 还要生成一份到drawable目录（fallback）
drawable_dir = os.path.join(output_base, 'drawable')
os.makedirs(drawable_dir, exist_ok=True)
# 把xxhdpi的大小复制一份到drawable作为默认
default_size = SIZES['xxhdpi']
default_img_path = os.path.join(output_base, f'mipmap-xxhdpi', 'ic_launcher.png')
if os.path.exists(default_img_path):
    default_img = Image.open(default_img_path)
    default_img.save(os.path.join(drawable_dir, 'ic_launcher.png'), 'PNG')
    print(f'[OK] drawable/ic_launcher.png (fallback)')

print('\n=== 所有图标生成完毕！ ===')
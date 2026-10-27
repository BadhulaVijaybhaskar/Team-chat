#!/usr/bin/env python3
"""Generate Astra Loop brand SVG/PNG assets and install into Mattermost webapp paths.

Rerun from repo root:
  python3 astra-loop/brand/generate_assets.py
"""

from __future__ import annotations

import math
import shutil
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw

ROOT = Path('/workspace')
BRAND = ROOT / 'astra-loop' / 'brand'
SRC_JPG = Path('/opt/cursor/artifacts/assets/astra-loop-logo.jpg')
FONT_TTF = Path('/tmp/pjs/PlusJakartaSans-600.ttf')
WOFF2_SRC = Path('/tmp/pjs/woff2')
FONTS_DST = ROOT / 'webapp' / 'channels' / 'src' / 'fonts'
IMAGES = ROOT / 'webapp' / 'channels' / 'src' / 'images'
FAVICON_DIR = IMAGES / 'favicon'
API_FAVICON = ROOT / 'api' / 'v4' / 'html' / 'static' / 'favicon.ico'
SERVER_BOT = ROOT / 'server' / 'channels' / 'app' / 'users' / 'bot_default_icon.png'

BLUE = '#145CF6'
TEAL = '#09B5A4'
NAVY = '#0B1324'
WHITE = '#E8EDF5'
MENTION_RED = '#D24B4E'
UNREAD_AMBER = '#F5A623'


def lemniscate_points(a: float = 1.0, n: int = 360) -> list[tuple[float, float]]:
    """Bernoulli lemniscate samples for a continuous ∞ centerline."""
    pts: list[tuple[float, float]] = []
    for i in range(n + 1):
        t = (2 * math.pi * i / n) - (math.pi / 2)
        s = math.sin(t)
        c = math.cos(t)
        denom = 1 + s * s
        x = (a * c) / denom
        y = (a * s * c) / denom
        pts.append((x, y))
    return pts


def _normals(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    normals: list[tuple[float, float]] = []
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy) or 1.0
        normals.append((-dy / length, dx / length))
    return normals


def infinity_ribbon_path_d(cx: float, cy: float, scale: float, half_width: float) -> str:
    """Filled ribbon ∞ as a single closed polygon (parallel-curve offset)."""
    pts = lemniscate_points()
    norms = _normals(pts)
    left: list[tuple[float, float]] = []
    right: list[tuple[float, float]] = []
    for (x, y), (nx, ny) in zip(pts, norms):
        px, py = cx + x * scale, cy + y * scale
        left.append((px + nx * half_width, py + ny * half_width))
        right.append((px - nx * half_width, py - ny * half_width))
    poly = left + list(reversed(right))
    cmds = [f'M{poly[0][0]:.3f},{poly[0][1]:.3f}']
    cmds.extend(f'L{x:.3f},{y:.3f}' for x, y in poly[1:])
    cmds.append('Z')
    return ' '.join(cmds)


def infinity_svg_markup(
    view: int = 512,
    stroke_ratio: float = 0.13,
    gradient_id: str = 'astraInf',
) -> str:
    cx = cy = view / 2
    # Fit ∞ with padding for ribbon width
    scale = view * 0.34
    half_w = view * stroke_ratio * 0.5
    d = infinity_ribbon_path_d(cx, cy, scale, half_w)
    return f'''  <defs>
    <linearGradient id="{gradient_id}" x1="12%" y1="50%" x2="88%" y2="50%">
      <stop offset="0%" stop-color="{BLUE}"/>
      <stop offset="55%" stop-color="#1AA8E0"/>
      <stop offset="100%" stop-color="{TEAL}"/>
    </linearGradient>
  </defs>
  <path d="{d}" fill="url(#{gradient_id})"/>
'''


def text_to_svg_paths(text: str, font_path: Path, font_size: float, x: float, y: float, fill: str) -> tuple[str, float]:
    """Convert text to SVG path elements. Returns (markup, advance_width)."""
    font = TTFont(str(font_path))
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    units = font['head'].unitsPerEm
    scale = font_size / units
    # Baseline y is the text baseline
    cursor = 0.0
    parts: list[str] = []
    hmtx = font['hmtx'].metrics
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            cursor += font_size * 0.35
            continue
        pen = SVGPathPen(glyph_set)
        glyph_set[gname].draw(pen)
        raw = pen.getCommands()
        # Transform glyph path: scale, flip Y (font Y-up → SVG Y-down), translate
        transformed = transform_svg_path(raw, scale=scale, ox=x + cursor, oy=y)
        if transformed.strip():
            parts.append(f'<path fill="{fill}" d="{transformed}"/>')
        advance, _ = hmtx[gname]
        cursor += advance * scale
    return '\n    '.join(parts), cursor


def transform_svg_path(commands: str, scale: float, ox: float, oy: float) -> str:
    """Parse SVG path commands from SVGPathPen and apply scale + translate (Y flip)."""
    import re

    tokens = re.findall(r'[MmLlHhVvCcQqTtSsAaZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', commands)
    out: list[str] = []
    i = 0
    cmd = None
    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t
            out.append(cmd)
            i += 1
            continue
        # numbers follow current cmd
        assert cmd is not None
        if cmd in 'Zz':
            continue
        if cmd in 'Hh':
            x = float(t)
            out.append(f'{ox + x * scale:.3f}')
            i += 1
        elif cmd in 'Vv':
            y = float(t)
            out.append(f'{oy - y * scale:.3f}')
            i += 1
        elif cmd in 'Aa':
            # rx ry x-axis-rotation large-arc sweep x y
            nums = [float(tokens[i + k]) for k in range(7)]
            rx, ry, rot, large, sweep, x, y = nums
            out.extend([
                f'{rx * scale:.3f}',
                f'{ry * scale:.3f}',
                f'{rot:.3f}',
                f'{int(large)}',
                f'{int(sweep)}',
                f'{ox + x * scale:.3f}',
                f'{oy - y * scale:.3f}',
            ])
            i += 7
        else:
            # pairs x,y
            x = float(t)
            y = float(tokens[i + 1])
            out.append(f'{ox + x * scale:.3f}')
            out.append(f'{oy - y * scale:.3f}')
            i += 2
    return ' '.join(out)


def build_full_logo_svg(wordmark_fill: str, out_path: Path) -> None:
    # Layout: icon ~120 units tall, wordmark to the right
    icon_size = 120
    pad = 8
    font_size = 52
    # Icon occupies [0..icon_size], wordmark starts after gap
    gap = 18
    text_x = icon_size + gap
    # Baseline roughly vertically centered with icon
    text_y = icon_size * 0.66
    paths, text_w = text_to_svg_paths('Astra Loop', FONT_TTF, font_size, text_x, text_y, wordmark_fill)
    width = text_x + text_w + pad
    height = icon_size
    # Infinity in left square
    inf = infinity_svg_markup(view=icon_size, stroke_ratio=0.145, gradient_id='astraInfLogo')
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.2f} {height:.2f}" width="{width:.2f}" height="{height:.2f}" fill="none" role="img" aria-label="Astra Loop">
{inf}  <g>
    {paths}
  </g>
</svg>
'''
    out_path.write_text(svg)
    print(f'wrote {out_path} ({width:.0f}x{height:.0f})')


def build_icon_svg(out_path: Path, view: int = 512) -> None:
    inf = infinity_svg_markup(view=view, stroke_ratio=0.145, gradient_id='astraInfIcon')
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view} {view}" width="{view}" height="{view}" fill="none" role="img" aria-label="Astra Loop">
{inf}</svg>
'''
    out_path.write_text(svg)
    print(f'wrote {out_path}')


def svg_to_png(svg_path: Path, png_path: Path, width: int | None = None, height: int | None = None) -> None:
    """Rasterize SVG via CairoSVG (ImageMagick drops stroked paths)."""
    import cairosvg

    kwargs: dict = {'url': str(svg_path), 'write_to': str(png_path)}
    if width is not None:
        kwargs['output_width'] = width
    if height is not None:
        kwargs['output_height'] = height
    cairosvg.svg2png(**kwargs)
    im = Image.open(png_path).convert('RGBA')
    # Drop near-empty edge padding for full logos when only width set
    if width and not height:
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
            # scale back to requested width
            if im.width != width:
                nh = max(1, int(round(im.height * (width / im.width))))
                im = im.resize((width, nh), Image.Resampling.LANCZOS)
    im.save(png_path, 'PNG')


def remove_jpg_background(src: Path, dst: Path) -> None:
    """Fallback transparent PNG from source JPG (checkerboard removal)."""
    im = Image.open(src).convert('RGBA')
    pixels = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            mx, mn = max(r, g, b), min(r, g, b)
            # Light gray / white checkerboard & dotted swirl
            if mn > 175 and (mx - mn) < 28:
                pixels[x, y] = (0, 0, 0, 0)
                continue
            # Near-white faint dots
            if mn > 205 and (mx - mn) < 20:
                pixels[x, y] = (0, 0, 0, 0)
    # Crop to content
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    im.save(dst, 'PNG')
    print(f'wrote bg-removed reference {dst} size={im.size}')


def tint_icon(im: Image.Image, rgb: tuple[int, int, int], strength: float = 0.35) -> Image.Image:
    """Blend non-transparent pixels toward a tint (unread style)."""
    out = im.copy().convert('RGBA')
    px = out.load()
    w, h = out.size
    tr, tg, tb = rgb
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            nr = int(r * (1 - strength) + tr * strength)
            ng = int(g * (1 - strength) + tg * strength)
            nb = int(b * (1 - strength) + tb * strength)
            px[x, y] = (nr, ng, nb, a)
    return out


def add_badge(im: Image.Image, color: tuple[int, int, int], frac: float = 0.28) -> Image.Image:
    """Add a circular badge in the bottom-right (mentions style)."""
    out = im.copy().convert('RGBA')
    w, h = out.size
    r = max(2, int(min(w, h) * frac))
    cx = w - r - max(1, w // 16)
    cy = h - r - max(1, h // 16)
    overlay = Image.new('RGBA', out.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*color, 255))
    # subtle white ring
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 220), width=max(1, r // 5))
    return Image.alpha_composite(out, overlay)


def write_ico(images: list[Image.Image], path: Path) -> None:
    """Write a multi-size ICO file."""
    imgs = [im.convert('RGBA') for im in images]
    # Pillow embeds each requested size from the largest source image.
    largest = max(imgs, key=lambda im: im.width)
    sizes = [(im.width, im.height) for im in imgs]
    largest.save(path, format='ICO', sizes=sizes)
    print(f'wrote {path}')


def install_fonts() -> list[Path]:
    FONTS_DST.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    mapping = {
        400: 'PlusJakartaSans-Regular.woff2',
        500: 'PlusJakartaSans-Medium.woff2',
        600: 'PlusJakartaSans-SemiBold.woff2',
        700: 'PlusJakartaSans-Bold.woff2',
    }
    for weight, name in mapping.items():
        src = WOFF2_SRC / f'plus-jakarta-sans-latin-{weight}-normal.woff2'
        dst = FONTS_DST / name
        shutil.copy2(src, dst)
        written.append(dst)
        print(f'font {dst}')
    # OFL notice
    ofl_src = Path('/tmp/pjs/OFL.txt')
    if ofl_src.exists():
        dst = FONTS_DST / 'PlusJakartaSans-OFL.txt'
        shutil.copy2(ofl_src, dst)
        written.append(dst)
    return written


def update_typography_scss() -> Path:
    """Append Plus Jakarta Sans @font-face blocks if missing."""
    scss = ROOT / 'webapp' / 'channels' / 'src' / 'sass' / 'base' / '_typography.scss'
    text = scss.read_text()
    marker = "font-family: 'Plus Jakarta Sans'"
    if marker in text:
        print('typography already has Plus Jakarta Sans')
        return scss
    block = """

// Plus Jakarta Sans (Astra Loop brand)
@font-face {
    font-family: 'Plus Jakarta Sans';
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url('../fonts/PlusJakartaSans-Regular.woff2') format('woff2');
}

@font-face {
    font-family: 'Plus Jakarta Sans';
    font-style: normal;
    font-weight: 500;
    font-display: swap;
    src: url('../fonts/PlusJakartaSans-Medium.woff2') format('woff2');
}

@font-face {
    font-family: 'Plus Jakarta Sans';
    font-style: normal;
    font-weight: 600;
    font-display: swap;
    src: url('../fonts/PlusJakartaSans-SemiBold.woff2') format('woff2');
}

@font-face {
    font-family: 'Plus Jakarta Sans';
    font-style: normal;
    font-weight: 700;
    font-display: swap;
    src: url('../fonts/PlusJakartaSans-Bold.woff2') format('woff2');
}
"""
    scss.write_text(text.rstrip() + '\n' + block)
    print(f'updated {scss}')
    return scss


def resize_contain(im: Image.Image, size: tuple[int, int], bg: tuple[int, int, int, int] | None = None) -> Image.Image:
    canvas = Image.new('RGBA', size, bg or (0, 0, 0, 0))
    fitted = im.copy()
    fitted.thumbnail(size, Image.Resampling.LANCZOS)
    x = (size[0] - fitted.width) // 2
    y = (size[1] - fitted.height) // 2
    canvas.paste(fitted, (x, y), fitted)
    return canvas


def main() -> None:
    BRAND.mkdir(parents=True, exist_ok=True)

    # --- SVG masters ---
    logo_svg = BRAND / 'astra-loop-logo.svg'
    logo_white_svg = BRAND / 'astra-loop-logo-white.svg'
    icon_svg = BRAND / 'astra-loop-icon.svg'
    build_full_logo_svg(NAVY, logo_svg)
    build_full_logo_svg(WHITE, logo_white_svg)
    build_icon_svg(icon_svg, view=512)

    # Reference bg-removed JPG
    if SRC_JPG.exists():
        remove_jpg_background(SRC_JPG, BRAND / 'astra-loop-logo-from-jpg.png')

    # --- Raster from SVG ---
    logo_png = BRAND / 'astra-loop-logo-transparent.png'
    logo_white_png = BRAND / 'astra-loop-logo-white.png'
    icon_png = BRAND / 'astra-loop-icon.png'
    svg_to_png(logo_svg, logo_png, width=930)
    svg_to_png(logo_white_svg, logo_white_png, width=438)
    svg_to_png(icon_svg, icon_png, width=512, height=512)

    # Extra icon sizes in brand/
    for s in (256, 192, 128, 64, 50, 32, 16):
        svg_to_png(icon_svg, BRAND / f'astra-loop-icon-{s}.png', width=s, height=s)

    # --- Install into Mattermost image paths (keep filenames) ---
    shutil.copy2(logo_svg, IMAGES / 'logo.svg')

    # logo.png historically 465x91; logoWhite 219x36
    svg_to_png(logo_svg, IMAGES / 'logo.png', width=465)
    svg_to_png(logo_white_svg, IMAGES / 'logoWhite.png', width=219)

    # Email logos
    svg_to_png(logo_svg, IMAGES / 'logo-email.png', width=288)
    # blue email: recolor wordmark isn't needed — use full logo (gradient icon + navy text)
    svg_to_png(logo_svg, IMAGES / 'logo_email_blue.png', width=264)
    svg_to_png(logo_svg, IMAGES / 'logo_email_dark.png', width=264)
    # gray: render white logo then tint gray, or build gray wordmark
    gray_svg = BRAND / 'astra-loop-logo-gray.svg'
    build_full_logo_svg('#787878', gray_svg)
    svg_to_png(gray_svg, IMAGES / 'logo_email_gray.png', width=132)

    # Bot / icons — infinity only
    bot = resize_contain(Image.open(icon_png).convert('RGBA'), (256, 256))
    bot.save(IMAGES / 'bot_default_icon.png')
    SERVER_BOT.parent.mkdir(parents=True, exist_ok=True)
    bot.save(SERVER_BOT)
    resize_contain(Image.open(icon_png).convert('RGBA'), (50, 50)).save(IMAGES / 'icon50x50.png')
    resize_contain(Image.open(icon_png).convert('RGBA'), (64, 64)).save(IMAGES / 'icon64x64.png')

    # Favicons from infinity
    FAVICON_DIR.mkdir(parents=True, exist_ok=True)
    base512 = Image.open(icon_png).convert('RGBA')
    sizes = [16, 24, 32, 64, 96]
    for s in sizes:
        base = resize_contain(base512, (s, s))
        base.save(FAVICON_DIR / f'favicon-default-{s}x{s}.png')
        tint_icon(base, tuple(int(UNREAD_AMBER[i:i+2], 16) for i in (1, 3, 5)), 0.4).save(
            FAVICON_DIR / f'favicon-unread-{s}x{s}.png'
        )
        add_badge(base, tuple(int(MENTION_RED[i:i+2], 16) for i in (1, 3, 5))).save(
            FAVICON_DIR / f'favicon-mentions-{s}x{s}.png'
        )

    # Generic favicon-* and apple/android
    for s, name in [
        (16, 'favicon-16x16.png'),
        (32, 'favicon-32x32.png'),
        (96, 'favicon-96x96.png'),
        (192, 'android-chrome-192x192.png'),
    ]:
        resize_contain(base512, (s, s)).save(FAVICON_DIR / name)

    for s in (57, 60, 72, 76, 120, 144, 152):
        resize_contain(base512, (s, s)).save(FAVICON_DIR / f'apple-touch-icon-{s}x{s}.png')

    # API favicon.ico
    ico_imgs = [resize_contain(base512, (s, s)) for s in (16, 32, 48, 64)]
    write_ico(ico_imgs, API_FAVICON)

    # Fonts
    install_fonts()
    update_typography_scss()

    print('done')


if __name__ == '__main__':
    main()

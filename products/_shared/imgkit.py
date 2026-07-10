"""Shared image-generation toolkit for MacroDigitalCo Etsy listing marketing images."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 2000
TEAL = (15, 122, 115)
TEAL_DARK = (10, 74, 70)
NAVY = (27, 58, 92)
NAVY_DARK = (14, 28, 46)
CREAM = (247, 244, 238)
WHITE = (255, 255, 255)
GOLD = (201, 162, 90)
MUTED = (110, 120, 118)
DARKBG = (26, 26, 26)
DARKBG2 = (18, 18, 18)

import os as _os


def _first_existing(paths):
    for p in paths:
        if _os.path.exists(p):
            return p
    return paths[-1]


FB = _first_existing([
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
])
FR = _first_existing([
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
])
FI = _first_existing([
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
    "C:/Windows/Fonts/ariali.ttf",
])


def font(path, size):
    return ImageFont.truetype(path, size)


def grad_bg(w, h, top, bottom, horizontal=False):
    img = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(img)
    if not horizontal:
        for y in range(h):
            t = y / h
            r = int(top[0] + (bottom[0] - top[0]) * t)
            g = int(top[1] + (bottom[1] - top[1]) * t)
            b = int(top[2] + (bottom[2] - top[2]) * t)
            d.line([(0, y), (w, y)], fill=(r, g, b))
    else:
        for x in range(w):
            t = x / w
            r = int(top[0] + (bottom[0] - top[0]) * t)
            g = int(top[1] + (bottom[1] - top[1]) * t)
            b = int(top[2] + (bottom[2] - top[2]) * t)
            d.line([(x, 0), (x, h)], fill=(r, g, b))
    return img


def centered_text(d, text, fnt, cx, y, fill, anchor="mm"):
    d.text((cx, y), text, font=fnt, fill=fill, anchor=anchor)


def wrap_text(d, text, fnt, max_w):
    words = text.split()
    lines = []
    line = ""
    for w_ in words:
        test = (line + " " + w_).strip()
        if d.textlength(test, font=fnt) > max_w and line:
            lines.append(line)
            line = w_
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def badge(base, cx, cy, text, bg=GOLD, fg=(40, 30, 10), fnt=None, pad=22):
    fnt = fnt or font(FB, 34)
    bbox = ImageDraw.Draw(base).textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    w, h = tw + pad * 2, th + pad * 1.6
    x0, y0 = cx - w / 2, cy - h / 2
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h / 2, fill=bg)
    d.text((cx, cy - 2), text, font=fnt, fill=fg, anchor="mm")


def draw_icon(d, kind, cx, cy, r=55, teal=TEAL, fg=WHITE):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=teal)
    c = fg
    if kind == "edit":
        d.line([cx - 20, cy + 20, cx + 22, cy - 22], fill=c, width=8)
        d.polygon([(cx + 22, cy - 22), (cx + 32, cy - 12), (cx + 22, cy - 2)], fill=c)
        d.line([cx - 26, cy + 26, cx - 14, cy + 14], fill=c, width=8)
    elif kind == "swap":
        d.arc([cx - 26, cy - 26, cx + 26, cy + 10], start=200, end=340, fill=c, width=7)
        d.polygon([(cx + 22, cy - 22), (cx + 34, cy - 14), (cx + 20, cy - 6)], fill=c)
        d.arc([cx - 26, cy - 10, cx + 26, cy + 26], start=20, end=160, fill=c, width=7)
        d.polygon([(cx - 22, cy + 22), (cx - 34, cy + 14), (cx - 20, cy + 6)], fill=c)
    elif kind == "page":
        d.rounded_rectangle([cx - 20, cy - 28, cx + 20, cy + 28], radius=4, outline=c, width=6)
        d.line([cx - 10, cy - 10, cx + 10, cy - 10], fill=c, width=4)
        d.line([cx - 10, cy, cx + 10, cy], fill=c, width=4)
        d.line([cx - 10, cy + 10, cx + 4, cy + 10], fill=c, width=4)
    elif kind == "download":
        d.line([cx, cy - 26, cx, cy + 12], fill=c, width=8)
        d.polygon([(cx - 18, cy - 2), (cx + 18, cy - 2), (cx, cy + 18)], fill=c)
        d.line([cx - 24, cy + 26, cx + 24, cy + 26], fill=c, width=8)
    elif kind == "shield":
        d.polygon([(cx, cy - 28), (cx + 24, cy - 16), (cx + 24, cy + 8), (cx, cy + 30), (cx - 24, cy + 8), (cx - 24, cy - 16)], outline=c, width=6)
        d.line([cx - 10, cy, cx - 2, cy + 10], fill=c, width=6)
        d.line([cx - 2, cy + 10, cx + 14, cy - 8], fill=c, width=6)
    elif kind == "palette":
        d.ellipse([cx - 24, cy - 20, cx + 24, cy + 24], fill=None, outline=c, width=6)
        for dx, dy in [(-10, -8), (10, -10), (14, 8), (-6, 12)]:
            d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5], fill=c)
    elif kind == "chart":
        d.line([cx - 24, cy + 26, cx - 24, cy - 4], fill=c, width=9)
        d.line([cx, cy + 26, cx, cy - 18], fill=c, width=9)
        d.line([cx + 24, cy + 26, cx + 24, cy + 8], fill=c, width=9)
        d.line([cx - 30, cy + 26, cx + 30, cy + 26], fill=c, width=6)
    elif kind == "calendar":
        d.rounded_rectangle([cx - 26, cy - 22, cx + 26, cy + 26], radius=6, outline=c, width=6)
        d.line([cx - 26, cy - 6, cx + 26, cy - 6], fill=c, width=5)
        d.line([cx - 12, cy - 28, cx - 12, cy - 16], fill=c, width=5)
        d.line([cx + 12, cy - 28, cx + 12, cy - 16], fill=c, width=5)
    elif kind == "check":
        d.rounded_rectangle([cx - 26, cy - 26, cx + 26, cy + 26], radius=8, outline=c, width=6)
        d.line([cx - 12, cy + 2, cx - 2, cy + 14], fill=c, width=7)
        d.line([cx - 2, cy + 14, cx + 16, cy - 12], fill=c, width=7)
    elif kind == "brain":
        d.ellipse([cx - 26, cy - 24, cx + 26, cy + 24], outline=c, width=6)
        d.line([cx, cy - 24, cx, cy + 24], fill=c, width=4)
        d.arc([cx - 24, cy - 16, cx + 4, cy + 10], start=0, end=180, fill=c, width=4)
        d.arc([cx - 4, cy - 16, cx + 24, cy + 10], start=0, end=180, fill=c, width=4)
    elif kind == "clock":
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=c, width=6)
        d.line([cx, cy, cx, cy - 16], fill=c, width=5)
        d.line([cx, cy, cx + 14, cy + 6], fill=c, width=5)
    elif kind == "heart":
        d.pieslice([cx - 24, cy - 22, cx, cy + 2], start=180, end=360, fill=c)
        d.pieslice([cx, cy - 22, cx + 24, cy + 2], start=180, end=360, fill=c)
        d.polygon([(cx - 24, cy - 6), (cx + 24, cy - 6), (cx, cy + 26)], fill=c)
    elif kind == "moon":
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=c)
        d.ellipse([cx - 12, cy - 28, cx + 30, cy + 20], fill=teal)
    elif kind == "gradebook":
        d.rounded_rectangle([cx - 26, cy - 26, cx + 26, cy + 26], radius=4, outline=c, width=5)
        d.line([cx - 26, cy - 8, cx + 26, cy - 8], fill=c, width=4)
        d.line([cx - 26, cy + 8, cx + 26, cy + 8], fill=c, width=4)
        d.line([cx - 8, cy - 26, cx - 8, cy + 26], fill=c, width=4)
    elif kind == "book":
        d.line([cx, cy - 22, cx, cy + 24], fill=c, width=5)
        d.arc([cx - 30, cy - 22, cx + 2, cy + 26], start=270, end=90, fill=c, width=6)
        d.arc([cx - 2, cy - 22, cx + 30, cy + 26], start=90, end=270, fill=c, width=6)
    elif kind == "target":
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=c, width=5)
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=c, width=5)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=c)


def _drop_shadow(w, h, blur=28, opacity=110):
    shadow = Image.new("RGBA", (w + blur * 4, h + blur * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    d.rounded_rectangle([blur * 2, blur * 2, blur * 2 + w, blur * 2 + h], radius=18, fill=(0, 0, 0, opacity))
    return shadow.filter(ImageFilter.GaussianBlur(blur / 2))


def _paste_page(base, page_img, cx, cy, target_w, angle=0):
    ratio = target_w / page_img.width
    target_h = int(page_img.height * ratio)
    pg = page_img.convert("RGBA").resize((target_w, target_h), Image.LANCZOS)
    border = Image.new("RGBA", (target_w + 6, target_h + 6), (255, 255, 255, 255))
    border.paste(pg, (3, 3))
    shadow = _drop_shadow(border.width, border.height, blur=22, opacity=95)
    if angle:
        border = border.rotate(angle, expand=True, resample=Image.BICUBIC)
        shadow = shadow.rotate(angle, expand=True, resample=Image.BICUBIC)
    sx = int(cx - shadow.width / 2)
    sy = int(cy - shadow.height / 2) + 10
    base.paste(shadow, (sx, sy), shadow)
    bx = int(cx - border.width / 2)
    by = int(cy - border.height / 2)
    base.paste(border, (bx, by), border)


def build_flatlay_cover(page_images, title, subtitle_lines, badge_text, outpath,
                         accent=TEAL, accent_dark=TEAL_DARK, bg_top=CREAM,
                         bg_bottom=(233, 228, 216), title_color=None, sub_color=None):
    """Realistic-feeling mockup: actual rendered product pages fanned out with drop shadows,
    a title banner on top and a badge at the bottom. page_images: list of PIL Image (2-4)."""
    img = grad_bg(W, H, bg_top, bg_bottom).convert("RGBA")
    d = ImageDraw.Draw(img)
    title_color = title_color or accent_dark
    sub_color = sub_color or MUTED

    band_h = 430
    d.rectangle([0, 0, W, band_h], fill=accent_dark)
    d.rectangle([0, band_h - 6, W, band_h], fill=GOLD)

    ty = 130
    for ln in title.split("\n"):
        centered_text(d, ln, font(FB, 82), W / 2, ty, WHITE)
        ty += 92
    sy = ty + 20
    for sl in subtitle_lines:
        centered_text(d, sl, font(FR, 34), W / 2, sy, (225, 230, 235))
        sy += 46

    n = len(page_images)
    layout = {
        2: [(-16, W * 0.34, 1230, 760), (14, W * 0.66, 1290, 760)],
        3: [(-18, W * 0.24, 1200, 700), (0, W * 0.5, 1300, 760), (18, W * 0.76, 1200, 700)],
        4: [(-20, W * 0.20, 1120, 620), (-7, W * 0.42, 1260, 700), (7, W * 0.62, 1260, 700), (20, W * 0.82, 1120, 620)],
    }
    positions = layout.get(n, layout[3])
    for (angle, cx, cy, tw), pg in zip(positions, page_images):
        _paste_page(img, pg, cx, cy, int(tw), angle=angle)

    if badge_text:
        badge(img, W / 2, H - 130, badge_text, bg=GOLD, fg=(40, 30, 10), fnt=font(FB, 40))
    centered_text(d, "MacroDigitalCo", font(FI, 32), W / 2, H - 50, sub_color)

    img.convert("RGB").save(outpath, quality=94)


def build_cover(title, subtitle_lines, badge_text, outpath, accent=TEAL, accent_dark=TEAL_DARK,
                 bg_top=CREAM, bg_bottom=(233, 228, 216), title_color=None, dark_mode=False,
                 sub_color=None, tag=None):
    img = grad_bg(W, H, bg_top, bg_bottom).convert("RGBA")
    d = ImageDraw.Draw(img)
    title_color = title_color or accent_dark
    sub_color = sub_color or MUTED

    if tag:
        badge(img, W / 2, 190, tag, bg=accent, fg=WHITE, fnt=font(FB, 30))

    margin = 90
    d.rectangle([margin, margin, W - margin, H - margin], outline=accent, width=4)
    d.rectangle([margin + 18, margin + 18, W - margin - 18, H - margin - 18], outline=GOLD, width=2)

    ty = 620
    title_font = font(FB, 108)
    lines = title.split("\n")
    for ln in lines:
        centered_text(d, ln, title_font, W / 2, ty, title_color)
        ty += 122

    d.line([(W / 2 - 300, ty + 10), (W / 2 + 300, ty + 10)], fill=GOLD, width=6)

    sy = ty + 90
    for sl in subtitle_lines:
        centered_text(d, sl, font(FR, 40), W / 2, sy, sub_color)
        sy += 56

    icon_y = 1500
    icons = ["calendar", "check", "book", "target", "chart", "edit"]
    spacing = 260
    start_x = W / 2 - spacing * (len(icons) - 1) / 2
    for i, ic in enumerate(icons):
        draw_icon(d, ic, start_x + i * spacing, icon_y, r=50, teal=accent, fg=WHITE if not dark_mode else DARKBG)

    if badge_text:
        badge(img, W / 2, 1760, badge_text, bg=GOLD, fg=(40, 30, 10), fnt=font(FB, 40))

    centered_text(d, "MacroDigitalCo", font(FI, 34), W / 2, 1900, sub_color)

    img.convert("RGB").save(outpath, quality=92)


def build_customizable(title, subtitle, feats, outpath, accent=TEAL, accent_dark=TEAL_DARK,
                        bg_top=CREAM, bg_bottom=(233, 228, 216), card_bg=WHITE, text_color=None,
                        body_color=MUTED, card_outline=(220, 214, 200)):
    img = grad_bg(W, H, bg_top, bg_bottom).convert("RGBA")
    d = ImageDraw.Draw(img)
    text_color = text_color or accent_dark

    centered_text(d, title, font(FB, 88), W / 2, 200, text_color)
    centered_text(d, subtitle, font(FI, 36), W / 2, 280, body_color)
    d.line([(W / 2 - 260, 330), (W / 2 + 260, 330)], fill=GOLD, width=6)

    cols = 2
    col_w = 880
    row_h = 300
    start_x = (W - (col_w * cols + 80)) / 2
    start_y = 440
    head_font = font(FB, 38)
    body_font = font(FR, 29)

    for i, (icon, head, body) in enumerate(feats):
        col = i % cols
        row = i // cols
        x = start_x + col * (col_w + 80)
        y = start_y + row * row_h

        d.rounded_rectangle([x, y, x + col_w, y + row_h - 40], radius=24, fill=card_bg, outline=card_outline, width=2)
        cx = x + 100
        cy = y + (row_h - 40) / 2
        draw_icon(d, icon, cx, cy, teal=accent)

        tx = x + 190
        d.text((tx, y + 55), head, font=head_font, fill=text_color, anchor="lm")
        lines = wrap_text(d, body, body_font, col_w - 220)
        ly = y + 105
        for ln in lines:
            d.text((tx, ly), ln, font=body_font, fill=body_color, anchor="lm")
            ly += 40

    img.convert("RGB").save(outpath, quality=92)


def build_bonus_slide(items, outpath, footer="Questions before or after buying? Message us anytime.",
                       bg_top=NAVY, bg_bottom=(14, 30, 48), title_color=WHITE,
                       item_color=(235, 238, 242), footer_color=(170, 185, 200), accent=GOLD,
                       check_fg=None):
    img = grad_bg(W, H, bg_top, bg_bottom).convert("RGBA")
    d = ImageDraw.Draw(img)
    check_fg = check_fg or bg_top

    centered_text(d, "YOU WILL GET", font(FB, 90), W / 2, 170, title_color)
    d.line([(W / 2 - 220, 245), (W / 2 + 220, 245)], fill=accent, width=6)

    y = 340
    item_font = font(FR, 36)
    for it in items:
        d.ellipse([180, y - 28, 240, y + 32], fill=accent)
        d.line([193, y + 2, 208, y + 17], fill=check_fg, width=6)
        d.line([208, y + 17, 228, y - 14], fill=check_fg, width=6)
        lines = wrap_text(d, it, item_font, W - 280 - 160)
        ty = y - (len(lines) - 1) * 24
        lx = 280
        for ln in lines:
            d.text((lx, ty), ln, font=item_font, fill=item_color, anchor="lm")
            ty += 48
        y += 105 if len(lines) == 1 else 105 + (len(lines) - 1) * 48

    centered_text(d, footer, font(FI, 32), W / 2, y + 30, footer_color)

    img.convert("RGB").save(outpath, quality=92)

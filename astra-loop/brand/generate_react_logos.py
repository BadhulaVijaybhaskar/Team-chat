#!/usr/bin/env python3
"""Emit React SVG logo components from brand SVG masters."""

from __future__ import annotations

import re
from pathlib import Path

BRAND = Path('/workspace/astra-loop/brand')
COMP = Path('/workspace/webapp/channels/src/components/common/svg_images_components')
ICON_COMP = Path('/workspace/webapp/channels/src/components/widgets/icons/mattermost_logo.tsx')


def parse_logo(svg_text: str) -> tuple[str, str, list[str], str]:
    vb = re.search(r'viewBox="([^"]+)"', svg_text).group(1)
    paths = re.findall(r'<path\s+([^>]+?)\s*/>', svg_text)
    inf_d = ''
    glyphs: list[str] = []
    fill = '#0B1324'
    for attrs in paths:
        d_m = re.search(r'd="([^"]*)"', attrs)
        fill_m = re.search(r'fill="([^"]+)"', attrs)
        d = d_m.group(1) if d_m else ''
        f = fill_m.group(1) if fill_m else ''
        if not d.strip():
            continue
        if f.startswith('url(') or (not inf_d and 'url' in attrs):
            inf_d = d
        else:
            glyphs.append(d)
            fill = f
    return vb, inf_d, glyphs, fill


def write_logo_tsx(
    filename: str,
    svg_path: Path,
    gradient_id: str,
    default_w: str,
    default_h: str,
) -> None:
    vb, inf_d, glyphs, fill = parse_logo(svg_path.read_text())
    glyph_jsx = '\n'.join(
        f"        <path\n            fill='{fill}'\n            d='{d}'\n        />"
        for d in glyphs
    )
    fill_url = f"url(#{gradient_id})"
    content = f"""// Copyright (c) 2015-present Mattermost, Inc. All Rights Reserved.
// See LICENSE.txt for license information.

import React from 'react';
import styled from 'styled-components';

type Props = {{
    width?: number;
    height?: number;
    className?: string;
}};

const Svg = styled.svg.attrs({{
    version: '1.1',
    xmlns: 'http://www.w3.org/2000/svg',
    xmlnsXlink: 'http://www.w3.org/1999/xlink',
}})``;

export default (props: Props) => (
    <Svg
        className={{props.className}}
        width={{props.width ? props.width.toString() : '{default_w}'}}
        height={{props.height ? props.height.toString() : '{default_h}'}}
        viewBox='{vb}'
        fill='none'
        xmlns='http://www.w3.org/2000/svg'
        role='img'
        aria-label='Astra Loop'
    >
        <defs>
            <linearGradient
                id='{gradient_id}'
                x1='12%'
                y1='50%'
                x2='88%'
                y2='50%'
            >
                <stop
                    offset='0%'
                    stopColor='#145CF6'
                />
                <stop
                    offset='55%'
                    stopColor='#1AA8E0'
                />
                <stop
                    offset='100%'
                    stopColor='#09B5A4'
                />
            </linearGradient>
        </defs>
        <path
            d='{inf_d}'
            fill='{fill_url}'
        />
{glyph_jsx}
    </Svg>
);
"""
    out = COMP / filename
    out.write_text(content)
    print(f'wrote {out} ({out.stat().st_size} bytes)')


def write_mattermost_logo() -> None:
    icon = (BRAND / 'astra-loop-icon.svg').read_text()
    icon_d = re.search(r'<path d="([^"]+)"', icon).group(1)
    content = f"""// Copyright (c) 2015-present Mattermost, Inc. All Rights Reserved.
// See LICENSE.txt for license information.

import React from 'react';
import type {{CSSProperties}} from 'react';
import {{useIntl}} from 'react-intl';

export default function MattermostLogo(props: React.HTMLAttributes<HTMLSpanElement>) {{
    const {{formatMessage}} = useIntl();
    return (
        <span {{...props}}>
            <svg
                version='1.1'
                x='0px'
                y='0px'
                viewBox='0 0 512 512'
                role='img'
                aria-label={{formatMessage({{id: 'generic_icons.mattermost', defaultMessage: 'Astra Loop Logo'}})}}
            >
                <defs>
                    <linearGradient
                        id='astraInfMmLogo'
                        x1='12%'
                        y1='50%'
                        x2='88%'
                        y2='50%'
                    >
                        <stop
                            offset='0%'
                            stopColor='#145CF6'
                        />
                        <stop
                            offset='55%'
                            stopColor='#1AA8E0'
                        />
                        <stop
                            offset='100%'
                            stopColor='#09B5A4'
                        />
                    </linearGradient>
                </defs>
                <path
                    style={{style}}
                    fill='url(#astraInfMmLogo)'
                    d='{icon_d}'
                />
            </svg>
        </span>
    );
}}

const style: CSSProperties = {{
    fillRule: 'evenodd',
    clipRule: 'evenodd',
}};
"""
    ICON_COMP.write_text(content)
    print(f'wrote {ICON_COMP} ({ICON_COMP.stat().st_size} bytes)')


def clean_empty_paths() -> None:
    for name in [
        'astra-loop-logo.svg',
        'astra-loop-logo-white.svg',
        'astra-loop-logo-gray.svg',
    ]:
        p = BRAND / name
        t = p.read_text()
        t2 = re.sub(r'\s*<path fill="[^"]+" d=""/>\n?', '\n', t)
        p.write_text(t2)
    lp = Path('/workspace/webapp/channels/src/images/logo.svg')
    if lp.exists():
        t = lp.read_text()
        lp.write_text(re.sub(r'\s*<path fill="[^"]+" d=""/>\n?', '\n', t))


def main() -> None:
    clean_empty_paths()
    write_logo_tsx(
        'logo_dark_blue_svg.tsx',
        BRAND / 'astra-loop-logo.svg',
        'astraInfLogoDark',
        '209',
        '60',
    )
    write_logo_tsx(
        'logo_white_svg.tsx',
        BRAND / 'astra-loop-logo-white.svg',
        'astraInfLogoWhite',
        '209',
        '60',
    )
    write_mattermost_logo()
    # Keep webapp logo.svg in sync with cleaned brand master
    Path('/workspace/webapp/channels/src/images/logo.svg').write_text(
        (BRAND / 'astra-loop-logo.svg').read_text()
    )


if __name__ == '__main__':
    main()

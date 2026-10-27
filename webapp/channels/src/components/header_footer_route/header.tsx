// Copyright (c) 2015-present Mattermost, Inc. All Rights Reserved.
// See LICENSE.txt for license information.

import classNames from 'classnames';
import React, {useEffect, useState} from 'react';
import {useSelector} from 'react-redux';
import {Link} from 'react-router-dom';

import {getConfig, getLicense} from 'mattermost-redux/selectors/entities/general';

import BackButton from 'components/common/back_button';
import Logo from 'components/common/svg_images_components/logo_dark_blue_svg';
import LogoWhite from 'components/common/svg_images_components/logo_white_svg';

import './header.scss';
import {LicenseSkus} from 'utils/constants';

export type HeaderProps = {
    alternateLink?: React.ReactElement<any>;
    backButtonURL?: string;
    onBackButtonClick?: React.EventHandler<React.MouseEvent>;
};

const DEFAULT_SITE_NAMES = new Set(['Mattermost', 'Astra Loop']);

function usePrefersDarkScheme(): boolean {
    const [prefersDark, setPrefersDark] = useState(() => {
        if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
            return false;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    });

    useEffect(() => {
        if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
            return undefined;
        }
        const media = window.matchMedia('(prefers-color-scheme: dark)');
        const onChange = (event: MediaQueryListEvent) => setPrefersDark(event.matches);
        media.addEventListener('change', onChange);
        setPrefersDark(media.matches);
        return () => media.removeEventListener('change', onChange);
    }, []);

    return prefersDark;
}

const Header = ({alternateLink, backButtonURL, onBackButtonClick}: HeaderProps) => {
    const {SiteName} = useSelector(getConfig);
    const license = useSelector(getLicense);
    const prefersDark = usePrefersDarkScheme();
    const BrandLogo = prefersDark ? LogoWhite : Logo;

    const ariaLabel = SiteName || 'Astra Loop';

    // Free/entry installs show the logo only — no TEAM/ENTRY EDITION badges.
    let freeBanner = null;
    if (license.IsLicensed === 'false' || license.SkuShortName === LicenseSkus.Entry) {
        freeBanner = <BrandLogo/>;
    }

    let title: React.ReactNode = SiteName;
    if (typeof title === 'string' && DEFAULT_SITE_NAMES.has(title)) {
        if (freeBanner) {
            title = '';
        } else {
            title = <BrandLogo/>;
        }
    }

    return (
        <div
            data-testid='hfroute-header'
            className={classNames('hfroute-header', {'has-free-banner': freeBanner, 'has-custom-site-name': title})}
        >
            <div className='header-main'>
                <div>
                    {freeBanner &&
                        <Link
                            data-testid='header-logo-link'
                            className='header-logo-link'
                            to='/'
                            aria-label={ariaLabel}
                        >
                            {freeBanner}
                        </Link>
                    }
                    {title &&
                        <Link
                            data-testid='header-logo-link'
                            className='header-logo-link'
                            to='/'
                            aria-label={ariaLabel}
                        >
                            {title}
                        </Link>
                    }
                </div>
                {alternateLink}
            </div>
            {onBackButtonClick && (
                <BackButton
                    className='header-back-button'
                    url={backButtonURL}
                    onClick={onBackButtonClick}
                />
            )}
        </div>
    );
};

export default Header;

// Copyright (c) 2015-present Mattermost, Inc. All Rights Reserved.
// See LICENSE.txt for license information.

import React, {type JSX} from 'react';

import LogoWhite from 'components/common/svg_images_components/logo_white_svg';

const ProductBrandingFreeEdition = (): JSX.Element => {
    return (
        <span className='globalHeader-leftControls-productBranding-freeEdition'>
            <LogoWhite
                className='globalHeader-leftControls-productBranding-freeEdition-logo'
                width={116}
                height={20}
            />
        </span>
    );
};

export default ProductBrandingFreeEdition;

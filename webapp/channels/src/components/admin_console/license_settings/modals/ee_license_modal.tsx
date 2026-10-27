// Copyright (c) 2015-present Mattermost, Inc. All Rights Reserved.
// See LICENSE.txt for license information.

import React, {type JSX} from 'react';
import {useSelector, useDispatch} from 'react-redux';

import {GenericModal} from '@mattermost/components';
import {Button} from '@mattermost/shared/components/button';

import {closeModal} from 'actions/views/modals';
import {isModalOpen} from 'selectors/views/modals';

import {ModalIdentifiers} from 'utils/constants';

import type {GlobalState} from 'types/store';

import './ee_license_modal.scss';

type Props = {
    onClose?: () => void;
};

const EELicenseModal: React.FC<Props> = (props: Props): JSX.Element | null => {
    const dispatch = useDispatch();

    const show = useSelector((state: GlobalState) => isModalOpen(state, ModalIdentifiers.ENTERPRISE_EDITION_LICENSE));
    if (!show) {
        return null;
    }

    const handleOnClose = () => {
        if (props.onClose) {
            props.onClose();
        }
        dispatch(closeModal(ModalIdentifiers.ENTERPRISE_EDITION_LICENSE));
    };

    // Note: DO NOT LOCALISE THESE STRINGS. Legally we can not since the license is in English.
    return (
        <GenericModal
            compassDesign={true}
            className={'EELicenseModal'}
            show={show}
            id='EELicenseModal'
            onExited={handleOnClose}
        >
            <>
                <div
                    className='title'
                >
                    {'Enterprise Edition License:'}
                </div>
                <div className='enterprise-license-text'>
                    <div>
                        <p>{'Astra Loop includes open-source software. See Open-source licences for Apache 2.0 and AGPLv3 notices, LICENSE.txt, and NOTICE.txt.'}</p>
                        <p>
                            <a href='/static/oss/oss.html'>
                                {'Open-source licences'}
                            </a>
                        </p>
                        <p>{'Commercial enterprise features, when enabled under a separate subscription, are subject to the applicable commercial license terms for those features.'}</p>
                    </div>
                </div>
                <div className='content-footer'>
                    <Button
                        onClick={handleOnClose}
                        emphasis='primary'
                    >
                        {'Close'}
                    </Button>
                </div>
            </>
        </GenericModal>
    );
};

export default EELicenseModal;

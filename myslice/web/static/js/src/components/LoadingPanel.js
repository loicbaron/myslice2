import React from 'react';
import classNames from 'classnames';

export default class LoadingPanel extends React.Component {

    render() {
        var loadingClass = classNames({
            'loading': true,
            'hidden': !this.props.show
        });
        return (
            <div className={loadingClass}>
                <img src="/static/images/loading.svg" alt="Loading..." />
            </div>
        );
    }
}
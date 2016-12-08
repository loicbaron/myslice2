import React from 'react';
import Title from './Title';

class Dialog extends React.Component {

    constructor(props) {
        super(props);
        this._handleEscKey = this._handleEscKey.bind(this);
        this._handleClick = this._handleClick.bind(this);
    }

    _handleClick(event){
        if (event.target.className == "dialog") {
            this.props.cancel();
        }
    }

    _handleEscKey(event){
        if (event.keyCode == 27) {
            this.props.cancel();
        }
    }

    render() {
        return (
            <div className="dialog" onKeyDown={this._handleEscKey} onClick={this._handleClick} >
                <div className="dialogClose" onClick={this.props.cancel}>
                    <i className="fa fa-close fa-2x fa-fw"></i>
                </div>
                <div className="container">
                    <div className="row">
                        <div className="col-sm-8 col-sm-offset-2">
                            <div className="d-panel">
                                {this.props.children}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

}

Dialog.propTypes = {
    cancel: React.PropTypes.func,
};

Dialog.defaultProps = {
    cancel: () => {}
};

const DialogHeader = ({children}) => {

    let num = React.Children.count(children);

    if (num >= 2) {
        return (
            <div className="d-header">
                <div className="row">
                    <div className="col-sm-6">
                        {children[0]}
                    </div>
                    <div className="col-sm-6 d-header-right">
                        {children.slice(1)}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="d-header">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>
        );
    }

};

const DialogBar = ({children}) => {

    let num = React.Children.count(children);

    if (num == 2) {
        return (
            <div className="d-bar">
                <div className="row">
                    <div className="col-sm-6">
                        {children[0]}
                    </div>
                    <div className="col-sm-6">
                        {children.slice(1)}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="d-bar">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>
        );
    }
};

const DialogBody = ({children}) =>
            <div className="d-body">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>;

const DialogFooter = ({children}) => {

    let num = React.Children.count(children);

    if (num >= 2) {
        return (
            <div className="d-footer">
                <div className="row">
                    <div className="col-sm-6">
                        {children[0]}
                    </div>
                    <div className="col-sm-6 d-footer-right">
                        {children.slice(1)}
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <div className="d-footer">
                <div className="row">
                    <div className="col-sm-12">
                        {children}
                    </div>
                </div>
            </div>
        );
    }

};

const DialogAlert = ({title, cancel, children}) =>
        <Dialog cancel={cancel}>
            <DialogHeader>
                <Title title={title} />
            </DialogHeader>
            <DialogBody>
                {children}
            </DialogBody>
            <DialogFooter>
                <div>
                    <button className="ok" onClick={cancel}>
                        Ok
                    </button>
                </div>
            </DialogFooter>
        </Dialog>;

DialogAlert.propTypes = {
    title: React.PropTypes.string,
    cancel: React.PropTypes.func,
};

DialogAlert.defaultProps = {
    title: 'Alert',
    cancel: () => {}
};

const DialogConfirm = ({title, cancel, confirm, children}) =>
        <Dialog cancel={cancel}>
            <DialogHeader>
                <Title title={title} />
            </DialogHeader>
            <DialogBody>
                {children}
            </DialogBody>
            <DialogFooter>
                <div>
                    <button className="ok" onClick={cancel}>
                        Cancel
                    </button>
                    <button className="confirm" onClick={confirm}>
                        Confirm
                    </button>
                </div>
            </DialogFooter>
        </Dialog>;

DialogConfirm.propTypes = {
    title: React.PropTypes.string,
    cancel: React.PropTypes.func,
    confirm: React.PropTypes.func.isRequired,
};

DialogConfirm.defaultProps = {
    title: 'Confirm',
    cancel: () => {}
};

export { Dialog, DialogBar, DialogBody, DialogFooter, DialogHeader, DialogAlert, DialogConfirm };

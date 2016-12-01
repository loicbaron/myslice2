import React from 'react';
import store from '../stores/SlicesFormStore';
import actions from '../actions/SlicesFormActions';

import ElementMessage from './base/ElementMessage';

import LoadingPanel from './LoadingPanel';

var ReactDOM = require('react-dom');

class SlicesForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }

    componentDidMount() {
        // store
        store.listen(this.onChange);
        if(ReactDOM.findDOMNode(this.refs.nameInput)){
            ReactDOM.findDOMNode(this.refs.nameInput).focus();
        }
    }
    componentDidUpdate() {
        if(ReactDOM.findDOMNode(this.refs.closeButton)){
            ReactDOM.findDOMNode(this.refs.closeButton).focus();
        }
    }
    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    handleLabelChange(e) {
        actions.updateLabel(e.target.value);
        actions.normaliseLabel(e.target.value);
    }
    handleSubmit(e) {
        // prevent the browser's default action of submitting the form
        e.preventDefault();
        var label = this.state.label;
        console.log(this.props.project);
        console.log(this.props.project.id);
        actions.updateProject(this.props.project.id);
        var flag = false;
        var msg = '';
        if(!label){
            msg += 'Name is required \n';
            flag = true;
        }
        if(flag){
            alert(msg);
            return;
        }

        actions.submitForm();
    }
    handleClose(e){
        console.log(e.target.value);
        actions.initComponent();
        this.props.close();
    }

    render() {
        if(this.state.message && Object.keys(this.state.message).length>0){
            return(
                <div>
                    <br/>
                    <ElementMessage message={this.state.message} />
                    <div className="col-sm-4">
                    <button className="large" value="Close" onClick={this.handleClose} ref="closeButton">
                    <i className="fa fa-times" aria-hidden="true"></i> Close
                    </button>
                    </div>
                </div>
            );
        }else{
            return (
                <div className="p-view-body">
                    <div className="container-fluid">
                        <div className="row">
                            <div className="col-md-12">
                                <div id="project-form">
                                    <form className="experimentForm" onSubmit={this.handleSubmit}>
                                    <input type="text" placeholder="Name" value={this.state.label} onChange={this.handleLabelChange} ref="nameInput" />
                                    <br/>
                                    <div><i><b>Important: </b>quote in your papers</i></div>
                                    <div>Experiments leading to the publication of this paper have been performed using the OneLab Federation of testbeds.</div>
                                    <br/>
                                    <div className="col-sm-8">
                                        <button className="large" type="submit" value="Save">
                                        <i className="fa fa-floppy-o" aria-hidden="true"></i> Save
                                        </button>
                                    </div>
                                    <div className="col-sm-4">
                                        <button className="large" value="Cancel" onClick={this.props.close}>
                                        <i className="fa fa-times" aria-hidden="true"></i> Cancel
                                        </button>
                                    </div>
                                    </form>
                                    <LoadingPanel show={this.state.loading} />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    }
}
SlicesForm.propTypes = {
    close: React.PropTypes.func,
};

SlicesForm.defaultProps = {
};

export default SlicesForm;

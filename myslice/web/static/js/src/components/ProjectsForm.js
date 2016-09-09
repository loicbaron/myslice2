import React from 'react';
import store from '../stores/ProjectsFormStore';
import actions from '../actions/ProjectsFormActions';

import ElementMessage from './base/ElementMessage';

import LoadingPanel from './LoadingPanel';

var ReactDOM = require('react-dom');

class ProjectsForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.updateAuthority = this.updateAuthority.bind(this);
    }

    componentDidMount() {
        // store
        store.listen(this.onChange);
        ReactDOM.findDOMNode(this.refs.nameInput).focus();
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

    handleUrlChange(e) {
       actions.updateUrl(e.target.value);
    }

    updateAuthority(value) {
       console.log("component: "+value);
       actions.updateAuthority.defer(value);
    }

    handleDescriptionChange(e) {
       actions.updateDescription(e.target.value);
    }

    handleStartDateChange(e) {
       actions.updateStartDate(e.target.value);
    }

    handleEndDateChange(e) {
       actions.updateEndDate(e.target.value);
    }

    onPublicChanged(e) {
        actions.updatePublic(e.currentTarget.checked);
        actions.updateProtected(!e.currentTarget.checked);
        actions.updatePrivate(!e.currentTarget.checked);
    }

    onProtectedChanged(e) {
        actions.updatePublic(!e.currentTarget.checked);
        actions.updateProtected(e.currentTarget.checked);
        actions.updatePrivate(!e.currentTarget.checked);
    }

    onPrivateChanged(e) {
        actions.updatePublic(!e.currentTarget.checked);
        actions.updateProtected(!e.currentTarget.checked);
        actions.updatePrivate(e.currentTarget.checked);
    }

    handleSubmit(e) {
        // prevent the browser's default action of submitting the form
        e.preventDefault();
        var label = this.state.label;
        var description = this.state.description;

        var flag = false;
        var msg = '';
        if(!label){
            msg += 'Name is required \n';
            flag = true;
        }
        if(!description){
            msg += 'Description is required \n';
            flag = true;
        }
        if(flag){
            alert(msg);
            return;
        }

        actions.submitForm();

    }

    render() {
        console.log(this.message);
        console.log(this.state.message);
        if(this.state.message && Object.keys(this.state.message).length>0){
            return(
                <div>
                    <br/>
                    <ElementMessage message={this.state.message} />
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
                                    <input type="radio" value={this.state.v_public} checked={this.state.v_public === true } onChange={this.onPublicChanged} /> Public
                                    <input type="radio" value={this.state.v_protected} checked={this.state.v_protected === true } onChange={this.onProtectedChanged} /> Protected
                                    <input type="radio" value={this.state.v_private} checked={this.state.v_private === true } onChange={this.onPrivateChanged} /> Private <br/>

                                    <input type="text" placeholder="URL" value={this.state.url} onChange={this.handleUrlChange} /><br/>
                                    <textarea name="description" placeholder="Describe your project in a few words..." value={this.state.description} onChange={this.handleDescriptionChange} /><br/>
                                    Start: <input type="text" placeholder="yyyy-mm-dd hh:mm" value={this.state.start_date} onChange={this.handleStartDateChange} />
                                    End: <input type="text" placeholder="yyyy-mm-dd hh:mm" value={this.state.end_date} onChange={this.handleEndDateChange} /><br/>
                                    <br/>
                                    <div><i><b>Important: </b>quote in your papers</i></div>
                                    <div>Experiments leading to the publication of this paper have been performed using the OneLab Federation of testbeds.</div>
                                    <br/>
                                    <button className="large" type="submit" value="Save">
                                    <i className="fa fa-floppy-o" aria-hidden="true"></i> Save
                                    </button>
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

export default ProjectsForm;

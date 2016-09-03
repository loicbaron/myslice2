import React from 'react';
import store from '../stores/SlicesFormStore';
import actions from '../actions/SlicesFormActions';

import LoadingPanel from './LoadingPanel';

var ReactDOM = require('react-dom');

class SlicesForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
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

    render() {
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
                                <button className="large" type="submit" value="Save">
                                <i class="fa fa-floppy-o" aria-hidden="true"></i> Save
                                </button>
                                </form>
                                <div className="">
                                    {this.state.message}
                                </div>
                                <LoadingPanel show={this.state.loading} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        );
    }
}

export default SlicesForm;

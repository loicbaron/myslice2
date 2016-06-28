import React from 'react';
import Select from 'react-select';

import actions from '../actions/UsersActions';

export default class UsersFilter extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            'selected': []
        };
        this.setValue = this.setValue.bind(this);
    }

    componentDidMount() {
        // store
        // store.listen(this.onChange);

    }

    componentWillUnmount() {
        // store.unlisten(this.onChange);
    }


    setValue(e) {
		this.setState({ 'selected': e.target.value });
        this.props.handleChange(e.target.value);
	}

    render() {
        return <input 
            type="text" 
            onChange={this.setValue}
            placeholder="Search user"
        />

    }
}

import React from 'react';

import actions from '../../actions/dialogs/SelectResource';
import store from '../../stores/dialogs/SelectResource';

class FilterLeases extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleStartDate = this.handleStartDate.bind(this);
        this.handleTime = this.handleTime.bind(this);
        this.handleDuration = this.handleDuration.bind(this);
    }
    componentDidMount() {
        store.listen(this.onChange);
        console.log(this.state.lease);
    }
    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }
    handleStartDate(e) {
       console.log(e.target.value);
       this.props.handleChange({'start_date':e.target.value});
    }
    handleTime(e) {
       console.log(e.target.value);
       this.props.handleChange({'start_time':e.target.value});
    }
    handleDuration(e) {
       console.log(e.target.value);
       this.props.handleChange({'duration':e.target.value});
    }
    render(){
        return(
            <div className="container">
                <div className="row">
                  <div className="col-sm-4">
                    Start date: <input type="date" placeholder="yyyy-mm-dd " value={this.state.start_date} onChange={this.handleStartDate.bind(this)} />
                    &nbsp;<input type="time" placeholder="hh:mm" value={this.state.time} onChange={this.handleTime.bind(this)}/>
                  </div>
                  <div className="col-sm-2">Duration:&nbsp; 
                    <select value={this.state.duration} onChange={this.handleDuration.bind(this)}>
                        <option value="10 min">10 min</option>
                        <option value="15 min">15 min </option>
                        <option value="30 min ">30 min</option>
                        <option value="60 min">1 h</option>
                        <option value="120 min">2 h</option>
                        <option value="240 min">4 h</option>
                        <option value="480 min">8 h</option>
                        <option value="1440 min">24 h</option>
                    </select>
                  </div>
                </div>
            </div>
            );
    }
}
FilterLeases.propTypes = {
    handleChange: React.PropTypes.func.isRequired
};

FilterLeases.defaultProps = {
};
export default FilterLeases;

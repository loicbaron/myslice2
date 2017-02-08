import React from 'react';

import actions from '../../actions/dialogs/SelectResource';
import store from '../../stores/dialogs/SelectResource';

class FilterLeases extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
    }
    componentDidMount() {
        store.listen(this.onChange);
    }
    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }
    handleStartDateChange(e) {
       actions.updateStartDate(e.target.value);
       this.props.handleChange();
    }
    handleTimeChange(e) {
       console.log(e.target.value);
       actions.updateTime(e.target.value);
       this.props.handleChange();
    }
    handleChangeDuration(event) {
       actions.updateDuration(event.target.value);
       this.props.handleChange();
    }
    render(){
        return(
            <div className="container">
                <div className="row">
                  <div className="col-sm-4">
                    Start date: <input type="date" placeholder="yyyy-mm-dd " value={this.state.start_date} onChange={this.handleStartDateChange.bind(this)} />
                    &nbsp;<input type="time" placeholder="hh:mm" value={this.state.time} onChange={this.handleTimeChange.bind(this)}/>
                  </div>
                  <div className="col-sm-2">Duration:&nbsp; 
                    <select value={this.state.duration} onChange={this.handleChangeDuration.bind(this)}>
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

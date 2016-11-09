import React from 'react';

import actions from '../../actions/dialogs/SelectResource';
import store from '../../stores/dialogs/SelectResource';

import Dialog from '../base/Dialog';
import DialogPanel from '../base/DialogPanel';
import DialogHeader from '../base/DialogHeader';
import DialogFooter from '../base/DialogFooter';
import DialogBody from '../base/DialogBody';
import Title from '../base/Title';
import Text from '../base/Text';
import DateTime from '../base/DateTime';
import List from '../base/List';
import Button from '../base/Button';
import InputText from '../InputText'
import { ResourceList } from '../objects/Resource';

class SelectResourceDialog extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleChange = this.handleChange.bind(this);
        //this.handleChangeDuration = this.handleChangeDuration.bind(this);
        //this.handleStartDateChange = this.handleStartDateChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchResources(this.props.testbed);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }
    handleSubmit(event) {

        // prevent the browser's default action of submitting the form
        event.preventDefault();
        //console.log(this.state.value);
        //console.log(this.state.type);
        var tofilter= this.state.type.concat("(.*)".concat(this.state.value));
        console.log(tofilter);
        actions.updateFilter(tofilter);
    }
    handleFilter(value) {
        //var f = {'email':value,'shortname':value}
        //actions.updateFilteredUsers();
        //

        //For the text filter
        //console.log( value);

        actions.updateFilter(value);
    }

    /* fetch the users list */
    fetchUsers(filter={}) {
        switch (this.props.from){
            case 'authority':
                actions.fetchFromAuthority(filter);
                break;
            default:
                actions.fetchUsers(filter);
        }
    }

    selectResource(element) {
        actions.selectResource(element);
    }

    handleStartDateChange(e) {

       actions.updateStartDate(e.target.value);

    }
    handleTimeChange(e) {
       actions.updateTime(e.target.value);
    }
    isSelected(resource) {
        //console.log(this.state.selected);
        /* TOFIX
        this.state.selected.find((el) => {
            return el.id === resource.id;
        })
        */
    }

    handleChange(event) {
        this.setState({value: event.target.value});


    }
    handleChangeDuration(event) {
        this.setState({duration: event.target.value});


    }
     handleChangeType(event) {
          actions.updateType(event.target.value);


    }

    //Reserve Resources
    applyChanges() {
  // calculate the end date needed for the POST /lease

        //to have the duration on seconds
        //var nu=this.state.duration.split(" ");
          // console.log(nu[0]*60);
        //Convert the start date on timestamp

        var datum = Date.parse(this.state.start_date);
        var timeStamp = datum/1000;
        //alert(this.state.start_date)​
        console.log(timeStamp);
        //console.log(this.state.time);
        //var end_date= new Date(this.state.start_date + (this.state.time+int(this.state.duration)));


    }

    renderSelectedStatus() {
        if (this.state.selected.length > 0) {
            return <div>
                You have selected <a>{this.state.selected.length} resource{this.state.selected.length > 1 ? "s":"" }</a>
            </div>;
        }
    }

    render() {
        // if(Object.keys(this.state.filter).length>0){
        //     var usersList = <UsersList users={this.state.filteredUsers} addUser={this.props.addUser} />
        // }else{
        //     var usersList = <UsersList users={this.state.users} addUser={this.props.addUser} />
        // }

        var dis=[];
        //var selectedOption = this.props.selected;
         const optionLocation = this.state.all_resources.map(function(res) {
             if (!res.location) return;
             if (dis.indexOf(res.location.city) < 0 && res.location.city != null)
                 {dis.push(res.location.city);
                  return (<option key={res.id} value={res.location.city} >{res.location.city}</option>);
                 }
         });
         var reservation= null;



         switch(this.props.testbed.name) {
            case 'FIT IoT-Lab':
                reservation =

                    <div className="p-view-body">
                        <p><img className="img" src="/static/images/iot.png" alt="FIT IoT Lab" /></p>
                            <div className="container-fluid">

                                <div className="row">
                                    <div className="col-md-12">
                                        <div id="resourceReservation-form">

                                                Configure your experiment :<br/>
                                                Start date: <input type="date" placeholder="yyyy-mm-dd " value={this.state.start_date} onChange={this.handleStartDateChange.bind(this)} />
                                                Time:  <input type="time" placeholder="hh:mm" value={this.state.time} onChange={this.handleTimeChange.bind(this)}/>
                                                <br/>
                                                Duration:<select value={this.state.duration} onChange={this.handleChangeDuration.bind(this)}>
                                                              <option value="10 min">10 min</option>
                                                              <option value="15 min">15 min </option>
                                                              <option value="30 min ">30 min</option>
                                                              <option value="1 h">1 h</option>
                                                              <option value="2 h">2 h</option>
                                                              <option value="4 h">4 h</option>
                                                              <option value="8 h">8 h</option>
                                                              <option value="24 h">24 h</option>
                                                          </select>
                                                <br/>
                                            <form className="experimentForm" onSubmit={this.handleSubmit} >
                                                Choose your nodes :
                                                <br/>
                                                <div className="container">
                                                Type : <ul className="nav nav-pills "  >
                                                            <li className="active"><a data-toggle="pill" href="#home">A8 Node</a></li>
                                                            <li><a data-toggle="pill" href="#menu1">M3 Node</a></li>
                                                            <li><a data-toggle="pill" href="#menu2">WSN430 Node</a></li>
                                                       </ul>
                                                    <div className="tab-content">
                                                        <div id="home" className="tab-pane fade in active">
                                                            <p>The A8 open node is the most powerful IoT-LAB node and allows to run high-level OS like Linux.</p>
                                                        </div>
                                                        <div id="menu1" className="tab-pane fade">
                                                            <p>The M3 open node is based on a STM32 (ARM Cortex M3) micro-controller.</p>
                                                        </div>
                                                        <div id="menu2" className="tab-pane fade">
                                                            <p>The WSN430 open node is a WSN430 node based on a low power MSP430-based platform, with a fully functional ISM radio interface and a set of standard sensors.</p>
                                                        </div>
                                                    </div>

                                                </div>
                                                <br/>
                                                Choose the type (M3, A8, WSN340)? <input type ="text" value={this.state.type} onChange={this.handleChangeType} placeholder="type" /><br/>
                                                Site : <select  value={this.state.value} onChange={this.handleChange} >
                                                            {optionLocation}
                                                       </select>

                                            </form>

                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                break;
        }
        return (
            <Dialog close={this.props.close}>
                <DialogPanel>
                    <DialogHeader>
                        <Title title={this.props.testbed.name} />
                    </DialogHeader>
                    <div>{reservation}</div>
                    <DialogBody>

                        <InputText name="filter" handleChange={this.handleFilter} placeholder="Filter" />
                        <button className="apply" onClick={this.applyChanges.bind(this)} >
                            Apply
                        </button>
                        <ResourceList resources={this.state.resources}
                                      selected={this.state.selected}
                                      handleSelect={(element) => this.selectResource(element)} />
                    </DialogBody>
                    <DialogFooter>
                        {this.renderSelectedStatus()}
                        <button className="cancel" onClick={this.cancel} >
                            Cancel
                        </button>

                    </DialogFooter>
                </DialogPanel>
            </Dialog>
        );
    }
}

SelectResourceDialog.propTypes = {
    testbed: React.PropTypes.object.isRequired,
    close: React.PropTypes.func.isRequired,

};

SelectResourceDialog.defaultProps = {

};

export default SelectResourceDialog;

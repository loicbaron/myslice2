import React from 'react';

import actions from '../../actions/dialogs/SelectResource';
import store from '../../stores/dialogs/SelectResource';

import { DialogPanel, Dialog, DialogBody, DialogHeader, DialogFooter, DialogBar } from '../base/Dialog';
import Title from '../base/Title';
import Text from '../base/Text';
import DateTime from '../base/DateTime';
import Button from '../base/Button';
import InputText from '../InputText'

import IotFilter from '../filters/iot';
import FilterLeases from '../filters/leases';
import { ResourceList } from '../objects/Resource';

class SelectResourceDialog extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.apply = this.apply.bind(this);
        this.cancel = this.cancel.bind(this);
        this.refreshResources = this.refreshResources.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        actions.fetchResources(this.props.testbed);
        actions.initLease();
        console.log(this.state.lease);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    selectResource(resource) {
        actions.selectResource(resource);
    }

    clearSelection() {
        actions.clearSelection();
    }

    showSelected() {
        actions.showSelected();
    }

    showAll() {
        actions.showAll();
    }

    renderSelectedStatus() {
        if (this.state.selected.length > 0) {
            if (this.state.show_selected) {
                return <div className="d-selected">
                    You have selected <span>{this.state.selected.length + " resource" + (this.state.selected.length > 1 ? "s" : "")}</span>
                    &nbsp;(<a onClick={this.showAll}>Show all resources</a> | <a onClick={this.clearSelection}>Clear</a>)
                </div>;
            } else {
                return <div className="d-selected">
                    You have selected <a onClick={this.showSelected}>{this.state.selected.length + " resource" + (this.state.selected.length > 1 ? "s" : "")}</a>
                </div>;
            }
        } else {
            return <div className="d-selected">Select resources</div>;
        }
    }

    cancel() {
        this.clearSelection();
        this.props.cancel();
    }

    apply() {
        console.log(this.props.testbed.name);
        this.props.apply(this.state.selected, this.state.lease);
        this.clearSelection();
        this.props.cancel();
    }

    filterResources(filter) {
        actions.filterResources(filter);
    }
    handleFilter(value) {
        //var f = {'email':value,'shortname':value}
        //actions.updateFilteredUsers();
        //

        //For the text filter
        //console.log( value);

        actions.updateFilter(value);
    }

    filterEvent(event) {
        actions.filterEvent(event.target.value);
    }


// Filter by site
    handleChange(event) {
        this.setState({value: event.target.value});
        actions.updateFilter(event.target.value);
    }

    handleChangeType(event) {
         //actions.updateType(event.target.value);
         event.preventDefault()
         var el = event.target.textContent

         console.log(el)
         actions.updateFilter(el);
    }
    refreshResources(){
        actions.fetchResources(this.props.testbed);
    }
    render() {
        var dis=[];
        //var selectedOption = this.props.selected;
         const optionLocation = this.state.all_resources.map(function(res) {
             if (!res.location) return;
             if (dis.indexOf(res.location.city) < 0 && res.location.city != null)
                 {dis.push(res.location.city);
                  return (<option key={res.id} value={res.location.city} >{res.location.city}</option>);
                 }
         });

         var reservation = null;
         var filterInput = null;
         var testbedLink = null;
         console.log(this.props.testbed);
         if(this.props.testbed.hasOwnProperty('hasLeases') && this.props.testbed.hasLeases == true){
            reservation = <FilterLeases testbed={this.props.testbed} handleChange={this.refreshResources} />;
         }
         switch(this.props.testbed.name) {
            case 'FIT IoT-Lab':
            case 'FIT IoT-Lab Dev':
                filterInput = <div>
                    <IotFilter handleChange={this.filterResources} />
                </div>
                testbedLink = 
                <div className="container">
                    <div className="row">
                        <a href="https://www.iot-lab.info/hardware/" target="_blank">Technical specifications</a>
                    </div>
                </div>

                var info =
<div className="container">
<div className="row">
  <div className="col-sm-2">Site : <select  value={this.state.value} onChange={this.handleChange} >
                                        <option value="">Choose the site</option>
                                        {optionLocation}
                                   </select></div>
  <div className="col-sm-5"><center><img className="img" src="/static/images/iot.png" alt="FIT IoT Lab" /></center></div>
</div>
<div  className="row">
   <div className="col-sm-1">Type:</div>
    <div id="Type" className="col-sm-6">
      <ul className="nav nav-pills"  >
          <li ><a onClick={this.handleChangeType.bind(this)} data-toggle="tab" href="#home">A8</a></li>
          <li><a onClick={this.handleChangeType.bind(this)} data-toggle="tab" href="#menu1">M3</a></li>
          <li><a onClick={this.handleChangeType.bind(this)} data-toggle="tab" href="#menu2">WSN430</a></li>
      </ul>
      <div className="panel-body">
          <div className="tab-content clearfix">
              <div className="tab-pane fade in active" id="home"><p>The A8 open node is the most powerful IoT-LAB node and allows to run high-level OS like Linux.
                                                                For more information click  <a href="https://www.iot-lab.info/hardware/a8">here</a></p>
              </div>
              <div className="tab-pane fade" id="menu1"><p>The M3 open node is based on a STM32 (ARM Cortex M3) micro-controller.
                                                                For more information click<a href="https://www.iot-lab.info/hardware/m3"> here</a></p>
              </div>
              <div className="tab-pane fade" id="menu2"><p>The WSN430 open node is a WSN430 node based on a low power MSP430-based platform with a fully functional ISM radio interface and a set of standard sensors.
                                                                For more information click  <a href="https://www.iot-lab.info/hardware/wsn430">here</a></p>
              </div>
          </div>
      </div>
    </div>
</div>
</div>
                break;
            default:
                filterInput = <input
                        type="text"
                        onChange={this.filterEvent}
                        placeholder="Filter"
                        />
                break;
        }

        let resources = [];
        if (this.state.show_selected) {
            resources = this.state.selected;
        } else if (this.state.filtered.length > 0) {
            resources = this.state.filtered;
        } else {
            resources = this.state.resources;
        }

        return (
            <Dialog cancel={this.props.cancel}>
                <DialogHeader>
                    <Title title="Add Resources" />
                </DialogHeader>
                <DialogBar>
                    {reservation}
                </DialogBar>
                <DialogBar>
                    {filterInput}
                </DialogBar>
                <DialogBody>
                    <ResourceList resources={resources}
                                  selected={this.state.selected}
                                  handleSelect={this.selectResource}
                    />
                </DialogBody>
                <DialogBar>
                    {testbedLink}
                </DialogBar>
                <DialogFooter>
                    {this.renderSelectedStatus()}
                    <div>
                        <button className="cancel" onClick={this.cancel} >
                            Cancel
                        </button>
                        <button className="apply" onClick={this.apply} >
                            Apply
                        </button>
                    </div>
                </DialogFooter>
            </Dialog>
        );
    }
}

SelectResourceDialog.propTypes = {
    testbed: React.PropTypes.object.isRequired,
    apply: React.PropTypes.func.isRequired,
    cancel: React.PropTypes.func.isRequired,
};

SelectResourceDialog.defaultProps = {

};

export default SelectResourceDialog;

import alt from '../../alt';
import actions from '../../actions/dialogs/SelectResource';
import source from '../../sources/dialogs/SelectResource';

import common from '../../utils/Commons';

class SelectResourceDialog {

    constructor() {

        // Resource List as retrieved from the API
        this.resources = [];

        // Filtered users
        this.filtered = [];

        // Selected users
        this.selected = [];

        // current testbed
        this.testbed = null;

        // Lease
        this.lease = {};

        // if true shows selected
        this.show_selected = false;

        this.errorMessage = null;

        // the list of resources
        this.resources = [];
        this.lease['resources'] = [];

        this.all_resources = [];
        // the list of selected resources
        this.selected = [];
        this.selectedIdList= [];
        // The type of the nodes
        this.type ='';
        this.time ='';

        // initialise the start date
        var d = new Date();
        var m = d.getMonth()+1;
        var month = (m<10?'0':'') + m;
        var day = (d.getDate()<10?'0':'') + d.getDate();
        var df = d.getFullYear()+"-"+month+"-"+day;
        this.start_date = df;
        this.updateStartDate(df);

        //initialise the duration
        this.duration='10 min';
        this.updateDuration(this.duration);

        //intialise the filter
        this.filter = null;
        this.filterResource = this.filterResource.bind(this);

        this.errorMessage = null;
        this.message = {};

        this.bindListeners({
            fetchResources: actions.FETCH_RESOURCES,
            updateResources: actions.UPDATE_RESOURCES,
            errorResources: actions.ERROR_RESOURCES,

            selectResource: actions.SELECT_RESOURCE,
            clearSelection: actions.CLEAR_SELECTION,
            showSelected: actions.SHOW_SELECTED,
            showAll: actions.SHOW_ALL,
            filterResources: actions.FILTER_RESOURCES,
            filterEvent: actions.FILTER_EVENT,

            updateTestbed: actions.UPDATE_TESTBED,
            initLease: actions.INIT_LEASE,
            updateStartDate: actions.UPDATE_START_DATE,
            updateTime: actions.UPDATE_TIME,
            updateType: actions.UPDATE_TYPE,
            updateFilter : actions.UPDATE_FILTER,
            SuccessReservation : actions.SUCCESS_RESERVATION,
            ErrorReservation : actions.ERROR_RESERVATION,

        });

        this.registerAsync(source);
    }

    fetchResources(testbed = null) {

        this.resources = [];
        this.filtered = [];

        if (testbed) {
            this.updateTestbed(testbed);
        }

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchResources();
        }


    }
    initLease(){
        this.lease = {};
        this.lease['resources'] = [];

        // initialise the start date
        var d = new Date();
        var m = d.getMonth()+1;
        var month = (m<10?'0':'') + m;
        var day = (d.getDate()<10?'0':'') + d.getDate();
        var df = d.getFullYear()+"-"+month+"-"+day;
        this.updateStartDate(df);

        //initialise the duration
        this.duration='10 min';
        this.updateDuration(this.duration);
    }
    updateResources(resources) {
        if (resources.hasOwnProperty('data')) {
            this.resources = resources.data.result;
        } else {
            this.resources = resources;
        }
        // we do a copy of the object to avoid references
        //this.all_resources = Object.assign([], this.resources);
    }

    errorResources(errorMessage) {
        console.log(errorMessage);
    }

    selectResource(resource) {
        // Is this resource already selected?
        let resourceId = this.selected.some(function(el) {
            return el.id === resource.id;
        });

        // If not add it to selected
        if (!resourceId) {
            this.selected.push(resource);
        // Else remove it from selected
        } else {
            this.selected = this.selected.filter(function(el) {
                return el.id !== resource.id;
            });
        }

        if (this.selected.length == 0) {
            this.showAll();
        }

        // Gather the Selected Resources Id in Lease
        var resources = Array();
        this.selected.map(function(res) {
            resources.push(res.id);
        }.bind(this));
        this.lease['resources'] = resources;
    }

    clearSelection() {
        this.selected = [];
        this.lease = {};
        this.showAll();
    }

    showSelected() {
        this.show_selected = true;
    }

    showAll() {
        this.show_selected = false;
    }

    /*
        filters = {
            city: [], // array list
            country: [],
            hardware: []
        }
     */
    filterResources(value) {
        // value is an array
        let filters = {
            city: [],
            country: [],
            hardware: []
        };

        this.filtered = this.resources;

        for(let i = 0; i < value.length; i++) {
            filters[value[i].type].push(value[i].value)
        }

        Object.keys(filters).forEach(function(filter_name) {

            switch(filter_name) {
                case 'city':
                    if (filters[filter_name].length > 0) {
                        this.filtered = this.filtered.filter(function (el) {
                            return typeof(el.location.city) !== 'undefined' && filters[filter_name].some(value =>
                                el.location.city.toLowerCase().indexOf(value) != -1
                            );
                        });
                    }
                    break;
                case 'country':
                    if (filters[filter_name].length > 0) {
                        this.filtered = this.filtered.filter(function (el) {
                            return typeof(el.location.country) !== 'undefined' && filters[filter_name].some(value =>
                                el.location.country.toLowerCase().indexOf(value) != -1
                            );
                        });
                    }

                    break;
                case 'hardware':
                    if (filters[filter_name].length > 0) {
                        this.filtered = this.filtered.filter(function (el) {
                            return typeof(el.hardware_types) !== 'undefined' && filters[filter_name].some(value =>
                                    el.hardware_types.some(hw => hw.toLowerCase().indexOf(value) != -1)
                            );
                        });
                    }
                    break;
                default:
                    if (filters[filter_name].length > 0) {
                        this.filtered = this.filtered.filter(function (el) {
                            return typeof(el.location.name) !== 'undefined' && filters[filter_name].some(value =>
                                el.name.toLowerCase().indexOf(value) != -1
                            );
                        });
                    }
            }

        }.bind(this));

    }
    filterEvent(value){
        if(value){
            this.filtered = this.resources.filter(function(el) {
                return common.searchText(el, value);
            });
        }else{
            this.filtered = [];
        }
    }
    updateTestbed(testbed) {
        this.testbed = testbed;
        this.lease['testbed'] = testbed.id;
    }

    updateStartDate(start_date) {
        this.start_date = start_date;
        if(!this.time){
            this.setTimeNow();
        }
        //Convert start_date to timestamp
        var t = " ".concat(this.time);
        var datum = Date.parse(this.start_date.concat(t));
        this.lease['start_time'] = datum/1000;
    }
    setTimeNow(){
        var d = new Date();
        var h = (d.getHours()<10?'0':'') + d.getHours();
        var m = (d.getMinutes()<10?'0':'') + d.getMinutes();
        this.updateTime(h+":"+m);
    }
    updateTime(time) {
        this.time = time;
        var t = " ".concat(time);
        //Convert start_date to timestamp
        var datum = Date.parse(this.start_date.concat(t));
        this.lease['start_time'] = datum/1000;
    }
    updateDuration(duration){
        this.duration = duration;
        //Convert the duration to seconds
        var nu = duration.split(' ');
        this.lease['duration'] = nu[0]*60;
    }

    updateType(type) {
        this.type = type;
    }
    updateFilter(filter) {
        this.filter = filter.toLowerCase();
       // console.log( this.filter);
        this.resources = this.all_resources.filter(this.filterResource);

    }
    filterResource(resource){
        return resource.name.search(this.filter) > -1;
    }
    isSelected(resource) {
        this.selected.find((el) => {
            return (el.id === resource.id);
        });
    }
    SuccessReservation() {
        this.message['type'] = "success";
        this.message['msg'] = "Lease has been created.";
    }

    ErrorReservation(response) {
        this.message['type'] = "error";
        this.message['msg'] = response.data.error;
    }



}


export default alt.createStore(SelectResourceDialog, 'SelectResourceDialog');


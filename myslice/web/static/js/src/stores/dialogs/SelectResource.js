import alt from '../../alt';
import actions from '../../actions/dialogs/SelectResource';
import source from '../../sources/dialogs/SelectResource';

class SelectResourceDialog {

    constructor() {
        // the testbed
        this.testbed = null;
        // the list of resources
        this.resources = [];
        this.all_resources = [];
        // the list of selected resources
        this.selected = [];
        // The type of the nodes
        this.type ='';
        this.time ='';
        // initialise the start date
        var d = new Date();
        var df = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();
        this.start_date=df;
        //initialise the duration
        this.duration='';
        //intialise the filter
        this.filter = null;
        this.filterResource = this.filterResource.bind(this);

        this.errorMessage = null;

        this.bindListeners({
            updateTestbed: actions.UPDATE_TESTBED,
            fetchResources: actions.FETCH_RESOURCES,
            updateResources: actions.UPDATE_RESOURCES,
            errorResources: actions.ERROR_RESOURCES,
            updateStartDate: actions.UPDATE_START_DATE,
            updateTime: actions.UPDATE_TIME,
            updateType: actions.UPDATE_TYPE,
            selectResource: actions.SELECT_RESOURCE,
            updateFilter : actions.UPDATE_FILTER,


        });

        this.registerAsync(source);

    }

    updateTestbed(testbed) {
        this.testbed = testbed;
    }

    fetchResources(testbed = null) {

        if (testbed) {
            this.testbed = testbed;
        }

        if (!this.getInstance().isLoading()) {
            this.getInstance().resources();
        }

    }

    updateResources(resources) {
        if (resources.hasOwnProperty('data')) {
            this.resources = resources.data.result;
        } else {
            this.resources = resources;
        }
        // we do a copy of the object to avoid references
        this.all_resources = Object.assign([], this.resources);
    }

    errorResources(errorMessage) {
        console.log(errorMessage);
    }
    updateStartDate(start_date) {
        this.start_date = start_date;
    }
    updateTime(time) {
        this.time = time;
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

    selectResource(resource) {
        let resourceId = this.selected.some(function(el) {
            return el.id === resource.id;
        });

        if (!resourceId) {
            this.selected.push(resource);
        } else {
            this.selected = this.selected.filter(function(el) {
                return el.id !== resource.id;
            });
        }

        // if ((typeof(resource.isSelected) === 'undefined') || (!resource.isSelected)) {
        //     resource.isSelected = true;
        // } else {
        //     resource.isSelected = false;
        // }
    }

}


export default alt.createStore(SelectResourceDialog, 'SelectResourceDialog');


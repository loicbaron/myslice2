import alt from '../../alt';
import actions from '../../actions/views/Slice';
import source from '../../sources/views/Slice';
import common from '../../utils/Commons';

/*
    This store is used in the SliceView
 */
class SliceView {

    constructor() {
        // the hrn of the current slice
        this.hrn = null;

        // the current slice
        this.slice = {
            shortname: null,
            name: null,
            hrn: null,
            users: [],
            resources: []
        };

        // the slice we are saving
        this.saving = {};

        // the list of testbeds
        this.testbeds = [];

        // the selected testbed
        this.testbed = null;

        this.dialog = null;

        this.errorMessage = null;

        this.bindListeners({
            updateSlice: actions.UPDATE_SLICE,
            fetchSlice: actions.FETCH_SLICE,
            errorSlice: actions.ERROR_SLICE,

            saveSlice: actions.SAVE_SLICE,
            saveSliceSuccess: actions.SAVE_SLICE_SUCCESS,
            saveSliceError: actions.SAVE_SLICE_ERROR,

            removeResources: actions.REMOVE_RESOURCES,

            updateTestbeds: actions.UPDATE_TESTBEDS,
            fetchTestbeds: actions.FETCH_TESTBEDS,
            errorTestbeds: actions.ERROR_TESTBEDS,

            selectResourceDialog: actions.SELECT_RESOURCE_DIALOG,
            selectUserDialog: actions.SELECT_USER_DIALOG,
            closeDialog: actions.CLOSE_DIALOG
        });

        this.registerAsync(source);
        
    }


    fetchSlice(hrn) {

        this.hrn = hrn;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetchSlice();
        }

    }

    updateSlice(slice) {
        if (slice.hasOwnProperty('data')) {
            this.slice = slice.data.result[0];
        } else {
            this.slice = slice;
        }

    }

    errorSlice(errorMessage) {
        console.log(errorMessage);
    }

    fetchTestbeds() {
        this.getInstance().fetchTestbeds();
    }

    updateTestbeds(testbeds) {
        if (testbeds.hasOwnProperty('data')) {
            this.testbeds = testbeds.data.result;
        } else {
            this.testbeds = testbeds;
        }

    }

    errorTestbeds(errorMessage) {
        console.log(errorMessage);
    }

    selectResourceDialog(testbed) {
        this.dialog = 'selectResource';
        this.testbed = testbed;
    }

    selectUserDialog() {
        this.dialog = 'selectUser';
    }

    closeDialog() {
        this.dialog = null;
        this.testbed = null;
    }
    removeResources(save){
        var _this = this;
        // save = {'resources': r, 'lesases': l}
        this.saving = this.slice;
        if (save.hasOwnProperty('resources')) {
            save.resources.map(r => {
                // remove this resource from this.saving
                if(common.containsObject(r, this.saving.resources)){
                    this.saving.resources = common.removeFromArray(this.saving.resources, r.id, 'id');
                }else{
                    console.log("resource not found");
                }
                // remove leases for this resource from this.saving
                this.saving.leases.map(function(l, j) {
                    if(l.resources.includes(r.id)){
                        _this.saving.leases.splice(j);
                    }
                });
            });
        }
        if (save.hasOwnProperty('leases') && save['leases'].length > 0){
            // remove leases for this resource from this.saving
            save.leases.map(l => {
                l.resources.map(r => {
                    _this.saving.leases.map(function(sLease, i) {
                        if(sLease.resources.includes(r)){
                            _this.saving.leases.splice(i);
                        }
                    });
                });
            });
            this.getInstance().saveLeases();
        } else {
            this.getInstance().saveSlice();
        }
    }
    saveSlice(save) {
        // save = {'resources': r, 'lesases': l}
        // this.saving is a copy of this.slice
        this.saving = this.slice;
        console.log("save = ");
        console.log(save);
        // if save has resources, add these resources to this.saving
        if (save.hasOwnProperty('resources')) {
            save.resources.map(r => {
                if (!this.saving.resources.includes(r.id)) {
                    this.saving.resources.push(r);
                }
            });
        }
        // if save has leases, add these leases to this.saving
        if (save.hasOwnProperty('leases') && save['leases'].length > 0) {
            var _this = this;
            save['leases'].forEach(function(lease) {
                lease['slice_id'] = _this.slice.id;
                _this.saving.leases.push(lease);
            });
            console.log(this.saving);
            this.getInstance().saveLeases();
        } else {
            this.getInstance().saveSlice();
        }
    }

    saveSliceSuccess(x) {
        console.log(x);
        // {"result": "success", "debug": null, "error": null, "events": [["858dddc3-5500-4ba1-a6b3-430ef32434d6"]]}

        this.saving = {};
    }

    saveSliceError(x) {
        console.log(x);

        this.saving = {};
    }

}


export default alt.createStore(SliceView, 'SliceView');

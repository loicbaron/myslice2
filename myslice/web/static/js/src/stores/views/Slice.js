import alt from '../../alt';
import actions from '../../actions/views/Slice';
import source from '../../sources/views/Slice';

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

    saveSlice(save) {
        this.saving = this.slice;

        if (save.hasOwnProperty('resources')) {
            save.resources.map(r => {
                if (!this.saving.resources.includes(r.id)) {
                    this.saving.resources.push(r);
                }
            });
        }
        if(save.hasOwnProperty('lease') && Object.keys(save['lease']).length>0){
            save.lease['slice_id'] = this.slice.id;
            this.saving.leases.push(save.lease); 
            this.getInstance().saveLeases();
        }else{
            this.getInstance().saveSlice();
        }
        //console.log(saving);
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

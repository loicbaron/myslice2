import alt from '../alt';
import actions from '../actions/SlicesActions';
import source from '../sources/SlicesSource';

class SlicesStore {

    constructor() {
        this.slices = [];

        /* the currently active slice */
        this.current = {
            slice: {},
            users: [],
            resources: []
        };

        this.filter = [];

        this.dialog = null;

        /* for slices we also have a menu */
        this.menu = false;

        this.errorMessage = null;

        this.bindListeners({
            setCurrentSlice: actions.SET_CURRENT_SLICE,
            getCurrentSlice: actions.GET_CURRENT_SLICE,
            updateSliceElement: actions.UPDATE_SLICE_ELEMENT,
            updateSlices: actions.UPDATE_SLICES,
            fetchSlices: actions.FETCH_SLICES,
            errorSlices: actions.ERROR_SLICES,
            showMenu: actions.SHOW_MENU
        });

        this.registerAsync(source);

    }

    setCurrentSlice(slice) {
        this.current = {
            slice: slice,
            users: [],
            resources: []
        };

        if (!this.getInstance().isLoading()) {
            //this.getInstance().users();
            //this.getInstance().slices();

        }

        localStorage.setItem('slice', this.current.slice.id);
    }

    /*
        returns the id of the current slice
     */
    getCurrentSlice() {
        var current = null;
        var id = localStorage.getItem('slice') || null;
        if (!id) {
            // retrieve the first slice
            current = this.slices[0];
        } else {
            current = this.slices.findIndex(function(sliceElement) {
                return (sliceElement.id === id);
            });
        }

        this.setCurrentSlice(current)
    }

    fetchSlices(filter) {

        this.filter = filter;

        if (!this.getInstance().isLoading()) {
            this.getInstance().fetch();
        }

    }

    updateSliceElement(slice) {
        let index = this.slices.findIndex(function(sliceElement) {
            return (sliceElement.id === slice.id);
        });

        if (index !== -1) {
            this.slices[index] = slice;
        } else {
            this.slices.unshift(slice);
        }

        this.errorMessage = null;
    }

    updateSlices(slices) {
        if (slices.hasOwnProperty('data')) {
            this.slices = slices.data.result;
        } else {
            this.slices = slices;
        }
    }

    errorSlices(errorMessage) {
        console.log(errorMessage);
    }

    showMenu(show) {
        this.menu = show;
    }

}


export default alt.createStore(SlicesStore, 'SlicesStore');


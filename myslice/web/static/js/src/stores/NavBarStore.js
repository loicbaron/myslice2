import alt from '../alt';
import actions from '../actions/SlicesActions';
import source from '../sources/SlicesSource';

class NavStore {

    constructor() {
        this.slices = [];

        /* the currently active slice */
        this.current = {};

        /* for slices we also have a menu */
        this.menu = false;
        
        this.bindListeners({
            setCurrentSlice: actions.SET_CURRENT_SLICE,
            updateSliceElement: actions.UPDATE_SLICE_ELEMENT,
            updateSlices: actions.UPDATE_SLICES,
            fetchSlices: actions.FETCH_SLICES,
            errorSlices: actions.ERROR_SLICES,
            showMenu: actions.SHOW_MENU
        });

        this.registerAsync(source);


    }

    /*
        set the current slice
        - from the localstorage if available
        - if the slice is not found defaults to the first one
        - or empty otherwise
     */
    setCurrentSlice(hrn = null) {

        if (hrn) {
            var index = this.slices.findIndex(function(s) {
                return (s.hrn === hrn);
            });
        } else {
            let id = localStorage.getItem('slice');
            var index = this.slices.findIndex(function(s) {
                return (s.id === id);
            });
        }

        if (index !== -1) {
            this.current = this.slices[index];
        } else if (this.slices.length > 0) {
            this.current = this.slices[0];
        } else {
            this.current = {
                    id: null
            }
        }

        localStorage.setItem('slice', this.current.id);

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

        // check URL
        var u = window.location.href.toString().split(window.location.host)[1].split('/');
        var hrn = u.pop();
        var ctl = u.pop();

        if (ctl === 'slices') {
            this.setCurrentSlice(hrn);
        } else {
            this.setCurrentSlice();
        }

    }

    errorSlices(errorMessage) {
        console.log(errorMessage);
    }

    showMenu(show) {
        this.menu = show;
    }

}


export default alt.createStore(NavStore, 'NavStore');


import alt from '../../alt';
import actions from '../../actions/views/Activity';
import source from '../../sources/views/Activity';

import common from '../../utils/Commons';

class ActivityStore {

    constructor() {
        this.activity = [];
        this.errorMessage = null;

        // Filtered events
        this.filtered = [];

        this.bindListeners({
            updateActivity: actions.UPDATE_ACTIVITY,
            updateActivityElement: actions.UPDATE_ACTIVITY_ELEMENT,
            
            getUserToken: actions.GET_USER_TOKEN,
            setUserToken: actions.SET_USER_TOKEN,

            fetchActivity: actions.FETCH_ACTIVITY,
            watchActivity: actions.WATCH_ACTIVITY,

            filterEvent: actions.FILTER_EVENT,
        });

        this.registerAsync(source);

    }

    getUserToken() {
        let token = sessionStorage.getItem('token') 
        
        if (!token) {
            this.getInstance().getUserToken();
        }
    }

    setUserToken(data) {
        sessionStorage.setItem('token' , data['data']);
    }

    fetchActivity(filter) {
        this.activity = [];
        this.filtered = [];
        this.filter = {
            'action': [],
            'status': [],
            'object': []
        };

        /*
            filter: {
                action: [ a, b, c ],
                status: [ x, y, z ]
            }
         */
        if (filter.length > 0) {
            filter.map(function (f) {
                this.filter[f.name].push(f.value);
            }.bind(this));
        }

        this.getInstance().fetchActivity();

    }

    watchActivity() {}

    updateActivity(activity) {
        if (activity.hasOwnProperty('data')) {
            this.activity = activity.data.result;
        } else {
            this.activity = activity;
        }
    }


    updateActivityElement(activityElement) {
        // Check if we already have this activity in the state
        let index = this.activity.findIndex(function(needle) {
            return (needle.id === activityElement.id);
        });
        /*  If we do we update it, otherwise we add a new
            activity event to the state (at the top of the array) */
        if (index !== -1) {
            this.activity[index] = activityElement;
        } else {
            this.activity.unshift(activityElement);
        }

        this.errorMessage = null;
        // optionally return false to suppress the store change event
    }

    filterEvent(value){
        if(value){
            this.filtered = this.activity.filter(function(el) {
                return common.searchText(el, value);
            });
        }else{
            this.filtered = [];
        }
    }

}


export default alt.createStore(ActivityStore, 'ActivityStore');


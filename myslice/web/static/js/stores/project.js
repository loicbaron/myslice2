/**
 * Project Store
 */

class ProjectStore {

    constructor() {
        var d = new Date();
        var df = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate()+" "+d.getHours()+":"+ d.getMinutes()+":"+d.getSeconds()
        this.label = '';
        this.name = '';
        this.v_public = true;
        this.v_protected = false;
        this.v_private = false;
        this.url = '';
        this.description = '';
        this.start_date = df;
        this.end_date = '';


        this.bindListeners({
            updateLabel: projectactions.UPDATE_LABEL,
            updateName: projectactions.UPDATE_NAME,
            updatePublic: projectactions.UPDATE_PUBLIC,
            updateProtected: projectactions.UPDATE_PROTECTED,
            updatePrivate: projectactions.UPDATE_PRIVATE,
            updateUrl: projectactions.UPDATE_URL,
            updateDescription: projectactions.UPDATE_DESCRIPTION,
            updateStartDate: projectactions.UPDATE_START_DATE,
            updateEndDate: projectactions.UPDATE_END_DATE,
        });
    }

    updateLabel(label) {
        this.label = label;
    }
    updateName(name) {
        this.name = name;
    }
    updatePublic(v_public) {
        this.v_public = v_public;
    }
    updateProtected(v_protected) {
        this.v_protected = v_protected;
    }
    updatePrivate(v_private) {
        this.v_private = v_private;
    }
    updateUrl(url) {
        this.url = url;
    }
    updateDescription(description) {
        this.description = description;
    }
    updateStartDate(start_date) {
        this.start_date = start_date;
    }
    updateEndDate(end_date) {
        this.end_date = end_date;
    }

}

window.projectstore = alt.createStore(ProjectStore, 'ProjectStore');

/**
 * Project Store
 */

class ProjectFormStore {

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
            updateLabel: projectformactions.UPDATE_LABEL,
            updateName: projectformactions.UPDATE_NAME,
            updatePublic: projectformactions.UPDATE_PUBLIC,
            updateProtected: projectformactions.UPDATE_PROTECTED,
            updatePrivate: projectformactions.UPDATE_PRIVATE,
            updateUrl: projectformactions.UPDATE_URL,
            updateDescription: projectformactions.UPDATE_DESCRIPTION,
            updateStartDate: projectformactions.UPDATE_START_DATE,
            updateEndDate: projectformactions.UPDATE_END_DATE,
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

window.projectformstore = alt.createStore(ProjectFormStore, 'ProjectFormStore');

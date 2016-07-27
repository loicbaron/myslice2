import React from 'react';

import store from '../../stores/SliceViewStore';
import actions from '../../actions/SliceViewActions';

import View from '../base/View';
import Dialog from '../base/Dialog';
import DialogHeader from '../base/DialogHeader';
import DialogBody from '../base/DialogBody';
import DialogPanel from '../base/DialogPanel';
import Panel from '../base/Panel';
import PanelHeader from '../base/PanelHeader';
import PanelBody from '../base/PanelBody';
import Title from '../base/Title';
import Button from '../base/Button';

import UsersList from '../UsersList';
import UsersDialog from '../UsersDialog';

class SliceView extends React.Component {

    constructor(props) {
        super(props);
        this.state = store.getState();
        this.onChange = this.onChange.bind(this);
        this.closeDialog = this.closeDialog.bind(this);
    }

    componentDidMount() {
        store.listen(this.onChange);
        console.log(this.props.slice);
    }

    componentWillUnmount() {
        store.unlisten(this.onChange);
    }

    onChange(state) {
        this.setState(state);
    }

    closeDialog() {
        actions.showDialog(null);
    }

    
    render() {
        var panelRight = null;
        var dialog = null;

        if (this.state.errorMessage) {
            return (
                <div>Something is wrong</div>
            );
        }

        switch(this.state.dialog) {
            case 'users':
                dialog = <UsersDialog close={this.closeDialog} />;
                break;
            case 'project':
                dialog = <Dialog close={this.closeDialog}>
                            <DialogPanel>
                                <DialogHeader>
                                    <Title title="New Project" />
                                </DialogHeader>
                                <DialogBody>
                                    <ProjectsForm />
                                </DialogBody>
                            </DialogPanel>
                        </Dialog>;
                break;
        }

        console.log(this.state)

        if (this.state.current) {
            var slice_title = this.state.current.name;

            return (
                <View>
                    <Panel>
                        <PanelHeader>
                            <Title title={slice_title} subtitle={this.state.current.shortname}/>
                        </PanelHeader>
                        <PanelBody>
                        </PanelBody>
                        {dialog}
                    </Panel>
                    {panelRight}
                </View>
            );
        } else {
            return (<View>
                    <Panel>
                        <PanelBody>
                                <div>Wait...</div>
                            </PanelBody>
                        </Panel>
            </View>
            );
        }
    }
}

export default SliceView;
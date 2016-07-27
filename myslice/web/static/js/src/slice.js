import React from 'react';
import ReactDOM from 'react-dom';
import SliceView from './views/slices';

const getCurrentSlice = () => {
    var u = window.location.href.toString().split(window.location.host)[1].split('/');
    var hrn = u.pop();
    var ctl = u.pop();

    if (ctl === 'slices') {
        return hrn;
    }
};

ReactDOM.render(
        <SliceView slice={getCurrentSlice()} />,
        document.getElementById('sliceView')
);
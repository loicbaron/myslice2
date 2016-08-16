import React from 'react';

const ElementTitle = ({label, detail}) =>
    <h3 className="elementTitle">
        {label}
        &nbsp;
        <span>{detail}</span>
    </h3>;

export default ElementTitle;
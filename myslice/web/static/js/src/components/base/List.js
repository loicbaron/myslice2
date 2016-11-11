import React from 'react';

const List = ({children}) =>
    <ul className="elementList">
        {children}
    </ul>;

const ListSimple = ({children}) =>
    <ul className="elementListSimple">
        {children}
    </ul>;

export { List, ListSimple };
/* webpack.config.js */
var path = require('path');
var webpack = require('webpack');

module.exports = {
    context: __dirname,
    entry: {
        settings :"./settings.js",
        password :"./password.js",
        projects: "./projects.js",
        slice: "./slice.js",
        users: "./users.js",
        registration: "./registration.js",
        password_forgot :"./password_forgot.js",
        login: "./login.js",
        navbar: "./navbar.js",
        activity: "./activity.js",
        status: "./status.js",
        dashboard: "./dashboard.js",
        addOrganization : "./addOrganization.js"
    },
    output: {
        filename: "[name].js",
        path: "/root/myslice/myslice/web/static/js/build/",
    },
    module: {
    loaders: [
        {
            test: /\.jsx?$/,
            include: [
                __dirname,
            ],
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
                presets: ['es2015', 'react'],
                compact: false
            }
        }, { test: /\.css$/, loader: 'style-loader!css-loader' },
    ]
    },
};

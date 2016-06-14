/* webpack.config.js */
var path = require('path');
var webpack = require('webpack');

module.exports = {
  context: __dirname,
  entry: {
          userprofile :"./userprofile.js",
          projects: "./projects.js",
          registration: "./registration.js",
          login: "./login.js"
        },
  output: {
    filename: "[name].js",
    path: "../build/",
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

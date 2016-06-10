/* webpack.config.js */
var path = require('path');
var webpack = require('webpack');

module.exports = {
  context: __dirname,
  entry: "./userprofile.js",
  output: {
    filename: "userprofile.js",
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

/* config-overrides.js */
const { override, addBabelPlugin, addWebpackAlias } = require('customize-cra');
const path = require('path');

module.exports = override(
    // 1. Configure Babel to handle the imports in code
    addBabelPlugin([
        'module-resolver',
        {
            root: ['./src'],
            alias: {
                '@': './src',
            },
        },
    ]),

    // 2. Configure Webpack to understand the alias for bundling
    addWebpackAlias({
        '@': path.resolve(__dirname, 'src'),
    }),
);

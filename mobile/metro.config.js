const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const defaultConfig = getDefaultConfig(__dirname);

const config = {
  resolver: {
    alias: {
      '@': './src',
      '@components': './src/components',
      '@screens': './src/screens',
      '@services': './src/services',
      '@store': './src/store',
      '@utils': './src/utils',
      '@types': './src/types',
      '@assets': './src/assets',
    },
  },
};

module.exports = mergeConfig(defaultConfig, config);

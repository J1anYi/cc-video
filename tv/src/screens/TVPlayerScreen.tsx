import React from 'react';
import { View, StyleSheet, StatusBar } from 'react-native';
import Video from 'react-native-video';
import { useRoute } from '@react-navigation/native';

export function TVPlayerScreen() {
  const route = useRoute();
  const { movieId } = route.params as { movieId: number };

  return (
    <View style={styles.container}>
      <StatusBar hidden />
      <Video
        source={{ uri: 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8' }}
        style={styles.video}
        controls
        resizeMode='contain'
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' },
  video: { flex: 1 },
});

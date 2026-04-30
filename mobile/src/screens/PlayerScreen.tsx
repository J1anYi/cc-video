import React from 'react';
import { View, StyleSheet, StatusBar } from 'react-native';
import Video from 'react-native-video';
import { useRoute } from '@react-navigation/native';
import apiService from '../services/api';

export function PlayerScreen() {
  const route = useRoute();
  const { movieId } = route.params as { movieId: number };
  const streamUrl = apiService.getStreamUrl(movieId);

  return (
    <View style={styles.container}>
      <StatusBar hidden />
      <Video
        source={{ uri: streamUrl }}
        style={styles.video}
        controls
        resizeMode='contain'
        playInBackground
        playWhenInactive
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' },
  video: { flex: 1 },
});

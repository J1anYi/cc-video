import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity } from 'react-native';
import { useRoute, useNavigation } from '@react-navigation/native';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { fetchMovie } from '../store/moviesSlice';

export function MovieDetailScreen() {
  const route = useRoute();
  const navigation = useNavigation();
  const dispatch = useDispatch();
  const { movieId } = route.params as { movieId: number };
  const { currentMovie } = useSelector((state: RootState) => state.movies);

  React.useEffect(() => {
    dispatch(fetchMovie(movieId) as any);
  }, [dispatch, movieId]);

  const handlePlay = () => {
    navigation.navigate('Player' as never, { movieId } as never);
  };

  if (!currentMovie) {
    return (
      <View style={styles.container}>
        <Text style={styles.loading}>Loading...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <Image source={{ uri: currentMovie.backdrop_url }} style={styles.backdrop} />
      <View style={styles.content}>
        <Text style={styles.title}>{currentMovie.title}</Text>
        <View style={styles.meta}>
          <Text style={styles.metaText}>{currentMovie.release_year}</Text>
          <Text style={styles.metaText}>{currentMovie.duration} min</Text>
          <Text style={styles.rating}>{currentMovie.rating.toFixed(1)}</Text>
        </View>
        <TouchableOpacity style={styles.playButton} onPress={handlePlay}>
          <Text style={styles.playButtonText}>Play</Text>
        </TouchableOpacity>
        <Text style={styles.description}>{currentMovie.description}</Text>
        <Text style={styles.sectionTitle}>Director</Text>
        <Text style={styles.sectionText}>{currentMovie.director}</Text>
        <Text style={styles.sectionTitle}>Cast</Text>
        <Text style={styles.sectionText}>{currentMovie.cast.join(', ')}</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#141414' },
  backdrop: { width: '100%', height: 220 },
  content: { padding: 16 },
  title: { color: '#fff', fontSize: 24, fontWeight: 'bold', marginBottom: 8 },
  meta: { flexDirection: 'row', marginBottom: 16 },
  metaText: { color: '#888', marginRight: 16 },
  rating: { color: '#ffd700', fontWeight: 'bold' },
  playButton: { backgroundColor: '#e50914', paddingVertical: 12, borderRadius: 4, alignItems: 'center', marginBottom: 16 },
  playButtonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  description: { color: '#ccc', lineHeight: 22, marginBottom: 16 },
  sectionTitle: { color: '#fff', fontSize: 16, fontWeight: 'bold', marginTop: 12 },
  sectionText: { color: '#888', marginTop: 4 },
  loading: { color: '#fff', textAlign: 'center', marginTop: 100 },
});

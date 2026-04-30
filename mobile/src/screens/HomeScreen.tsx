import React from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Image, ActivityIndicator } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { fetchTrending } from '../store/moviesSlice';
import { Movie } from '../types';

export function HomeScreen() {
  const dispatch = useDispatch();
  const navigation = useNavigation();
  const { trending, isLoading } = useSelector((state: RootState) => state.movies);

  React.useEffect(() => {
    dispatch(fetchTrending() as any);
  }, [dispatch]);

  const renderMovie = ({ item }: { item: Movie }) => (
    <TouchableOpacity
      style={styles.movieCard}
      onPress={() => navigation.navigate('MovieDetail' as never, { movieId: item.id } as never)}
    >
      <Image source={{ uri: item.poster_url }} style={styles.poster} />
      <View style={styles.movieInfo}>
        <Text style={styles.title} numberOfLines={2}>{item.title}</Text>
        <Text style={styles.rating}>{item.rating.toFixed(1)}</Text>
      </View>
    </TouchableOpacity>
  );

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#e50914" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={trending}
        renderItem={renderMovie}
        keyExtractor={(item) => item.id.toString()}
        numColumns={2}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#141414' },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#141414' },
  list: { padding: 8 },
  movieCard: { flex: 1, margin: 8, backgroundColor: '#1f1f1f', borderRadius: 8, overflow: 'hidden' },
  poster: { width: '100%', height: 200 },
  movieInfo: { padding: 8 },
  title: { color: '#fff', fontSize: 14, fontWeight: 'bold' },
  rating: { color: '#ffd700', fontSize: 12, marginTop: 4 },
});

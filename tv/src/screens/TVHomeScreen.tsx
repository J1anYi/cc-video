import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { TVMovieRow } from '../components/TVMovieRow';
import { Movie } from '../types';

const mockTrending: Movie[] = [
  { id: 1, title: 'Action Movie 1', description: 'An action movie', poster_url: 'https://picsum.photos/200/300', backdrop_url: 'https://picsum.photos/800/450', video_url: '', duration: 120, release_year: 2024, rating: 8.5, genres: ['Action'], director: 'Director', cast: ['Actor 1'] },
  { id: 2, title: 'Drama Movie 1', description: 'A drama movie', poster_url: 'https://picsum.photos/200/300', backdrop_url: 'https://picsum.photos/800/450', video_url: '', duration: 110, release_year: 2024, rating: 7.8, genres: ['Drama'], director: 'Director', cast: ['Actor 2'] },
];

export function TVHomeScreen() {
  const navigation = useNavigation();

  const handleSelectMovie = (movie: Movie) => {
    navigation.navigate('MovieDetail' as never, { movieId: movie.id } as never);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.logo}>CC Video</Text>
        <TouchableOpacity isTVSelectable style={styles.searchButton}>
          <Text style={styles.searchText}>Search</Text>
        </TouchableOpacity>
      </View>
      <ScrollView style={styles.content}>
        <TVMovieRow title='Trending Now' movies={mockTrending} onSelectMovie={handleSelectMovie} />
        <TVMovieRow title='Popular' movies={mockTrending} onSelectMovie={handleSelectMovie} />
        <TVMovieRow title='New Releases' movies={mockTrending} onSelectMovie={handleSelectMovie} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 48, paddingVertical: 24 },
  logo: { color: '#e50914', fontSize: 36, fontWeight: 'bold' },
  searchButton: { backgroundColor: '#1f1f1f', paddingVertical: 12, paddingHorizontal: 24, borderRadius: 8 },
  searchText: { color: '#fff', fontSize: 18 },
  content: { flex: 1 },
});

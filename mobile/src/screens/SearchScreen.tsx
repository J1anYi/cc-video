import React from 'react';
import { View, Text, StyleSheet, TextInput, FlatList, TouchableOpacity, Image } from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { searchMovies, clearSearchResults } from '../store/moviesSlice';
import { Movie } from '../types';

export function SearchScreen() {
  const [query, setQuery] = React.useState('');
  const dispatch = useDispatch();
  const searchResults = useSelector((state: RootState) => state.movies.searchResults);

  const handleSearch = () => {
    if (query.trim()) {
      dispatch(searchMovies(query) as any);
    }
  };

  const renderMovie = ({ item }: { item: Movie }) => (
    <TouchableOpacity style={styles.movieCard}>
      <Image source={{ uri: item.poster_url }} style={styles.poster} />
      <View style={styles.movieInfo}>
        <Text style={styles.title} numberOfLines={2}>{item.title}</Text>
        <Text style={styles.year}>{item.release_year}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder='Search movies...'
          placeholderTextColor='#888'
          value={query}
          onChangeText={setQuery}
          onSubmitEditing={handleSearch}
        />
      </View>
      <FlatList
        data={searchResults}
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
  searchContainer: { padding: 16 },
  searchInput: { backgroundColor: '#1f1f1f', borderRadius: 8, padding: 12, color: '#fff' },
  list: { padding: 8 },
  movieCard: { flex: 1, margin: 8, backgroundColor: '#1f1f1f', borderRadius: 8, overflow: 'hidden' },
  poster: { width: '100%', height: 180 },
  movieInfo: { padding: 8 },
  title: { color: '#fff', fontSize: 12, fontWeight: 'bold' },
  year: { color: '#888', fontSize: 10, marginTop: 2 },
});

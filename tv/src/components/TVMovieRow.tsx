import React from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity } from 'react-native';
import { Movie } from '../types';

interface TVMovieRowProps {
  title: string;
  movies: Movie[];
  onSelectMovie: (movie: Movie) => void;
}

export function TVMovieRow({ title, movies, onSelectMovie }: TVMovieRowProps) {
  const renderMovie = ({ item, index }: { item: Movie; index: number }) => (
    <TouchableOpacity
      style={styles.movieCard}
      onPress={() => onSelectMovie(item)}
      onFocus={() => {}}
      hasTVPreferredFocus={index === 0}
      isTVSelectable
    >
      <Image source={{ uri: item.poster_url }} style={styles.poster} />
      <View style={styles.overlay}>
        <Text style={styles.title} numberOfLines={1}>{item.title}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.rowTitle}>{title}</Text>
      <FlatList
        horizontal
        data={movies}
        renderItem={renderMovie}
        keyExtractor={(item) => item.id.toString()}
        showsHorizontalScrollIndicator={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginVertical: 16 },
  rowTitle: { color: '#fff', fontSize: 24, fontWeight: 'bold', marginLeft: 48, marginBottom: 12 },
  movieCard: { width: 200, height: 300, marginHorizontal: 8, borderRadius: 8, overflow: 'hidden', backgroundColor: '#1f1f1f' },
  poster: { width: '100%', height: '100%' },
  overlay: { position: 'absolute', bottom: 0, left: 0, right: 0, backgroundColor: 'rgba(0,0,0,0.8)', padding: 8 },
  title: { color: '#fff', fontSize: 14, fontWeight: 'bold' },
});

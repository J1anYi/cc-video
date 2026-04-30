import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity } from 'react-native';
import { useRoute, useNavigation } from '@react-navigation/native';
import { TVButton } from '../components/TVButton';

export function TVMovieDetailScreen() {
  const route = useRoute();
  const navigation = useNavigation();
  const { movieId } = route.params as { movieId: number };

  const handlePlay = () => {
    navigation.navigate('Player' as never, { movieId } as never);
  };

  return (
    <ScrollView style={styles.container}>
      <Image source={{ uri: 'https://picsum.photos/800/450' }} style={styles.backdrop} />
      <View style={styles.content}>
        <Text style={styles.title}>Movie Title</Text>
        <View style={styles.meta}>
          <Text style={styles.metaText}>2024</Text>
          <Text style={styles.metaText}>120 min</Text>
          <Text style={styles.rating}>8.5</Text>
        </View>
        <View style={styles.buttons}>
          <TVButton title='Play' onPress={handlePlay} focused />
          <TVButton title='Add to List' onPress={() => {}} />
        </View>
        <Text style={styles.description}>This is the movie description. A compelling story of adventure and excitement.</Text>
        <Text style={styles.sectionTitle}>Cast</Text>
        <Text style={styles.sectionText}>Actor 1, Actor 2, Actor 3</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' },
  backdrop: { width: '100%', height: 400 },
  content: { padding: 48 },
  title: { color: '#fff', fontSize: 48, fontWeight: 'bold', marginBottom: 16 },
  meta: { flexDirection: 'row', marginBottom: 24 },
  metaText: { color: '#888', fontSize: 20, marginRight: 24 },
  rating: { color: '#ffd700', fontSize: 20, fontWeight: 'bold' },
  buttons: { flexDirection: 'row', marginBottom: 24 },
  description: { color: '#ccc', fontSize: 18, lineHeight: 28, marginBottom: 24 },
  sectionTitle: { color: '#fff', fontSize: 24, fontWeight: 'bold', marginTop: 16 },
  sectionText: { color: '#888', fontSize: 16, marginTop: 8 },
});

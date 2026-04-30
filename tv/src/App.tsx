import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { RootStackParamList } from './types';

import { TVHomeScreen } from './screens/TVHomeScreen';
import { TVMovieDetailScreen } from './screens/TVMovieDetailScreen';
import { TVPlayerScreen } from './screens/TVPlayerScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName='Main'
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: '#000' },
        }}
      >
        <Stack.Screen name='Main' component={TVHomeScreen} />
        <Stack.Screen name='MovieDetail' component={TVMovieDetailScreen} />
        <Stack.Screen name='Player' component={TVPlayerScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

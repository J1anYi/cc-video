import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Provider, useSelector } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { store, persistor } from './store';
import { RootState } from './store';
import { RootStackParamList, MainTabParamList } from './types';

import { LoginScreen } from './screens/LoginScreen';
import { HomeScreen } from './screens/HomeScreen';
import { SearchScreen } from './screens/SearchScreen';
import { MovieDetailScreen } from './screens/MovieDetailScreen';
import { PlayerScreen } from './screens/PlayerScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

function MainTabs() {
  return (
    <Tab.Navigator screenOptions={{ headerStyle: { backgroundColor: '#141414' }, headerTintColor: '#fff', tabBarStyle: { backgroundColor: '#141414' }, tabBarActiveTintColor: '#e50914' }}>
      <Tab.Screen name='Home' component={HomeScreen} />
      <Tab.Screen name='Discover' component={SearchScreen} />
    </Tab.Navigator>
  );
}

function AppNavigator() {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerStyle: { backgroundColor: '#141414' }, headerTintColor: '#fff', contentStyle: { backgroundColor: '#141414' } }}>
        {!isAuthenticated ? (
          <Stack.Screen name='Auth' component={LoginScreen} options={{ headerShown: false }} />
        ) : (
          <>
            <Stack.Screen name='Main' component={MainTabs} options={{ headerShown: false }} />
            <Stack.Screen name='MovieDetail' component={MovieDetailScreen} options={{ title: 'Movie' }} />
            <Stack.Screen name='Player' component={PlayerScreen} options={{ headerShown: false, orientation: 'landscape' }} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default function App() {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <AppNavigator />
      </PersistGate>
    </Provider>
  );
}

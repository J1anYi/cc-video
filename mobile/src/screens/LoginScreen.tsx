import React from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, Alert } from 'react-native';
import { useDispatch } from 'react-redux';
import { login } from '../store/authSlice';

export function LoginScreen() {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const dispatch = useDispatch();

  const handleLogin = async () => {
    if (!email.trim() || !password.trim()) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }
    try {
      await dispatch(login({ email, password }) as any).unwrap();
    } catch (error: any) {
      Alert.alert('Login Failed', error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>CC Video</Text>
      <TextInput
        style={styles.input}
        placeholder='Email'
        placeholderTextColor='#888'
        value={email}
        onChangeText={setEmail}
        autoCapitalize='none'
        keyboardType='email-address'
      />
      <TextInput
        style={styles.input}
        placeholder='Password'
        placeholderTextColor='#888'
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Sign In</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.linkButton}>
        <Text style={styles.linkText}>New user? Sign up</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#141414', padding: 20 },
  logo: { fontSize: 36, fontWeight: 'bold', color: '#e50914', marginBottom: 40 },
  input: { width: '100%', height: 50, backgroundColor: '#1f1f1f', borderRadius: 4, marginBottom: 12, paddingHorizontal: 16, color: '#fff' },
  button: { width: '100%', height: 50, backgroundColor: '#e50914', borderRadius: 4, justifyContent: 'center', alignItems: 'center', marginTop: 12 },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  linkButton: { marginTop: 20 },
  linkText: { color: '#888' },
});

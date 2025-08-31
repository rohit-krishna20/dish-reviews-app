import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { api } from './api';

export default function LoginScreen({ onAuth }) {
  const [email, setEmail] = useState('test@example.com');
  const [password, setPassword] = useState('password123');
  const [handle, setHandle] = useState('tester');
  const [mode, setMode] = useState('login');

  async function submit() {
    try {
      const path = mode === 'login' ? '/auth/login' : '/auth/register';
      const body = mode === 'login' ? { email, password } : { email, password, handle };
      const res = await api(path, 'POST', body);
      onAuth(res.access_token);
    } catch (e) {
      Alert.alert('Auth error', e.message);
    }
  }

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 28, marginBottom: 12 }}>Dish Reviews</Text>
      {mode === 'register' && (
        <TextInput placeholder="Handle" value={handle} onChangeText={setHandle} style={{ borderWidth:1, marginBottom:8, padding:8 }} />
      )}
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} autoCapitalize="none" style={{ borderWidth:1, marginBottom:8, padding:8 }} />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry style={{ borderWidth:1, marginBottom:8, padding:8 }} />
      <Button title={mode === 'login' ? 'Login' : 'Register'} onPress={submit} />
      <View style={{ height: 12 }} />
      <Button title={mode === 'login' ? 'Need an account? Register' : 'Have an account? Login'} onPress={() => setMode(mode === 'login' ? 'register' : 'login')} />
    </View>
  );
}

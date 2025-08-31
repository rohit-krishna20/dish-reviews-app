import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { api } from './api';

export default function AddReviewScreen({ route, navigation }) {
  const { dishId, token, visitId } = route.params;
  const [overall, setOverall] = useState('5');
  const [text, setText] = useState('');

  async function submit() {
    try {
      await api(`/visits/review/${dishId}`, 'POST', {
        visit_id: visitId,
        rating_overall: parseInt(overall),
        text
      }, token);
      Alert.alert('Review added!');
      navigation.goBack();
    } catch (e) {
      Alert.alert('Error', e.message);
    }
  }

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 22, fontWeight: '700', marginBottom: 16 }}>Add Review</Text>
      <Text>Overall Rating (1–5):</Text>
      <TextInput
        keyboardType="numeric"
        value={overall}
        onChangeText={setOverall}
        style={{ borderWidth: 1, marginVertical: 8, padding: 8 }}
      />
      <Text>Comments (optional):</Text>
      <TextInput
        value={text}
        onChangeText={setText}
        placeholder="Write your thoughts..."
        style={{ borderWidth: 1, marginVertical: 8, padding: 8, minHeight: 80 }}
        multiline
      />
      <Button title="Submit" onPress={submit} />
    </View>
  );
}

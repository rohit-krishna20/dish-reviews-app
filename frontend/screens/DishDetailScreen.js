import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Button } from 'react-native';
import { api } from './api';

export default function DishDetailScreen({ route, navigation }) {
  const { dishId, dishName, token, visitId } = route.params;
  const [data, setData] = useState(null);

  async function load() {
    const res = await api(`/dishes/${dishId}`);
    setData(res);
  }

  useEffect(() => { load(); }, []);

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 22, fontWeight: '700', marginBottom: 8 }}>{dishName}</Text>

      {data && (
        <>
          <Text>
            {data.dish.avg_rating ? `${data.dish.avg_rating}★ (${data.dish.review_count} reviews)` : 'No reviews yet'}
          </Text>
          <Text style={{ marginBottom: 16 }}>Bayes: {data.dish.bayes_score} | Wilson: {data.dish.wilson_lb}</Text>

          {visitId && (
            <Button
              title="Add Review"
              onPress={() => navigation.navigate('AddReview', { dishId, token, visitId })}
            />
          )}

          <FlatList
            style={{ marginTop: 20 }}
            data={data.reviews}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <View style={{ marginBottom: 12, borderBottomWidth: 0.5, paddingBottom: 8 }}>
                <Text style={{ fontWeight: '600' }}>{item.rating_overall}★</Text>
                {item.text ? <Text>{item.text}</Text> : null}
                <Text style={{ color: '#555' }}>{new Date(item.created_at).toLocaleString()}</Text>
              </View>
            )}
          />
        </>
      )}
    </View>
  );
}

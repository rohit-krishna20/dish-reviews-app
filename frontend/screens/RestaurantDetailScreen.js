import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, Button, Alert } from 'react-native';
import { api } from './api';

export default function RestaurantDetailScreen({ route, navigation }) {
  const { restaurant, token } = route.params;
  const [menu, setMenu] = useState(null);
  const [visitId, setVisitId] = useState(null);

  async function loadMenu() {
    try {
      const res = await api(`/restaurants/${restaurant.id}/menu`);
      setMenu(res);
    } catch (e) {
      console.error(e);
    }
  }

  async function startVisit() {
    try {
      const res = await api(`/visits`, 'POST', { restaurant_id: restaurant.id, method: 'unverified' }, token);
      setVisitId(res.visit_id);
      Alert.alert('Visit started', `Verified: ${res.verified}`);
    } catch (e) {
      Alert.alert('Error', e.message);
    }
  }

  useEffect(() => { loadMenu(); }, []);

  return (
    <View style={{ flex: 1 }}>
      <View style={{ padding:16, borderBottomWidth:1 }}>
        <Text style={{ fontSize: 22, fontWeight:'700' }}>{restaurant.name}</Text>
        <Text>{restaurant.street || ''} {restaurant.city || ''}</Text>
        <View style={{ height: 8 }} />
        <Button title={visitId ? 'Visit Active' : 'Start Visit'} onPress={startVisit} />
      </View>

      {menu && (
        <FlatList
          data={menu.sections}
          keyExtractor={(sec) => sec.title}
          renderItem={({ item: sec }) => (
            <View style={{ padding: 16 }}>
              <Text style={{ fontSize: 18, fontWeight: '700' }}>{sec.title}</Text>
              {sec.dishes.map((d) => (
                <TouchableOpacity
                  key={d.id}
                  onPress={() => navigation.navigate('DishDetail', { dishId: d.id, dishName: d.name, token, visitId })}
                  style={{ paddingVertical: 10, borderBottomWidth: 0.5 }}
                >
                  <Text style={{ fontSize: 16 }}>{d.name} {d.price_cents ? `· $${(d.price_cents/100).toFixed(2)}` : ''}</Text>
                  <Text>{d.avg_rating ? `${d.avg_rating}★ (${d.review_count})` : 'No ratings yet'}</Text>
                </TouchableOpacity>
              ))}
            </View>
          )}
        />
      )}
    </View>
  );
}

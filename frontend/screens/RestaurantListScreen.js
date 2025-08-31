import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, RefreshControl } from 'react-native';
import { api } from './api';

export default function RestaurantListScreen({ navigation, token }) {
  const [data, setData] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  async function load() {
    setRefreshing(true);
    try {
      const res = await api('/restaurants');
      setData(res);
    } catch (e) {
      console.error(e);
    } finally {
      setRefreshing(false);
    }
  }

  useEffect(() => { load(); }, []);

  return (
    <View style={{ flex: 1 }}>
      <FlatList
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />}
        data={data}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity
            onPress={() => navigation.navigate('RestaurantDetail', { restaurant: item, token })}
            style={{ padding: 16, borderBottomWidth: 1 }}
          >
            <Text style={{ fontSize: 18, fontWeight: '600' }}>{item.name}</Text>
            <Text>{item.street || ''} {item.city || ''}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

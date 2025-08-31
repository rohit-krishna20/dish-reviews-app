import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from './screens/LoginScreen';
import RestaurantListScreen from './screens/RestaurantListScreen';
import RestaurantDetailScreen from './screens/RestaurantDetailScreen';
import DishDetailScreen from './screens/DishDetailScreen';
import AddReviewScreen from './screens/AddReviewScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  const [token, setToken] = useState(null);
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName={token ? 'Restaurants' : 'Login'}>
        <Stack.Screen name="Login" options={{ title: 'Sign in' }}>
          {(props) => <LoginScreen {...props} onAuth={setToken} />}
        </Stack.Screen>
        <Stack.Screen name="Restaurants" options={{ title: 'Restaurants' }}>
          {(props) => <RestaurantListScreen {...props} token={token} />}
        </Stack.Screen>
        <Stack.Screen name="RestaurantDetail" component={RestaurantDetailScreen} options={{ title: 'Menu' }} />
        <Stack.Screen name="DishDetail" component={DishDetailScreen} options={{ title: 'Dish' }} />
        <Stack.Screen name="AddReview" component={AddReviewScreen} options={{ title: 'Add Review' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

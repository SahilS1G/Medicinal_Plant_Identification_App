import { SafeAreaView, StyleSheet, Text, View } from 'react-native'
import React from 'react'

import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
// import Main from '../screens/Main'
import Home from '../screens/Home'
import History from '../screens/History'
import Profile from '../screens/Profile'

export type AppStackParamList = {
    Home: undefined;
    History: undefined;
    Profile: undefined;

}

const Tab = createBottomTabNavigator<AppStackParamList>()

// const Stack = createNativeStackNavigator<AppStackParamList>()

export const AppStack = () => {
  return (
   <Tab.Navigator>
     <Tab.Screen name='Home' component={Home}/>
     <Tab.Screen name='History' component={History}/>
      <Tab.Screen name='Profile' component={Profile}/>
    </Tab.Navigator>
  )
}



const styles = StyleSheet.create({})
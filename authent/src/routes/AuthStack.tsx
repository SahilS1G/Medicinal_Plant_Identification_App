import { SafeAreaView, StyleSheet, Text, View } from 'react-native'
import React from 'react'

import {createNativeStackNavigator} from '@react-navigation/native-stack'


import Login from '../screens/Login'
import Signup from '../screens/Signup'


export type AuthStackParamList = {
    Login: undefined;
    Signup: undefined;
}

const Stack = createNativeStackNavigator<AuthStackParamList>()

export const AuthStack = () => {
  console.log('Stack')
  return (
    <Stack.Navigator 
        screenOptions={{
            headerTitleAlign:'center',
            headerBackTitleVisible: false,
        }}
        initialRouteName='Login'
    >
      <Stack.Screen name='Login' component={Login}/>
      <Stack.Screen name='Signup' component={Signup}/>
    </Stack.Navigator>
  )
}



const styles = StyleSheet.create({})
import { View, Text } from 'react-native'
import React, { useContext, useEffect, useState } from 'react'

import {NavigationContainer} from '@react-navigation/native'
import { AppwriteContext } from '../appwrite/appwriteContext'
import Loading from '../components/Loading'

//routes
import { AppStack } from './AppStack'
import { AuthStack } from './AuthStack'



export default function Router()  {
  const [isLoading,setIsLoading] = useState<boolean>(true);
  const {appwrite, isLoggedIn,setIsLoggedIn} = useContext(AppwriteContext)

  useEffect(() => {
    appwrite
    .getCurrnetUser()
    .then(response => {
      setIsLoading(false)
      if (response) {
        setIsLoggedIn(true)
      }
      // console.log(isLoggedIn)
    })
    .catch(_ => {
      setIsLoading(false)
      setIsLoggedIn(false)
    })
    
  }, [appwrite,isLoggedIn])
  
  if (isLoading) {
    return <Loading/>
  }

  return (
   <NavigationContainer>
    {isLoggedIn ? <AppStack/> : <AuthStack/>}
   </NavigationContainer>
  )
}


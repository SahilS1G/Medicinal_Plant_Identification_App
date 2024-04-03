// import { StyleSheet, Text, View, SafeAreaView, Image } from 'react-native'
import { StyleSheet, Text, View, SafeAreaView, Image, KeyboardAvoidingView, TextInput, Pressable, Platform } from 'react-native'

import React, { useContext, useState, useEffect } from 'react'
import { FAB } from '@rneui/themed'
import {launchImageLibrary} from 'react-native-image-picker';
import {launchCamera} from 'react-native-image-picker';

//snackbar
import Snackbar from 'react-native-snackbar'

//context API
import { AppwriteContext } from '../appwrite/appwriteContext'

type UserObj = {
  name: String;
  email:String;
}



const Home = () => {
  const [userData, setUserData] = useState<UserObj>()
  const {appwrite,setIsLoggedIn} = useContext(AppwriteContext)
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const handleLogout = () => {
    appwrite.logout()
    .then(() => {
      setIsLoggedIn(false);
      Snackbar.show({
        text:"logout successful",
        duration:Snackbar.LENGTH_SHORT
      })
    })
  }

  const handleCameraLaunch = () => {
    const options = {
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    };
  
    launchCamera({
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    }, response => {
      if (response.didCancel) {
        console.log('User cancelled camera');
      } else if (response.errorCode) {
        console.log('Camera Error: ', response.errorCode);
      } else {
        let imageUri =  response.assets?.[0]?.uri;
        setSelectedImage(imageUri || null);
        console.log(imageUri);
      }
    });
  }

  const openImagePicker = () => {
    const options = {
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    };

    launchImageLibrary({
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    }, (response) => {
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.errorCode) {
        console.log('Image picker error: ', response.errorCode);
      } else {
        let imageUri =  response.assets?.[0]?.uri;
        setSelectedImage(imageUri || null);
      }
    });
  };

  useEffect(() => {
    appwrite.getCurrnetUser()
    .then(response => {
      if (response) {
        const user: UserObj = {
          name: response.name,
          email: response.email
        }
        setUserData(user)
      }
    })
  }, [appwrite])
  

  return (
    <SafeAreaView style={styles.container}>
    <View style={styles.welcomeContainer}>
      
      <Image
        source={{
          uri: 'https://static.zerochan.net/Thorfinn.full.2489996.png',
          width: 400,
          height: 300,
          cache: 'default',
        }}
        resizeMode="contain"
      />

      <Text style={styles.message}>
        Build Fast. Scale Big. All in One Place.
      </Text>
      <Pressable
            onPress={handleCameraLaunch}
            >
            <Text>camera</Text>
      </Pressable>
      <Pressable
            onPress={openImagePicker}
            >
            <Text>gallery</Text>
      </Pressable>
      {selectedImage && (
        <Image
          source={{ uri: selectedImage,
            width: 400,
          height: 300,
          cache: 'default',
          }}
          style={{ flex: 1 }}
          resizeMode="contain"
        />
      )}
      {userData && (
        <View style={styles.userContainer}>
          <Text style={styles.userDetails}>Name: {userData.name}</Text>
          <Text style={styles.userDetails}>Email: {userData.email}</Text>
        </View>
      )}
    </View>
    <FAB
      placement="right"
      color="#f02e65"
      size="large"
      title="Logout"
      icon={{name: 'logout', color: '#FFFFFF'}}
      onPress={handleLogout}
    />
  </SafeAreaView>
  )
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0D32',
  },
  welcomeContainer: {
    padding: 12,

    flex: 1,
    alignItems: 'center',
  },
  message: {
    fontSize: 26,
    fontWeight: '500',
    color: '#FFFFFF',
  },
  userContainer: {
    marginTop: 24,
  },
  userDetails: {
    fontSize: 20,
    color: '#FFFFFF',
  },
})

export default Home

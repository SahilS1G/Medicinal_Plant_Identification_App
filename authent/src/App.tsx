import React from 'react';
import type {PropsWithChildren} from 'react';
import {
  
  StyleSheet,
  
} from 'react-native';
import Home from './screens/Home';
import Router  from './routes/Router';
// import { AuthStack } from './routes/AuthStack';

function App(): React.JSX.Element {

  return (
    <>
    {/* <Router/> */}
    <Home/>

    </>
  );
}

const styles = StyleSheet.create({
  
});

export default App;

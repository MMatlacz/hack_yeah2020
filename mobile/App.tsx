import React from 'react';
import {NavigationContainer} from "@react-navigation/native";
import { createStackNavigator } from '@react-navigation/stack';

import 'react-native-gesture-handler';

import Main from "./src/views/help-requests/main";
import LogIn from "./src/views/user/LogIn";
import {AppLoading} from "expo";
import UserService from "./src/data/User";
import HelpRequestsService from "./src/data/HelpRequests";


const Stack = createStackNavigator();


export default class App extends React.Component {
  constructor(props: any) {
    super(props);
    this.state = {
      user: null
    };
    this.setUser = this.setUser.bind(this);
    this.getUserService = this.getUserService.bind(this);
    this.getHelpRequestsService = this.getHelpRequestsService.bind(this);
  }

  componentDidMount(): void {
    this.getUserService().fetchLocalUser();

    // use it to turn off cache of user
    // this.setUser({});
  }

  getUserService() {
    return new UserService(this.setUser);
  }

  getHelpRequestsService() {
    return new HelpRequestsService(this.state.user);
  }

  setUser(newUser: object) {
    this.setState({
      user: newUser
    });
  }

  isLoading() {
    return !this.state.user;
  }

  render = () => {
    if(this.isLoading()) {
      return <AppLoading/>;
    }

    if (this.state.user && this.state.user.access_token) {
      return (
        <NavigationContainer>
          <Stack.Navigator initialRouteName="Home">
            <Stack.Screen name="Home"  >
              {props => <Main {...props} helpRequestsService={this.getHelpRequestsService()} />}
            </Stack.Screen>
          </Stack.Navigator>
        </NavigationContainer>
      )
    } else {
      return (
        <NavigationContainer>
          <Stack.Navigator initialRouteName="LogIn">
            <Stack.Screen name="LogIn">
              {props => <LogIn {...props} userSerivice={this.getUserService()} />}
            </Stack.Screen>
          </Stack.Navigator>
        </NavigationContainer>
      )
    }
  };
}

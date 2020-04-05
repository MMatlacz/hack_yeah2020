import { API_URL } from 'react-native-dotenv'
import {AsyncStorage} from "react-native";


class UserService {
    apiURL: string;
    setUser: any;

    constructor(setUser: any) {
        this.setUser = setUser;
        this.apiURL = API_URL;

        this.registerUser = this.registerUser.bind(this);
        this.logIn = this.logIn.bind(this);
        this.fetchLocalUser = this.fetchLocalUser.bind(this);
        this.setLocalUser = this.setLocalUser.bind(this);
    }

    async fetchLocalUser() {
        AsyncStorage.getItem('user').then((userStr) => {
          this.setUser(JSON.parse(userStr || '{}'));
        });
    }

    async setLocalUser(user: object) {
        await AsyncStorage.setItem('user', JSON.stringify(user));
    }

    async registerUser(userRequest: UserRequest) {
        let response = await fetch(this.apiURL + '/users/', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userRequest)
        });

        if (response.status != 201) {
            throw await response.text();
        }

        return await this.logIn(userRequest.email, userRequest.password);
    }

    async logIn(email: string, password: string) {
        const url = this.apiURL + '/users/auth/tokens';

        let response = await fetch(url, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({email, password})
        });

        if (response.status != 200){
            throw await response.text();
        }

        const body = await response.json();
        const user = {
            email,
            access_token: body.access_token
        };
        this.setLocalUser(user);
        this.setUser(user);
        return user;
    }
}
export default UserService;